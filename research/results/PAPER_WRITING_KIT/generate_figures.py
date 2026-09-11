# -*- coding: utf-8 -*-
"""generate_figures.py
Creates the five required PNG figures for the CampusClimb paper using data from
MASTER_RESULTS.csv. All numbers are taken directly from the CSV and formatted
to match the values shown in RESULTS_TABLES.md (two‑decimal percentages).
The figures are saved at 300 DPI in the FIGURES/ folder.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Paths (relative to script location)
CSV_PATH = r"c:/Users/rahul/Downloads/CampusClimb/evaluation/output/MASTER_RESULTS.csv"
ARTIFACT_ROOT = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(ARTIFACT_ROOT, "FIGURES")
os.makedirs(FIG_DIR, exist_ok=True)

# Load CSV with explicit column names
cols = ["section", "configuration", "model_variant", "top1_accuracy", "top1_correct", "top1_total",
        "top3_accuracy", "top3_correct", "ci_95_low", "ci_95_high", "macro_f1", "coverage", "accuracy_on_covered",
        "p_value", "chi2_statistic", "notes"]

df = pd.read_csv(CSV_PATH, header=0, names=cols)

# Helper to format percentages for annotations (two decimals)
pct = lambda x: f"{x*100:.2f}%"

# Set plot style/aesthetics for premium feel
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#BDC3C7'
plt.rcParams['axes.linewidth'] = 0.8

# ---------------------------------------------------------------------------
# Figure 1: Baseline Top‑1 Accuracy with 95% CI error bars
# ---------------------------------------------------------------------------
baseline = df[df['section'].str.startswith('A.')].copy()
methods = baseline['configuration'].tolist()
top1 = baseline['top1_accuracy'].tolist()
ci_low = baseline['ci_95_low'].tolist()
ci_high = baseline['ci_95_high'].tolist()

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(methods, top1, color="#2E86C1", alpha=0.9, edgecolor='#2471A3')

# error bars (CI width)
ci_err_low = [t - l if not pd.isna(l) else 0 for t, l in zip(top1, ci_low)]
ci_err_high = [h - t if not pd.isna(h) else 0 for t, h in zip(top1, ci_high)]
ax.errorbar(methods, top1, yerr=[ci_err_low, ci_err_high], fmt='none', ecolor='#1A252C', capsize=4, elinewidth=1.5)

ax.set_ylabel('Top‑1 Accuracy', fontsize=11, fontweight='bold', labelpad=10)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=2))
ax.set_xticks(range(len(methods)))
ax.set_xticklabels(methods, rotation=35, ha='right', fontsize=9)
ax.set_title('Baseline Top‑1 Accuracy with 95% CI', fontsize=13, fontweight='bold', pad=15)
ax.grid(axis='y', linestyle='--', alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'fig1_baseline_comparison_barchart.png'), dpi=300)
plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 2: Component ablation waterfall (Δ Top‑1)
# ---------------------------------------------------------------------------
ablation = df[df['section'].str.startswith('C.')].reset_index(drop=True)
stages = ablation['configuration'].tolist()
acc = ablation['top1_accuracy']
prev = acc.shift(1).fillna(acc.iloc[0])
# Δ expressed in percentage‑points (two decimals)
delta = ((acc - prev) * 100).tolist()

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(stages, delta, color="#A93226", alpha=0.9, edgecolor='#7B241C')
ax.axhline(0, color='#5D6D7E', linewidth=1)

for rect, d in zip(bars, delta):
    height = rect.get_height()
    # Add text label above or below the bar
    va_dir = 'bottom' if height >= 0 else 'top'
    offset = 0.5 if height >= 0 else -0.5
    ax.text(rect.get_x() + rect.get_width()/2, height + offset, f"{d:+.2f}pp", ha='center', va=va_dir, fontsize=9, fontweight='bold')

ax.set_ylabel('Δ Top‑1 Accuracy (pp)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_xticks(range(len(stages)))
ax.set_xticklabels(stages, rotation=35, ha='right', fontsize=9)
ax.set_title('Component Ablation Δ Top‑1 Accuracy', fontsize=13, fontweight='bold', pad=15)
ax.grid(axis='y', linestyle='--', alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'fig2_component_ablation_waterfall.png'), dpi=300)
plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 3: LOSO per‑subject vs. in‑domain baseline
# ---------------------------------------------------------------------------
loso = df[(df['section'].str.startswith('B.')) & (~df['configuration'].str.contains('Aggregate'))].copy()

def map_subject(config):
    if "Operating Systems" in config:
        return "OS"
    elif "Computer Networks" in config:
        return "CN"
    elif "DBMS" in config:
        return "DBMS"
    return config

subjects = loso['configuration'].apply(map_subject).tolist()
loso_acc = loso['top1_accuracy'].tolist()

# Find the Headline In-domain FT Hybrid accuracy
baseline_row = df[(df['section'].str.startswith('A.')) & (df['configuration'].str.contains('FT Hybrid', regex=False)) & (~df['configuration'].str.contains('Gated'))]
baseline_val = baseline_row['top1_accuracy'].iloc[0]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(subjects, loso_acc, color="#1B4F72", alpha=0.9, edgecolor='#113F5C', width=0.5)
ax.axhline(baseline_val, color='#D35400', linestyle='--', linewidth=2, label=f'In‑domain FT Hybrid ({pct(baseline_val)})')

# Add values above the bars
for rect, v in zip(bars, loso_acc):
    ax.text(rect.get_x() + rect.get_width()/2, v + 0.01, pct(v), ha='center', va='bottom', fontweight='bold')

ax.set_ylabel('Top‑1 Accuracy', fontsize=11, fontweight='bold', labelpad=10)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=2))
ax.set_xticks(range(len(subjects)))
ax.set_xticklabels(subjects, fontsize=10, fontweight='bold')
ax.set_title('LOSO Top‑1 Accuracy per Subject vs. In-Domain Baseline', fontsize=13, fontweight='bold', pad=15)
ax.set_ylim(0, 0.8)
ax.legend(loc='upper right')
ax.grid(axis='y', linestyle='--', alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'fig3_loso_per_subject.png'), dpi=300)
plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 4: Coverage vs. Accuracy‑on‑Covered
# ---------------------------------------------------------------------------
cov_row = df[(df['section'].str.startswith('D.')) & (df['configuration']=='Coverage (chunks mapped)')].iloc[0]
coverage = cov_row['top1_correct'] / cov_row['top1_total']  # 210/229 = 0.9170
acc_covered = df[(df['section'].str.startswith('D.')) & (df['configuration']=='Accuracy on Covered')]['top1_accuracy'].iloc[0]

fig, ax = plt.subplots(figsize=(6, 5))
bars = ax.bar(['Coverage', 'Accuracy‑on‑Covered'], [coverage, acc_covered], color=['#117A65', '#D68910'], alpha=0.9, width=0.5)

ax.set_ylabel('Percentage', fontsize=11, fontweight='bold', labelpad=10)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=2))
ax.set_title('Gated Model Abstention-Aware Trade‑off', fontsize=13, fontweight='bold', pad=15)
ax.set_ylim(0, 1.15)

for rect, v in zip(bars, [coverage, acc_covered]):
    ax.text(rect.get_x() + rect.get_width()/2, v + 0.02, pct(v), ha='center', va='bottom', fontweight='bold', fontsize=10)

ax.grid(axis='y', linestyle='--', alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'fig4_precision_recall_tradeoff.png'), dpi=300)
plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 5: Error category breakdown (hard‑coded counts from error_analysis.md)
# ---------------------------------------------------------------------------
categories = ['Near‑miss', 'Cross‑subject', 'Ambiguous']
counts = [6, 6, 6]  # verified from error_analysis.md

fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(categories, counts, color=['#7D3C98', '#2471A3', '#CA6F1E'], alpha=0.9, width=0.5)

ax.set_ylabel('Number of Samples', fontsize=11, fontweight='bold', labelpad=10)
ax.set_title('Error Category Breakdown (Manual Analysis)', fontsize=13, fontweight='bold', pad=15)
ax.set_ylim(0, 8.0)

for rect, cnt in zip(bars, counts):
    ax.text(rect.get_x() + rect.get_width()/2, cnt + 0.15, str(cnt), ha='center', va='bottom', fontweight='bold', fontsize=10)

ax.grid(axis='y', linestyle='--', alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'fig5_confusion_matrix_or_error_breakdown.png'), dpi=300)
plt.close(fig)

print('All 5 figures successfully generated and saved to:', FIG_DIR)
