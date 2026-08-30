import React from 'react';
import { ChartSpecData } from '../../types';
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';

const COLORS = ['#0284c7', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#06b6d4', '#64748b'];

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-slate-900 border border-slate-700 p-3 rounded-lg shadow-xl text-xs">
        <p className="font-semibold text-slate-200 mb-1">{label}</p>
        {payload.map((entry: any, index: number) => (
          <p key={`item-${index}`} className="flex items-center gap-2 text-slate-300">
            <span className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.color }}></span>
            <span>{entry.name}:</span>
            <span className="font-bold text-slate-100">{entry.value}</span>
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export const AnalyticsChart: React.FC<{ chart: ChartSpecData }> = ({ chart }) => {
  if (!chart.data || chart.data.length === 0) return null;

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 my-4 shadow-lg">
      <h4 className="text-sm font-semibold text-slate-200 mb-4 flex items-center gap-2">
        <span className="w-2.5 h-2.5 rounded-full bg-cyan-500"></span>
        {chart.title}
      </h4>

      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          {chart.chart_type === 'pie' || chart.chart_type === 'donut' ? (
            <PieChart>
              <Tooltip content={<CustomTooltip />} />
              <Legend verticalAlign="bottom" height={36} wrapperStyle={{ fontSize: '12px', color: '#94a3b8' }} />
              <Pie
                data={chart.data}
                cx="50%"
                cy="50%"
                innerRadius={chart.chart_type === 'donut' ? 50 : 0}
                outerRadius={80}
                paddingAngle={4}
                dataKey={chart.y_keys[0] || 'value'}
                nameKey={chart.x_key || 'name'}
                label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                labelLine={false}
              >
                {chart.data.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
            </PieChart>
          ) : chart.chart_type === 'area' ? (
            <AreaChart data={chart.data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="colorArea" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#0284c7" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#0284c7" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey={chart.x_key} stroke="#64748b" tick={{ fontSize: 11 }} />
              <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
              <Tooltip content={<CustomTooltip />} />
              <Area type="monotone" dataKey={chart.y_keys[0] || 'value'} stroke="#0284c7" fillOpacity={1} fill="url(#colorArea)" />
            </AreaChart>
          ) : (
            <BarChart data={chart.data} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey={chart.x_key} stroke="#64748b" tick={{ fontSize: 11 }} />
              <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
              <Tooltip content={<CustomTooltip />} />
              <Legend verticalAlign="top" height={30} wrapperStyle={{ fontSize: '12px', color: '#94a3b8' }} />
              {chart.y_keys.map((key, idx) => (
                <Bar key={key} dataKey={key} fill={COLORS[idx % COLORS.length]} radius={[4, 4, 0, 0]} />
              ))}
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  );
};
