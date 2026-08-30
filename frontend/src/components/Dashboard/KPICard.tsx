import React from 'react';
import { KPICardData } from '../../types';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

export const KPICard: React.FC<{ card: KPICardData }> = ({ card }) => {
  const getChangeIcon = () => {
    if (card.change_type === 'positive') return <TrendingUp className="w-4 h-4 text-emerald-400" />;
    if (card.change_type === 'negative') return <TrendingDown className="w-4 h-4 text-rose-400" />;
    return <Minus className="w-4 h-4 text-slate-400" />;
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 shadow-lg hover:border-slate-700 transition-all flex flex-col justify-between">
      <div className="flex items-center justify-between gap-2 mb-2">
        <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">{card.title}</span>
        {card.change && (
          <div className="flex items-center gap-1 text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-800 border border-slate-700">
            {getChangeIcon()}
            <span className={card.change_type === 'positive' ? 'text-emerald-400' : card.change_type === 'negative' ? 'text-rose-400' : 'text-slate-300'}>
              {card.change}
            </span>
          </div>
        )}
      </div>

      <div className="text-2xl font-bold text-slate-100 tracking-tight my-1">
        {card.value}
      </div>

      {card.subtitle && (
        <div className="text-xs text-slate-400 mt-1 font-normal">
          {card.subtitle}
        </div>
      )}
    </div>
  );
};
