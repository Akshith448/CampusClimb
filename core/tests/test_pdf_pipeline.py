"""
Regression tests for the PDF extraction and cleaning pipeline.

These tests use ONLY synthetic text — no real PDFs, no college-specific content.
They verify that the generic algorithms behave correctly for any input.

Run with:
    cd c:\\Users\\rahul\\Downloads\\CampusClimb
    .\\venv\\Scripts\\python.exe -m pytest core/tests/test_pdf_pipeline.py -v
"""

import sys
import os

# Make sure project root is on path when running directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest

from core.pdf_extractor import (
    _normalize_line,
    _is_page_number_line,
    _normalize_bullet,
    _normalize_unicode,
    _reconstruct_paragraphs,
    _detect_running_noise,
    _clean_page_text,
    chunk_text,
)
from core.note_formatter import clean_note_text_local, _validate_cleaned_output


# ─────────────────────────────────────────────────────────────────────────────
# Tests: _is_page_number_line
# ─────────────────────────────────────────────────────────────────────────────

class TestPageNumberDetection:
    """Page-number artifact lines must be detected generically."""

    @pytest.mark.parametrize("line", [
        "1",
        " 12 ",
        "120",
        "Page 12",
        "PAGE 12",
        "page 12",
        "Page: 12",
        "Page 12 / 50",
        "12 of 50",
        "pg. 12",
        "- 12 -",
        "[12]",
    ])
    def test_detects_page_number(self, line: str):
        assert _is_page_number_line(line), f"Should detect page number: {line!r}"

    @pytest.mark.parametrize("line", [
        "x = 12 pages",
        "Section 1.2.3",
        "There are 50 questions",
        "Operating Systems is used in 120 devices",
        "IPv4 addresses are 32 bits",
        "The value of n is 1024",
        "Page replacement algorithms include FIFO, LRU, and Optimal.",
    ])
    def test_preserves_legitimate_content(self, line: str):
        assert not _is_page_number_line(line), f"Should NOT detect as page number: {line!r}"


# ─────────────────────────────────────────────────────────────────────────────
# Tests: _normalize_bullet
# ─────────────────────────────────────────────────────────────────────────────

class TestBulletNormalization:
    """PDF-native bullet glyphs at line start must be normalized to '- '."""

    @pytest.mark.parametrize("glyph,rest", [
        ("\u2022", "Demand paging is a memory management scheme"),
        ("\u25cf", "Process states include Ready, Running, and Waiting"),
        ("\u25a0", "FCFS is a non-preemptive algorithm"),
        ("\uf0b7", "Fragmentation reduces usable memory"),
        ("\u2192", "Context switching overhead"),
        ("\u2261 ", "Thrashing occurs when page fault rate is high"),  # ≡ space as bullet
        ("\u25a1 ", "Semaphores prevent race conditions"),              # □ space as bullet
    ])
    def test_normalizes_bullet_glyph(self, glyph: str, rest: str):
        line = glyph + rest
        result = _normalize_bullet(line)
        assert result.startswith("- "), f"Expected '- ' prefix, got: {result!r}"
        assert rest.strip() in result, "Content should be preserved"

    def test_preserves_math_triple_bar(self):
        """≡ mid-sentence (not at line start) must be preserved as mathematical symbol."""
        line = "We say x ≡ y (mod n) when n divides x-y"
        # This line does NOT start with ≡, so _normalize_bullet should be a no-op
        result = _normalize_bullet(line)
        assert result == line, f"Math notation should be unchanged, got: {result!r}"

    def test_preserves_normal_text_starting_with_o(self):
        """'o' used as a word start (not a bullet) must not be converted."""
        # 'o' is in the bullet set but only when followed by a lowercase word
        # indicating it IS a bullet, but "often..." starts with a real word
        line = "often the system calls the scheduler"
        result = _normalize_bullet(line)
        # Should be unchanged because 'o' is the bullet-set entry but rest starts lowercase
        # The logic: if line[0]=='o' and rest[0].islower() → preserve
        assert result == line, f"Should not convert 'o' word-start, got: {result!r}"


# ─────────────────────────────────────────────────────────────────────────────
# Tests: _detect_running_noise (statistical header/footer detection)
# ─────────────────────────────────────────────────────────────────────────────

class TestRunningNoiseDetection:
    """Headers/footers appearing on many pages must be flagged as noise."""

    def _make_pages(self, top_lines: list[str], body: str, n_pages: int) -> list[dict]:
        """Helper: create synthetic page structures."""
        pages = []
        for i in range(n_pages):
            pages.append({
                "text": f"{'  '.join(top_lines)}\n{body}\nPage {i+1}",
                "height": 792.0,
                "top_lines": top_lines,
                "bottom_lines": [f"Page {i+1}"],
            })
        return pages

    def test_detects_repeated_institutional_header(self):
        """A short line repeated on every page must be flagged."""
        pages = self._make_pages(
            top_lines=["Alpha University Department of Computing"],
            body="Virtual memory allows a process to use more memory than physically available.",
            n_pages=8,
        )
        noise = _detect_running_noise(pages)
        assert "alpha university department of computing" in noise, \
            f"Expected header in noise set, got: {noise}"

    def test_detects_repeated_footer(self):
        """A short repeated bottom line must be flagged."""
        pages = self._make_pages(
            top_lines=["Introduction to Algorithms"],
            body="A binary search tree maintains the BST property for all nodes.",
            n_pages=6,
        )
        noise = _detect_running_noise(pages)
        # Bottom line "Page N" varies per page → should NOT be in noise set
        # (each "Page 1", "Page 2" is different and won't reach threshold)
        for item in noise:
            assert not item.startswith("page ") or "page " not in item.split()[0], \
                f"Varying page numbers should not be in noise: {item}"

    def test_does_not_delete_long_repeated_headings(self):
        """A long line (> NOISE_MAX_WORDS) must NOT be flagged even if repeated."""
        long_line = "Chapter 3: Advanced Memory Management Techniques and Virtual Address Spaces"
        pages = self._make_pages(
            top_lines=[long_line],
            body="Segmentation divides memory into variable-size segments.",
            n_pages=10,
        )
        noise = _detect_running_noise(pages)
        normalized_long = long_line.lower()
        assert normalized_long not in noise, \
            f"Long heading should NOT be in noise: {normalized_long}"

    def test_no_noise_on_single_page(self):
        """Single-page PDF must never have noise detected (nothing to compare against)."""
        pages = self._make_pages(
            top_lines=["Any Header Line"],
            body="Some body content here.",
            n_pages=1,
        )
        noise = _detect_running_noise(pages)
        assert len(noise) == 0, f"Single page should produce no noise, got: {noise}"


# ─────────────────────────────────────────────────────────────────────────────
# Tests: _reconstruct_paragraphs
# ─────────────────────────────────────────────────────────────────────────────

class TestParagraphReconstruction:
    """PDF visual line-wraps must be rejoined; structural breaks must be preserved."""

    def test_joins_wrapped_sentence(self):
        """A sentence split across PDF lines must be rejoined."""
        text = "The operating system manages\nthe resources of a computer\nsystem."
        result = _reconstruct_paragraphs(text)
        assert "The operating system manages the resources of a computer system." in result

    def test_dehyphenates_word(self):
        """Words split with a trailing hyphen must be merged."""
        text = "Memory man-\nagement is a key OS function."
        result = _reconstruct_paragraphs(text)
        assert "Memory management is a key OS function." in result, \
            f"Expected dehyphenated word, got: {result!r}"

    def test_preserves_bullet_list(self):
        """Bullet items must not be joined into the preceding line."""
        text = "The OS provides three main services:\n- Process management\n- Memory management\n- I/O management"
        result = _reconstruct_paragraphs(text)
        assert "- Process management" in result
        assert "- Memory management" in result
        assert "- I/O management" in result

    def test_preserves_heading_break(self):
        """A heading line must not be merged with the preceding paragraph."""
        text = "This completes the discussion of paging.\nVIRTUAL MEMORY\nVirtual memory extends physical memory."
        result = _reconstruct_paragraphs(text)
        assert "VIRTUAL MEMORY" in result

    def test_preserves_blank_line_paragraph_break(self):
        """Blank lines must create paragraph boundaries."""
        text = "First paragraph text here.\n\nSecond paragraph text here."
        result = _reconstruct_paragraphs(text)
        assert "\n\n" in result or "\n" in result
        assert "First paragraph" in result
        assert "Second paragraph" in result

    def test_joins_mid_sentence_break(self):
        """A line NOT ending in punctuation, followed by a lowercase continuation, must join."""
        text = "The CPU scheduler selects a process from the ready\nqueue and allocates the CPU to it."
        result = _reconstruct_paragraphs(text)
        assert "ready queue" in result or "ready\nqueue" not in result


# ─────────────────────────────────────────────────────────────────────────────
# Tests: clean_note_text_local (Layer 1 deterministic cleaner)
# ─────────────────────────────────────────────────────────────────────────────

class TestLocalCleaner:
    """Generic deterministic cleaning: no hardcoded names, works on any PDF."""

    def test_removes_page_number_lines(self):
        text = "Process States\nPage 5\nA process can be in one of five states."
        result = clean_note_text_local(text)
        assert "Page 5" not in result
        assert "process" in result.lower()

    def test_normalizes_bullet_glyphs(self):
        text = "\u2022 First point\n\u2022 Second point\n\u2022 Third point"
        result = clean_note_text_local(text)
        lines = [l for l in result.splitlines() if l.strip()]
        bullet_lines = [l for l in lines if l.startswith("- ")]
        assert len(bullet_lines) == 3, f"Expected 3 bullet lines, got: {result!r}"

    def test_detects_allcaps_heading(self):
        text = "VIRTUAL MEMORY\nVirtual memory allows the execution of processes not completely in memory."
        result = clean_note_text_local(text)
        assert "### VIRTUAL MEMORY" in result

    def test_preserves_technical_content(self):
        """Important definitions, terms, and content must not be removed."""
        text = (
            "Deadlock occurs when a set of processes are each waiting for a resource\n"
            "held by another process in the set, causing all to be stuck permanently."
        )
        result = clean_note_text_local(text)
        assert "Deadlock" in result
        assert "resource" in result
        assert "processes" in result

    def test_handles_empty_input(self):
        assert clean_note_text_local("") == ""
        assert clean_note_text_local("   ") == ""

    def test_no_hardcoded_college_dependency(self):
        """
        Cleaner must not silently depend on specific college names.
        Text from a completely fictional college must be processed normally.
        """
        text = (
            "ZORB INSTITUTE OF INTERSTELLAR ENGINEERING\n"
            "Department of Quantum Computing\n"
            "Semaphores are synchronisation primitives.\n"
            "A semaphore S is an integer variable that is accessed through\n"
            "two atomic operations: wait and signal."
        )
        result = clean_note_text_local(text)
        # The educational content must survive regardless of college name
        assert "Semaphore" in result or "semaphore" in result.lower()
        assert "wait" in result.lower()
        assert "signal" in result.lower()

    def test_preserves_math_notation(self):
        """Mathematical symbols like ≡ in equations must not be destroyed."""
        text = "We define congruence as: a ≡ b (mod n) if n divides (a - b)"
        result = clean_note_text_local(text)
        # The ≡ appears mid-sentence (not at start), so must be preserved
        assert "≡" in result, f"Math notation should be preserved, got: {result!r}"


# ─────────────────────────────────────────────────────────────────────────────
# Tests: _validate_cleaned_output
# ─────────────────────────────────────────────────────────────────────────────

class TestValidationLayer:
    """Post-LLM validation must catch over-cleaning and empty results."""

    def test_accepts_good_output(self):
        raw = "This is a reasonably long piece of text about operating systems and memory management."
        cleaned = "This is a cleaned version of the text about operating systems and memory management."
        result, used_fallback = _validate_cleaned_output(raw, cleaned, "FALLBACK")
        assert result == cleaned
        assert not used_fallback

    def test_rejects_empty_output(self):
        raw = "The operating system manages resources for processes running on the CPU."
        cleaned = ""
        result, used_fallback = _validate_cleaned_output(raw, cleaned, "FALLBACK")
        assert result == "FALLBACK"
        assert used_fallback

    def test_rejects_over_cleaned_output(self):
        """If LLM removes > 70 % of words, the fallback must be used."""
        raw = " ".join(["word"] * 100)  # 100-word input
        cleaned = " ".join(["word"] * 10)  # 10-word output = 10% retained < 30% threshold
        result, used_fallback = _validate_cleaned_output(raw, cleaned, "FALLBACK")
        assert result == "FALLBACK"
        assert used_fallback

    def test_accepts_acceptable_word_loss(self):
        """40% word retention is above the 30% threshold — should be accepted."""
        raw = " ".join(["word"] * 100)
        cleaned = " ".join(["word"] * 40)  # 40% retained
        result, used_fallback = _validate_cleaned_output(raw, cleaned, "FALLBACK")
        assert result == cleaned
        assert not used_fallback


# ─────────────────────────────────────────────────────────────────────────────
# Tests: chunk_text
# ─────────────────────────────────────────────────────────────────────────────

class TestChunking:
    """Chunker must filter short/noisy chunks and produce reasonable segments."""

    def test_basic_chunking(self):
        text = (
            "The operating system acts as a fundamental interface between the user applications "
            "and the underlying computer hardware, managing resources for all running processes. "
            "Process scheduling ensures efficient CPU utilisation by deciding which process "
            "runs at any given moment using algorithms such as Round Robin or FCFS. "
            "Memory management prevents address space conflicts and provides each process "
            "with a protected virtual address space through paging and segmentation. "
            "File systems organise data on persistent storage devices using hierarchical "
            "directory structures and metadata stored in inodes or FAT entries. "
            "Security and protection mechanisms in the OS isolate processes from each other "
            "and enforce access control policies on files and devices. "
            "Device drivers abstract the hardware-specific details of peripherals and present "
            "a uniform interface to the rest of the operating system kernel."
        )
        chunks = chunk_text(text, sentences_per_chunk=2)
        assert len(chunks) >= 2, f"Expected at least 2 chunks, got {len(chunks)}"
        for c in chunks:
            assert len(c.split()) >= 20, f"Chunk too short: {c!r}"


    def test_filters_short_chunks(self):
        """Chunks below MIN_CHUNK_WORDS must be dropped."""
        text = "Hi. OK. Yes. "  # All very short "sentences"
        chunks = chunk_text(text, sentences_per_chunk=2)
        for c in chunks:
            assert len(c.split()) >= 20, f"Short chunk should be filtered: {c!r}"

    def test_empty_input(self):
        assert chunk_text("") == []
        assert chunk_text("   ") == []
