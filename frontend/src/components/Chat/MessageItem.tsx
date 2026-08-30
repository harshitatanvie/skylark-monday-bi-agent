import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { ChatMessage } from '../../types';
import { KPICard } from '../Dashboard/KPICard';
import { AnalyticsChart } from '../Dashboard/AnalyticsChart';
import { Bot, User, Copy, Check, AlertTriangle, ArrowRight, HelpCircle } from 'lucide-react';

interface Props {
  message: ChatMessage;
  onSendPrompt: (prompt: string) => void;
  onOpenDataQualityDrawer: () => void;
}

export const MessageItem: React.FC<Props> = ({ message, onSendPrompt, onOpenDataQualityDrawer }) => {
  const [copied, setCopied] = useState(false);
  const isAI = message.sender === 'ai';
  const data = message.response_data;

  const handleCopy = () => {
    if (!data?.answer_markdown) return;
    navigator.clipboard.writeText(data.answer_markdown);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={`flex gap-3 my-4 ${isAI ? 'justify-start' : 'justify-end'}`}>
      {isAI && (
        <div className="w-8 h-8 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 shrink-0 mt-1 shadow-md">
          <Bot className="w-4 h-4" />
        </div>
      )}

      <div className={`max-w-3xl flex flex-col ${isAI ? 'items-start' : 'items-end'}`}>
        <div
          className={`rounded-2xl p-5 shadow-lg border ${
            isAI
              ? 'bg-slate-900/90 border-slate-800 text-slate-100'
              : 'bg-gradient-to-r from-cyan-600 to-blue-600 border-cyan-500/40 text-white font-medium'
          }`}
        >
          {/* User Message Text */}
          {!isAI && <p className="text-sm whitespace-pre-wrap">{message.text}</p>}

          {/* AI Markdown Content */}
          {isAI && (
            <div className="prose-dark font-sans text-sm">
              <ReactMarkdown>{data?.answer_markdown || message.text}</ReactMarkdown>
            </div>
          )}

          {/* KPI Cards Grid */}
          {isAI && data?.kpi_cards && data.kpi_cards.length > 0 && (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 my-4">
              {data.kpi_cards.map((card, i) => (
                <KPICard key={i} card={card} />
              ))}
            </div>
          )}

          {/* Visual Charts */}
          {isAI && data?.charts && data.charts.length > 0 && (
            <div className="space-y-4 my-4">
              {data.charts.map((chart, i) => (
                <AnalyticsChart key={i} chart={chart} />
              ))}
            </div>
          )}

          {/* Data Quality Warning Alert */}
          {isAI && data?.data_quality_warning && (
            <div
              onClick={onOpenDataQualityDrawer}
              className="my-3 p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-between text-xs text-amber-300 hover:bg-amber-500/20 cursor-pointer transition"
            >
              <div className="flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
                <span>{data.data_quality_warning}</span>
              </div>
              <span className="underline font-semibold shrink-0 ml-2">Inspect DQ</span>
            </div>
          )}

          {/* Ambiguous Clarification Options */}
          {isAI && data?.clarification_needed && data.clarification_options && (
            <div className="my-4 p-4 rounded-xl bg-slate-950/80 border border-cyan-500/30">
              <h4 className="text-xs font-semibold text-cyan-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <HelpCircle className="w-4 h-4" /> Please select an option to narrow down:
              </h4>
              <div className="flex flex-col gap-2 mt-2">
                {data.clarification_options.map((opt, i) => (
                  <button
                    key={i}
                    onClick={() => onSendPrompt(opt)}
                    className="py-2 px-3 bg-slate-900 hover:bg-slate-800 text-left border border-slate-700 hover:border-cyan-500/50 rounded-lg text-xs font-medium text-slate-200 hover:text-cyan-300 transition flex items-center justify-between group"
                  >
                    <span>{opt}</span>
                    <ArrowRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-cyan-400 transition" />
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Footer Metadata & Actions */}
          {isAI && (
            <div className="flex items-center justify-between pt-3 mt-3 border-t border-slate-800/80 text-xs text-slate-400">
              <span className="text-[11px] text-slate-400">
                Data Grounding: Monday.com API ({data?.is_demo_mode ? 'Demo Mode' : 'Production GraphQL'})
              </span>
              <button
                onClick={handleCopy}
                className="flex items-center gap-1 hover:text-slate-200 transition px-2 py-1 rounded bg-slate-800/50"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? 'Copied' : 'Copy'}</span>
              </button>
            </div>
          )}
        </div>

        {/* Suggested Contextual Follow-up Chips */}
        {isAI && data?.suggested_followups && data.suggested_followups.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-2">
            {data.suggested_followups.map((chip, i) => (
              <button
                key={i}
                onClick={() => onSendPrompt(chip)}
                className="py-1 px-2.5 bg-slate-900/80 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 rounded-full text-xs text-slate-300 hover:text-cyan-300 transition flex items-center gap-1.5"
              >
                <span>{chip}</span>
                <ArrowRight className="w-3 h-3 text-slate-400" />
              </button>
            ))}
          </div>
        )}
      </div>

      {!isAI && (
        <div className="w-8 h-8 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300 shrink-0 mt-1 shadow-md">
          <User className="w-4 h-4" />
        </div>
      )}
    </div>
  );
};
