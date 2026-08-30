import React, { useState, useEffect } from 'react';
import { Loader2, Search, Database, Calculator, Sparkles } from 'lucide-react';

const STEPS = [
  { text: "Understanding business query intent...", icon: Search },
  { text: "Fetching dynamic data from Monday.com boards...", icon: Database },
  { text: "Normalizing messy records & calculating metrics...", icon: Calculator },
  { text: "Synthesizing founder insights...", icon: Sparkles }
];

export const LoadingSteps: React.FC = () => {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentStepIndex((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev));
    }, 700);

    return () => clearInterval(timer);
  }, []);

  const StepIcon = STEPS[currentStepIndex].icon;

  return (
    <div className="flex items-start gap-3 my-4 bg-slate-900/90 border border-cyan-500/30 rounded-xl p-4 max-w-md shadow-xl animate-pulse">
      <div className="p-2 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
        <Loader2 className="w-5 h-5 animate-spin" />
      </div>
      <div>
        <div className="flex items-center gap-2">
          <StepIcon className="w-4 h-4 text-cyan-400" />
          <span className="text-xs font-semibold uppercase tracking-wider text-cyan-400">
            Step {currentStepIndex + 1} of {STEPS.length}
          </span>
        </div>
        <p className="text-xs font-medium text-slate-200 mt-1">
          {STEPS[currentStepIndex].text}
        </p>
      </div>
    </div>
  );
};
