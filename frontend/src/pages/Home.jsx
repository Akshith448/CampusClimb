import React from 'react';
import Navbar from '../components/Navbar';
import HeroSection from '../components/HeroSection';
import ProblemSolution from '../components/ProblemSolution';
import HowItWorks from '../components/HowItWorks';
import LiveStatsSection from '../components/LiveStatsSection';
import TechCredibility from '../components/TechCredibility';
import CtaBanner from '../components/CtaBanner';
import Footer from '../components/Footer';

export default function Home({ theme, toggleTheme }) {
  return (
    <div className="min-h-screen bg-[#0a0a0a] dark:bg-[#0a0a0a] light:bg-neutral-100 text-neutral-100 dark:text-neutral-100 light:text-neutral-900 flex flex-col selection:bg-teal-600 selection:text-white transition-colors duration-200">
      <Navbar theme={theme} toggleTheme={toggleTheme} />
      <main className="flex-grow">
        <HeroSection />
        <ProblemSolution />
        <HowItWorks />
        <LiveStatsSection />
        <TechCredibility />
        <CtaBanner />
      </main>
      <Footer />
    </div>
  );
}
