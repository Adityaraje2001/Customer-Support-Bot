import authApi from '../api/authApi';
import type { FeedbackCreate, FeedbackResponse, FeedbackStats } from '../types/feedback';

export const feedbackService = {
  submitFeedback: async (data: FeedbackCreate): Promise<FeedbackResponse> => {
    const response = await authApi.post<FeedbackResponse>('/feedback/', data);
    return response.data;
  },

  getFeedback: async (): Promise<FeedbackResponse[]> => {
    const response = await authApi.get<FeedbackResponse[]>('/feedback/');
    return response.data;
  },

  getFeedbackStats: async (): Promise<FeedbackStats> => {
    const response = await authApi.get<FeedbackStats>('/feedback/stats');
    return response.data;
  },
};
