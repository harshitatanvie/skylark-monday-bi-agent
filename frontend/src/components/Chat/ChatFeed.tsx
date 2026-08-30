import React, { useState, useRef, useEffect } from 'react';
import { ChatMessage } from '../../types';
import { MessageItem } from './MessageItem';
import { LoadingSteps } from './LoadingSteps';
import { Send, Trash2, Sparkles, TrendingUp, AlertTriangle, PieChart, Briefcase } from 'lucide-react';

interface Props {
  messages: ChatMessage[];
  isLoading: boolean;
  onSendMessage: (msg: string) => void;
  onClearChat: () => void;
  onOpenDataQualityDrawer: () => void;
}

const SUGGESTED_PROMPTS = [
  {
    icon: TrendingUp,
    title: "Quarterly Pipeline",
    desc: "How is our pipeline looking for this quarter?",
    prompt: "How is our pipeline looking for this quarter?"
  },
  {
    icon: PieChart,
    title: "Sector Strength",
    desc: "Which sector has the strongest pipeline?",
    prompt: "Which sector has the strongest pipeline?"
  },
  {
    icon: Briefcase,
    title: "Won Revenue",
    desc: "How much revenue have we won to date?",
    prompt: "How much revenue have we won to date?"
  },
  {
    icon: AlertTriangle,
    title: "Operational Bottlenecks",
    desc: "Which work order projects are currently delayed?",
    prompt: "Which work order projects are currently delayed?"
  }
];

export const ChatFeed: React.FC<Props> = ({
  messages,
  isLoading,
  onSendMessage,
  onClearChat,
  onOpenDataQualityDrawer
}) => {
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim() || isLoading) return;
    onSendMessage(inputText);
    setInputText('');
  };

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden bg-slate-950">
      {/* Scrollable Message Feed */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center max-w-2xl mx-auto text-center py-8">
            <div className="w-14 h-14 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 mb-4 shadow-xl">
              <Sparkles className="w-7 h-7" />
            </div>
            <h2 className="text-2xl font-extrabold text-slate-100 tracking-tight mb-2">
              Monday.com Business Intelligence Agent
            </h2>
            <p className="text-slate-400 text-sm max-w-md mb-8">
              Ask natural-language business questions about your <span className="text-cyan-400 font-semibold">Deals</span> and <span className="text-emerald-400 font-semibold">Work Orders</span> boards. Powered by zero-hallucination deterministic analytics & data normalization.
            </p>

            {/* Prompt Cards Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full text-left">
              {SUGGESTED_PROMPTS.map((item, idx) => {
                const Icon = item.icon;
                return (
                  <button
                    key={idx}
                    onClick={() => onSendMessage(item.prompt)}
                    className="p-4 rounded-xl bg-slate-900/80 hover:bg-slate-900 border border-slate-800 hover:border-cyan-500/40 text-slate-300 hover:text-slate-100 transition shadow-lg group flex items-start gap-3"
                  >
                    <div className="p-2 rounded-lg bg-slate-800 group-hover:bg-cyan-500/10 group-hover:text-cyan-400 text-slate-400 transition">
                      <Icon className="w-5 h-5" />
                    </div>
                    <div>
                      <h4 className="text-xs font-semibold text-slate-200 group-hover:text-cyan-400 transition">{item.title}</h4>
                      <p className="text-xs text-slate-400 mt-0.5">{item.desc}</p>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        ) : (
          <div>
            {messages.map((msg) => (
              <MessageItem
                key={msg.id}
                message={msg}
                onSendPrompt={onSendMessage}
                onOpenDataQualityDrawer={onOpenDataQualityDrawer}
              />
            ))}
            {isLoading && <LoadingSteps />}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Form Bar */}
      <div className="p-4 border-t border-slate-800 bg-slate-900/90 backdrop-blur-md">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto flex items-center gap-2">
          {messages.length > 0 && (
            <button
              type="button"
              onClick={onClearChat}
              title="Clear chat history"
              className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-rose-400 border border-slate-700 transition"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}

          <div className="flex-1 relative">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Ask a business question (e.g. 'How is our pipeline looking this quarter?')..."
              disabled={isLoading}
              className="w-full py-3 pl-4 pr-12 bg-slate-950 border border-slate-800 focus:border-cyan-500 rounded-xl text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:ring-1 focus:ring-cyan-500 transition shadow-inner disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={!inputText.trim() || isLoading}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white disabled:opacity-40 disabled:hover:bg-cyan-600 transition shadow-md"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </form>
        <p className="text-[11px] text-slate-400 text-center mt-2">
          Calculations are derived deterministically from Monday.com raw board records. Numerical values are verified in Python.
        </p>
      </div>
    </div>
  );
};
