export interface KPICardData {
  title: string;
  value: string;
  change?: string;
  change_type?: 'positive' | 'negative' | 'neutral';
  subtitle?: string;
}

export interface ChartSpecData {
  title: string;
  chart_type: 'bar' | 'pie' | 'donut' | 'area' | 'line' | 'table';
  data: Record<string, any>[];
  x_key: string;
  y_keys: string[];
}

export interface BoardQualitySummary {
  board_name: string;
  total_records: number;
  valid_records: number;
  missing_dates_count: number;
  missing_amounts_count: number;
  missing_status_count: number;
  unnormalized_sectors_count: number;
  completeness_score_pct: number;
  issues: string[];
}

export interface DataQualityReport {
  total_records_analyzed: number;
  overall_health_score_pct: number;
  deals_quality: BoardQualitySummary;
  work_orders_quality: BoardQualitySummary;
  global_warnings: string[];
  last_fetched_timestamp: string;
}

export interface ChatResponseData {
  answer_markdown: string;
  intent_detected: string;
  kpi_cards: KPICardData[];
  charts: ChartSpecData[];
  data_quality_warning?: string;
  data_quality_report?: DataQualityReport;
  suggested_followups: string[];
  clarification_needed: boolean;
  clarification_options: string[];
  timestamp: string;
  is_demo_mode: boolean;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  timestamp: string;
  response_data?: ChatResponseData;
  isLoading?: boolean;
}

export interface LeadershipUpdateData {
  markdown_report: string;
  executive_snapshot: Record<string, any>;
  key_highlights: string[];
  risks_and_attention: string[];
  data_quality_summary: string[];
  generated_at: string;
  is_demo_mode: boolean;
}

export interface MondayStatusData {
  connected: boolean;
  message: string;
  is_demo_mode: boolean;
  has_valid_creds: boolean;
  deals_board_id: string;
  work_orders_board_id: string;
}
