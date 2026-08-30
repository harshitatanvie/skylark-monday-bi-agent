import axios from 'axios';
import { 
  ChatResponseData, 
  LeadershipUpdateData, 
  MondayStatusData, 
  DataQualityReport 
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

export const sendChatMessage = async (
  message: string, 
  useDemoMode?: boolean
): Promise<ChatResponseData> => {
  const response = await api.post<ChatResponseData>('/api/chat', {
    message,
    use_demo_mode: useDemoMode,
  });
  return response.data;
};

export const fetchLeadershipUpdate = async (
  useDemoMode?: boolean
): Promise<LeadershipUpdateData> => {
  const response = await api.post<LeadershipUpdateData>(
    `/api/leadership-update?use_demo_mode=${useDemoMode ? 'true' : 'false'}`
  );
  return response.data;
};

export const fetchMondayStatus = async (): Promise<MondayStatusData> => {
  const response = await api.get<MondayStatusData>('/api/monday/status');
  return response.data;
};

export const fetchDataQuality = async (useDemoMode?: boolean): Promise<DataQualityReport> => {
  const response = await api.get<DataQualityReport>(
    `/api/data-quality?use_demo_mode=${useDemoMode ? 'true' : 'false'}`
  );
  return response.data;
};
