import React from 'react';
import { 
  TrendingUp, 
  PieChart, 
  DollarSign, 
  AlertTriangle, 
  FileText, 
  Grid, 
  HelpCircle,
  ChevronRight,
  Database
} from 'lucide-react';

interface Props {
  onSelectPrompt: (prompt: string) => void;
  onOpenLeadershipModal: () => void;
  onOpenDataQualityDrawer: () => void;
  isOpen: boolean;
  onCloseMobile: () => void;
}

const SAMPLE_QUESTIONS = [
  { icon: TrendingUp, text: "How is our pipeline looking this quarter?" },
  { icon: PieChart, text: "Which sector has the strongest pipeline?" },
  { icon: DollarSign, text: "How much revenue have we won?" },
  { icon: AlertTriangle, text: "Which projects are delayed?" },
  { icon: Grid, text: "Compare pipeline across sectors." },
  { icon: FileText, text: "Give me a leadership update." },
  { icon: HelpCircle, text: "Which deals need attention?" },
];

export const Sidebar: React.FC<Props> = ({
  onSelectPrompt,
  onOpenLeadershipModal,
  onOpenDataQualityDrawer,
  isOpen,
  onCloseMobile
}) => {
  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          onClick={onCloseMobile}
          className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-40 lg:hidden"
        />
      )}

      <aside
        className={`fixed lg:static top-16 bottom-0 left-0 w-64 bg-slate-900 border-r border-slate-800 p-4 flex flex-col justify-between z-40 transition-transform duration-200 ${
          isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div>
          <div className="mb-4">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">
              Suggested Business Queries
            </h3>
            <div className="space-y-1">
              {SAMPLE_QUESTIONS.map((q, idx) => {
                const Icon = q.icon;
                return (
                  <button
                    key={idx}
                    onClick={() => {
                      if (q.text === "Give me a leadership update.") {
                        onOpenLeadershipModal();
                      } else {
                        onSelectPrompt(q.text);
                      }
                      onCloseMobile();
                    }}
                    className="w-full p-2.5 rounded-lg bg-slate-950/50 hover:bg-slate-800 border border-slate-800/80 hover:border-cyan-500/30 text-left text-xs font-medium text-slate-300 hover:text-cyan-300 transition flex items-center justify-between group"
                  >
                    <div className="flex items-center gap-2.5">
                      <Icon className="w-4 h-4 text-slate-400 group-hover:text-cyan-400 shrink-0 transition" />
                      <span className="truncate">{q.text}</span>
                    </div>
                    <ChevronRight className="w-3.5 h-3.5 text-slate-600 group-hover:text-cyan-400 shrink-0 transition" />
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Bottom Card: Grounded Data Notice */}
        <div className="pt-4 border-t border-slate-800">
          <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-xs">
            <div className="flex items-center gap-2 text-cyan-400 font-semibold mb-1">
              <Database className="w-4 h-4" />
              <span>Monday.com Integration</span>
            </div>
            <p className="text-[11px] text-slate-400 leading-relaxed mb-2">
              All analytics read dynamically from Deals & Work Orders boards.
            </p>
            <button
              onClick={() => {
                onOpenDataQualityDrawer();
                onCloseMobile();
              }}
              className="w-full py-1.5 px-2 bg-slate-900 hover:bg-slate-800 border border-slate-700 rounded text-[11px] font-medium text-slate-300 hover:text-slate-100 transition text-center"
            >
              View Data Quality Report
            </button>
          </div>
        </div>
      </aside>
    </>
  );
};
