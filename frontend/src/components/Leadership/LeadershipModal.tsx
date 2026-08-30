import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { LeadershipUpdateData } from '../../types';
import { fetchLeadershipUpdate } from '../../services/api';
import { X, Copy, Check, FileText, Loader2, Sparkles } from 'lucide-react';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  isDemoMode: boolean;
}

export const LeadershipModal: React.FC<Props> = ({ isOpen, onClose, isDemoMode }) => {
  const [data, setData] = useState<LeadershipUpdateData | null>(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      fetchLeadershipUpdate(isDemoMode)
        .then((res) => setData(res))
        .catch((err) => console.error("Failed to load leadership update", err))
        .finally(() => setLoading(false));
    }
  }, [isOpen, isDemoMode]);

  if (!isOpen) return null;

  const handleCopy = () => {
    if (!data?.markdown_report) return;
    navigator.clipboard.writeText(data.markdown_report);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-3xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-100">Executive Leadership Update</h3>
              <p className="text-xs text-slate-400">Concise business update synthesized from live Monday.com data</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {data && (
              <button
                onClick={handleCopy}
                className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition flex items-center gap-1.5"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? 'Copied Markdown' : 'Copy Report'}</span>
              </button>
            )}
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800 transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto flex-1">
          {loading ? (
            <div className="py-20 flex flex-col items-center justify-center text-center">
              <Loader2 className="w-8 h-8 text-cyan-400 animate-spin mb-3" />
              <p className="text-sm font-medium text-slate-300">Generating Executive Leadership Report...</p>
              <p className="text-xs text-slate-400 mt-1">Aggregating Deals, Work Orders, and Data Quality statistics</p>
            </div>
          ) : data ? (
            <div className="space-y-6">
              {/* Executive Snapshot Cards */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800">
                  <span className="text-[11px] text-slate-400 uppercase font-semibold">Open Pipeline</span>
                  <div className="text-base font-bold text-slate-100 mt-0.5">{data.executive_snapshot.formatted_open_pipeline}</div>
                </div>
                <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800">
                  <span className="text-[11px] text-slate-400 uppercase font-semibold">Won Revenue</span>
                  <div className="text-base font-bold text-slate-100 mt-0.5">{data.executive_snapshot.formatted_won_revenue}</div>
                </div>
                <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800">
                  <span className="text-[11px] text-slate-400 uppercase font-semibold">Active Projects</span>
                  <div className="text-base font-bold text-slate-100 mt-0.5">{data.executive_snapshot.active_work_orders}</div>
                </div>
                <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800">
                  <span className="text-[11px] text-slate-400 uppercase font-semibold">Delayed Work Orders</span>
                  <div className="text-base font-bold text-rose-400 mt-0.5">{data.executive_snapshot.delayed_work_orders}</div>
                </div>
              </div>

              {/* Full Markdown Report */}
              <div className="prose-dark bg-slate-950/60 p-6 rounded-xl border border-slate-800/80">
                <ReactMarkdown>{data.markdown_report}</ReactMarkdown>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-slate-400">Failed to generate report.</div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-950/60 flex items-center justify-between text-xs text-slate-400">
          <div className="flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            <span>Source of Truth: Monday.com Boards ({isDemoMode ? 'Demo Mode' : 'Production GraphQL'})</span>
          </div>
          <button
            onClick={onClose}
            className="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium rounded-lg transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
