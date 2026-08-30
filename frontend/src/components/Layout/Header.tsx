import React from 'react';
import { MondayStatusData, DataQualityReport } from '../../types';
import { Sparkles, ShieldCheck, FileText, Settings, Database, Activity } from 'lucide-react';

interface Props {
  mondayStatus: MondayStatusData | null;
  dataQualityReport: DataQualityReport | null;
  onOpenLeadershipModal: () => void;
  onOpenDataQualityDrawer: () => void;
  onOpenConfigModal: () => void;
}

export const Header: React.FC<Props> = ({
  mondayStatus,
  dataQualityReport,
  onOpenLeadershipModal,
  onOpenDataQualityDrawer,
  onOpenConfigModal
}) => {
  const isDemo = mondayStatus?.is_demo_mode ?? true;
  const dqScore = dataQualityReport?.overall_health_score_pct ?? 100;

  return (
    <header className="h-16 bg-slate-900/90 border-b border-slate-800 px-4 sm:px-6 flex items-center justify-between sticky top-0 z-30 backdrop-blur-md">
      {/* Brand & Logo */}
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-600 flex items-center justify-center text-white shadow-lg shadow-cyan-900/30">
          <Sparkles className="w-5 h-5" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-base font-bold text-slate-100 tracking-tight">Skylark Intelligence</h1>
            <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
              Monday.com BI Agent
            </span>
          </div>
          <p className="text-xs text-slate-400 font-normal">Full-Stack Business Intelligence & Cross-Board Analytics</p>
        </div>
      </div>

      {/* Right Controls & Actions */}
      <div className="flex items-center gap-2 sm:gap-3">
        {/* Mode Status Pill */}
        <div
          onClick={onOpenConfigModal}
          className={`cursor-pointer px-2.5 py-1 rounded-full text-xs font-semibold flex items-center gap-1.5 border transition ${
            isDemo
              ? 'bg-amber-500/10 text-amber-300 border-amber-500/30 hover:bg-amber-500/20'
              : 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30 hover:bg-emerald-500/20'
          }`}
        >
          <Activity className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">{isDemo ? 'Demo Mode' : 'Live Monday API'}</span>
        </div>

        {/* Data Quality Button */}
        <button
          onClick={onOpenDataQualityDrawer}
          className="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition flex items-center gap-1.5"
          title="Inspect Data Health & Governance"
        >
          <Database className="w-3.5 h-3.5 text-cyan-400" />
          <span className="hidden md:inline">Data Quality</span>
          <span className="px-1.5 py-0.2 rounded bg-cyan-500/20 text-cyan-300 font-bold text-[10px]">
            {dqScore}%
          </span>
        </button>

        {/* Leadership Update Button */}
        <button
          onClick={onOpenLeadershipModal}
          className="px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-md transition flex items-center gap-1.5"
        >
          <FileText className="w-3.5 h-3.5" />
          <span>Leadership Update</span>
        </button>

        {/* Config Modal Button */}
        <button
          onClick={onOpenConfigModal}
          className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 border border-slate-700 transition"
          title="Monday.com & AI Settings"
        >
          <Settings className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
};
