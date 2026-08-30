import React from 'react';
import { MondayStatusData } from '../../types';
import { X, Settings, CheckCircle2, AlertTriangle, Key, Database, Cpu } from 'lucide-react';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  status: MondayStatusData | null;
  isDemoMode: boolean;
  onToggleDemoMode: (val: boolean) => void;
}

export const ConfigModal: React.FC<Props> = ({
  isOpen,
  onClose,
  status,
  isDemoMode,
  onToggleDemoMode
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-slate-800 text-slate-300">
              <Settings className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-100">Monday.com & AI Settings</h3>
              <p className="text-xs text-slate-400">Connection state & execution mode</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-6 text-xs">
          {/* Demo Mode Toggle Card */}
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
            <div>
              <div className="flex items-center gap-2 font-semibold text-slate-200 text-sm">
                <Cpu className="w-4 h-4 text-cyan-400" />
                <span>Execution Mode</span>
              </div>
              <p className="text-slate-400 text-xs mt-0.5">
                Toggle between out-of-the-box Demo Mode dataset and live Monday GraphQL API.
              </p>
            </div>
            <button
              onClick={() => onToggleDemoMode(!isDemoMode)}
              className={`px-3 py-1.5 rounded-lg font-bold text-xs transition border ${
                isDemoMode
                  ? 'bg-amber-500/20 text-amber-300 border-amber-500/40 hover:bg-amber-500/30'
                  : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40 hover:bg-emerald-500/30'
              }`}
            >
              {isDemoMode ? 'Demo Mode' : 'Live Mode'}
            </button>
          </div>

          {/* Connection Status Details */}
          <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-3">
            <h4 className="font-semibold text-slate-200 text-xs uppercase tracking-wider flex items-center gap-1.5">
              <Database className="w-4 h-4 text-cyan-400" /> Monday.com Board Configuration
            </h4>

            <div className="flex items-center justify-between py-1 border-b border-slate-800">
              <span className="text-slate-400">API Connection Status:</span>
              <span className="flex items-center gap-1 font-semibold text-slate-200">
                {status?.connected ? (
                  <>
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span className="text-emerald-400">Connected</span>
                  </>
                ) : (
                  <>
                    <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
                    <span className="text-amber-400">Demo Fixture Active</span>
                  </>
                )}
              </span>
            </div>

            <div className="flex items-center justify-between py-1 border-b border-slate-800">
              <span className="text-slate-400">Deals Board ID:</span>
              <span className="font-mono text-slate-300">{status?.deals_board_id || 'Not Set'}</span>
            </div>

            <div className="flex items-center justify-between py-1 border-b border-slate-800">
              <span className="text-slate-400">Work Orders Board ID:</span>
              <span className="font-mono text-slate-300">{status?.work_orders_board_id || 'Not Set'}</span>
            </div>
          </div>

          {/* Security Note */}
          <div className="p-3 rounded-lg bg-slate-800/40 border border-slate-800 text-[11px] text-slate-400 flex items-start gap-2">
            <Key className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
            <span>
              API keys are stored securely on the backend server using environment variables (`.env`). Secrets are never exposed to the frontend browser context.
            </span>
          </div>
        </div>

        <div className="p-4 border-t border-slate-800 bg-slate-950/60 text-right">
          <button
            onClick={onClose}
            className="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg transition"
          >
            Close Settings
          </button>
        </div>
      </div>
    </div>
  );
};
