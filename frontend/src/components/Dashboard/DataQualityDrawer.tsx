import React from 'react';
import { DataQualityReport } from '../../types';
import { ShieldAlert, ShieldCheck, X, AlertTriangle, Database, CheckCircle2 } from 'lucide-react';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  report?: DataQualityReport | null;
}

export const DataQualityDrawer: React.FC<Props> = ({ isOpen, onClose, report }) => {
  if (!isOpen) return null;

  const score = report?.overall_health_score_pct ?? 100;
  const getScoreColor = () => {
    if (score >= 90) return 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10';
    if (score >= 70) return 'text-amber-400 border-amber-500/30 bg-amber-500/10';
    return 'text-rose-400 border-rose-500/30 bg-rose-500/10';
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-slate-950/70 backdrop-blur-sm flex justify-end">
      <div className="w-full max-w-md bg-slate-900 border-l border-slate-800 h-full p-6 overflow-y-auto flex flex-col justify-between shadow-2xl animate-in slide-in-from-right duration-200">
        <div>
          <div className="flex items-center justify-between pb-4 border-b border-slate-800">
            <div className="flex items-center gap-2">
              <Database className="w-5 h-5 text-cyan-400" />
              <h3 className="text-lg font-bold text-slate-100">Data Quality & Governance</h3>
            </div>
            <button
              onClick={onClose}
              className="p-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800 transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Health Score Badge */}
          <div className="my-6 p-4 rounded-xl border flex items-center justify-between glass-panel">
            <div>
              <span className="text-xs uppercase font-medium tracking-wider text-slate-400">Data Health Index</span>
              <div className="text-3xl font-extrabold text-slate-100 mt-1">
                {score}% <span className="text-xs font-normal text-slate-400">Completeness</span>
              </div>
            </div>
            <div className={`p-3 rounded-xl border ${getScoreColor()}`}>
              {score >= 80 ? <ShieldCheck className="w-8 h-8" /> : <ShieldAlert className="w-8 h-8" />}
            </div>
          </div>

          {report && (
            <div className="space-y-6">
              {/* Summary Stats */}
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800">
                  <span className="text-xs text-slate-400">Records Analyzed</span>
                  <div className="text-lg font-bold text-slate-200 mt-0.5">{report.total_records_analyzed}</div>
                </div>
                <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800">
                  <span className="text-xs text-slate-400">Last Fetched</span>
                  <div className="text-xs font-medium text-slate-300 mt-1">{report.last_fetched_timestamp || 'Just now'}</div>
                </div>
              </div>

              {/* Deals Board Metrics */}
              <div className="bg-slate-950/40 border border-slate-800 rounded-xl p-4">
                <h4 className="text-sm font-semibold text-slate-200 mb-3 flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-cyan-400"></span>
                  Deals Board Quality
                </h4>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between py-1 border-b border-slate-800/60">
                    <span className="text-slate-400">Total Deals:</span>
                    <span className="font-semibold text-slate-200">{report.deals_quality.total_records}</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-slate-800/60">
                    <span className="text-slate-400">Missing Expected Close Dates:</span>
                    <span className={report.deals_quality.missing_dates_count > 0 ? 'text-amber-400 font-semibold' : 'text-slate-200'}>
                      {report.deals_quality.missing_dates_count}
                    </span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-slate-800/60">
                    <span className="text-slate-400">Missing Deal Amount Values:</span>
                    <span className={report.deals_quality.missing_amounts_count > 0 ? 'text-amber-400 font-semibold' : 'text-slate-200'}>
                      {report.deals_quality.missing_amounts_count}
                    </span>
                  </div>
                </div>
              </div>

              {/* Work Orders Board Metrics */}
              <div className="bg-slate-950/40 border border-slate-800 rounded-xl p-4">
                <h4 className="text-sm font-semibold text-slate-200 mb-3 flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                  Work Orders Board Quality
                </h4>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between py-1 border-b border-slate-800/60">
                    <span className="text-slate-400">Total Work Orders:</span>
                    <span className="font-semibold text-slate-200">{report.work_orders_quality.total_records}</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-slate-800/60">
                    <span className="text-slate-400">Missing Target Dates:</span>
                    <span className={report.work_orders_quality.missing_dates_count > 0 ? 'text-amber-400 font-semibold' : 'text-slate-200'}>
                      {report.work_orders_quality.missing_dates_count}
                    </span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-slate-800/60">
                    <span className="text-slate-400">Missing Status Metadata:</span>
                    <span className={report.work_orders_quality.missing_status_count > 0 ? 'text-amber-400 font-semibold' : 'text-slate-200'}>
                      {report.work_orders_quality.missing_status_count}
                    </span>
                  </div>
                </div>
              </div>

              {/* Global Warnings List */}
              {report.global_warnings && report.global_warnings.length > 0 && (
                <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-4">
                  <h4 className="text-xs font-semibold text-amber-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                    <AlertTriangle className="w-4 h-4" /> Data Quality Warnings
                  </h4>
                  <ul className="space-y-1.5 text-xs text-amber-200/90 list-disc list-inside">
                    {report.global_warnings.map((warn, i) => (
                      <li key={i}>{warn}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        <div className="pt-4 border-t border-slate-800 text-center">
          <button
            onClick={onClose}
            className="w-full py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium text-xs rounded-lg transition"
          >
            Close Data Quality Panel
          </button>
        </div>
      </div>
    </div>
  );
};
