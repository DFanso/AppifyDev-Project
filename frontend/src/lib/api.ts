import axios from 'axios';
import { 
  type ArticleListResponse, 
  type Article, 
  type ChatMessage, 
  type ChatResponse,
  type ChatHistory,
  type Bookmark,
  type TrendingTopic,
  type SearchRequest
} from '@/lib/validations';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
  maxRedirects: 5,
  withCredentials: true, // Enable credentials for CORS
});

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const errorDetails = {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      data: error.response?.data,
      message: error.message,
      fullError: error,
    };
    
    console.error('API Error:', errorDetails);
    
    // Log specific error details for debugging
    if (error.response?.data) {
      console.error('Error Response Data:', error.response.data);
    }
    
    return Promise.reject(error);
  }
);

// Articles API
export const articlesApi = {
  getArticles: async (params?: {
    page?: number;
    page_size?: number;
    category?: string;
    source?: string;
    sentiment?: string;
    date_from?: string;
    date_to?: string;
  }): Promise<ArticleListResponse> => {
    const { data } = await api.get('/api/articles', { params });
    return data;
  },

  getArticle: async (id: number): Promise<Article> => {
    const { data } = await api.get(`/api/articles/${id}`);
    return data;
  },

  getArticlesByCategory: async (
    category: string,
    page = 1,
    page_size = 20
  ): Promise<ArticleListResponse> => {
    const { data } = await api.get(`/api/articles/category/${category}`, {
      params: { page, page_size }
    });
    return data;
  },

  getRecentArticles: async (
    hours = 24,
    page = 1,
    page_size = 20
  ): Promise<ArticleListResponse> => {
    const { data } = await api.get(`/api/articles/recent/${hours}`, {
      params: { page, page_size }
    });
    return data;
  },
};

// Chat API
export const chatApi = {
  sendMessage: async (message: ChatMessage): Promise<ChatResponse> => {
    const { data } = await api.post('/api/chat', message);
    return data;
  },

  summarizeArticle: async (articleId: number): Promise<{ summary: string; article_id: number }> => {
    const { data } = await api.post(`/api/chat/summarize/${articleId}`);
    return data;
  },

  getChatHistory: async (userId: string, limit = 20): Promise<ChatHistory[]> => {
    const { data } = await api.get(`/api/chat/history/${userId}`, { params: { limit } });
    return data;
  },

  clearChatHistory: async (userId: string): Promise<{ message: string }> => {
    const { data } = await api.delete(`/api/chat/history/${userId}`);
    return data;
  },

  getArticleTopics: async (articleId: number): Promise<{ article_id: number; topics: string[] }> => {
    const { data } = await api.get(`/api/chat/topics/${articleId}`);
    return data;
  },
};

// Search API
export const searchApi = {
  searchArticles: async (params: {
    q: string;
    category?: string;
    source?: string;
    sentiment?: string;
    date_from?: string;
    date_to?: string;
    page?: number;
    page_size?: number;
  }): Promise<ArticleListResponse> => {
    const { data } = await api.get('/api/search', { params });
    return data;
  },

  advancedSearch: async (searchRequest: SearchRequest): Promise<ArticleListResponse> => {
    const { data } = await api.post('/api/search', searchRequest);
    return data;
  },

  getSearchSuggestions: async (query: string, limit = 10): Promise<{ suggestions: string[] }> => {
    const { data } = await api.get('/api/search/suggestions', { params: { q: query, limit } });
    return data;
  },

  getPopularSearches: async (limit = 10): Promise<{ popular_searches: Array<{ term: string; type: string; count: number }> }> => {
    const { data } = await api.get('/api/search/popular', { params: { limit } });
    return data;
  },
};

// Bookmarks API
export const bookmarksApi = {
  createBookmark: async (articleId: number, userId = 'anonymous'): Promise<Bookmark> => {
    const { data } = await api.post('/api/bookmarks', { article_id: articleId, user_id: userId });
    return data;
  },

  getBookmarks: async (userId = 'anonymous', skip = 0, limit = 20): Promise<Bookmark[]> => {
    const { data } = await api.get('/api/bookmarks', { params: { user_id: userId, skip, limit } });
    return data;
  },

  deleteBookmark: async (bookmarkId: number): Promise<{ message: string }> => {
    const { data } = await api.delete(`/api/bookmarks/${bookmarkId}`);
    return data;
  },

  deleteBookmarkByArticle: async (articleId: number, userId = 'anonymous'): Promise<{ message: string }> => {
    const { data } = await api.delete(`/api/bookmarks/article/${articleId}`, { params: { user_id: userId } });
    return data;
  },

  checkBookmark: async (articleId: number, userId = 'anonymous'): Promise<{ is_bookmarked: boolean }> => {
    const { data } = await api.get(`/api/bookmarks/check/${articleId}`, { params: { user_id: userId } });
    return data;
  },
};

// Trending API
export const trendingApi = {
  getTrendingTopics: async (hours = 24, limit = 10): Promise<TrendingTopic[]> => {
    const { data } = await api.get('/api/trending/topics', { params: { hours, limit } });
    return data;
  },

  getTrendingCategories: async (hours = 24): Promise<Array<{ category: string; count: number }>> => {
    const { data } = await api.get('/api/trending/categories', { params: { hours } });
    return data;
  },

  getTrendingSources: async (hours = 24): Promise<Array<{ source: string; count: number }>> => {
    const { data } = await api.get('/api/trending/sources', { params: { hours } });
    return data;
  },

  getSentimentTrends: async (hours = 24): Promise<Array<{ sentiment: string; count: number; percentage: number }>> => {
    const { data } = await api.get('/api/trending/sentiment', { params: { hours } });
    return data;
  },

  getTrendingTimeline: async (hours = 168, interval_hours = 24): Promise<Array<{
    timestamp: string;
    count: number;
    top_categories: Record<string, number>;
  }>> => {
    const { data } = await api.get('/api/trending/timeline', { params: { hours, interval_hours } });
    return data;
  },
};

export default api;