export interface Article {
  id: number;
  title: string;
  url: string;
  content?: string;
  summary?: string;
  author?: string;
  published_at?: string;
  source?: string;
  category?: string;
  sentiment?: 'positive' | 'negative' | 'neutral';
  image_url?: string;
  created_at: string;
  updated_at: string;
}

export interface ArticleListResponse {
  articles: Article[];
  total: number;
  page: number;
  page_size: number;
  has_next: boolean;
}

export interface ChatMessage {
  message: string;
  article_id?: number;
  user_id?: string;
}

export interface ChatResponse {
  response: string;
  article_context?: Article;
  sources?: string[];
}

export interface ChatHistory {
  id: number;
  message: string;
  response: string;
  article_id?: number;
  created_at: string;
}

export interface Bookmark {
  id: number;
  article_id: number;
  article: Article;
  created_at: string;
}

export interface TrendingTopic {
  topic: string;
  count: number;
  score: number;
  articles: Article[];
}

export interface SearchFilters {
  category?: string;
  source?: string;
  sentiment?: 'positive' | 'negative' | 'neutral';
  date_from?: string;
  date_to?: string;
  search_query?: string;
}

export interface SearchRequest {
  query: string;
  filters?: SearchFilters;
  page: number;
  page_size: number;
}

export type Category = 'AI/ML' | 'Startups' | 'Cybersecurity' | 'Mobile' | 'Web3' | 'General';

export type Source = 'TechCrunch' | 'The Verge' | 'Hacker News' | 'Ars Technica';

export type TimeFilter = 'today' | 'week' | 'month' | 'all';