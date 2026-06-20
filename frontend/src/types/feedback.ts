export interface FeedbackCreate {
  session_id: string;
  message_id: string;
  question: string;
  answer: string;
  route_selected?: string;
  feedback_type: 'helpful' | 'not_helpful';
  feedback_comment?: string;
}

export interface FeedbackResponse {
  id: number;
  user_id: number | null;
  session_id: string;
  message_id: string;
  question: string;
  answer: string;
  route_selected: string | null;
  feedback_type: string;
  feedback_comment: string | null;
  created_at: string;
}

export interface FeedbackStats {
  total: number;
  helpful: number;
  not_helpful: number;
  helpful_pct: number;
  not_helpful_pct: number;
  by_agent: Record<string, { helpful: number; not_helpful: number }>;
}
