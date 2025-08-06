import { z } from 'zod';

// Article validation schema
export const articleSchema = z.object({
  id: z.number(),
  title: z.string(),
  url: z.string().url(),
  content: z.string().optional(),
  summary: z.string().optional(),
  author: z.string().optional(),
  published_at: z.string().optional(),
  source: z.string().optional(),
  category: z.string().optional(),
  sentiment: z.enum(['positive', 'negative', 'neutral']).optional(),
  image_url: z.string().nullable().optional().transform((val) => {
    if (!val || val.trim() === '') return null;
    if (val.startsWith('http://') || val.startsWith('https://') || val.startsWith('//')) {
      return val;
    }
    return null;
  }),
  created_at: z.string(),
  updated_at: z.string(),
});

// Article list response schema
export const articleListResponseSchema = z.object({
  articles: z.array(articleSchema),
  total: z.number(),
  page: z.number(),
  page_size: z.number(),
  has_next: z.boolean(),
});

// Chat message schema
export const chatMessageSchema = z.object({
  message: z.string().min(1, 'Message cannot be empty'),
  article_id: z.number().optional(),
  user_id: z.string().optional(),
});

// Chat response schema
export const chatResponseSchema = z.object({
  response: z.string(),
  article_context: articleSchema.optional(),
  sources: z.array(z.string()).optional(),
});

// Chat history schema
export const chatHistorySchema = z.object({
  id: z.number(),
  message: z.string(),
  response: z.string(),
  article_id: z.number().optional(),
  created_at: z.string(),
});

// Search filters schema
export const searchFiltersSchema = z.object({
  category: z.string().optional(),
  source: z.string().optional(),
  sentiment: z.enum(['positive', 'negative', 'neutral']).optional(),
  date_from: z.string().optional(),
  date_to: z.string().optional(),
  search_query: z.string().optional(),
});

// Search request schema
export const searchRequestSchema = z.object({
  query: z.string().min(1, 'Search query cannot be empty'),
  filters: searchFiltersSchema.optional(),
  page: z.number().min(1).default(1),
  page_size: z.number().min(1).max(100).default(20),
});

// Bookmark schema
export const bookmarkSchema = z.object({
  id: z.number(),
  article_id: z.number(),
  article: articleSchema,
  created_at: z.string(),
});

// Trending topic schema
export const trendingTopicSchema = z.object({
  topic: z.string(),
  count: z.number(),
  score: z.number(),
  articles: z.array(articleSchema),
});

// Categories and sources
export const categorySchema = z.enum([
  'Learning', 'Startup', 'Tech News', 'Products & Ideas', 'Engineering blogs', 
  'Machine Learning', 'Design', 'Psychology', 'Neuroscience', 'Science', 
  'Marketing', 'Others'
]);
export const sourceSchema = z.enum([
  'The Decision Lab', 'Ness Labs', 'Farnam Street', 'The Sunday Wisdom',
  'Commonplace - The Commoncog Blog', 'Scott H Young', 'Big Think',
  'Steve Blank', 'The singularity is nearer', 'Hacker News', 'Guy Kawasaki',
  'Essays - Benedict Evans', 'First Round Review', 'Sam Altman', 'Andrew Chen',
  'Both Sides of the Table - Medium', 'OnStartups', 'Product Life', 'Irrational Exuberance',
  'SlashGear', 'VentureBeat', 'The Verge', 'Engadget', 'Tech in Asia', 'TechCrunch',
  'Fast Company', 'Startups – TechCrunch', 'Forbes - Leadership', 'Forbes - Entrepreneurs',
  'Product Hunt', 'Hacker News: Show HN', 'Hacker News: Launches', 'Sachin Rekhi\'s Blog',
  'The Airtable Engineering Blog', 'Medium Engineering', 'The PayPal Technology Blog',
  'Pinterest Engineering Blog', 'Grab Tech', 'Slack Engineering', 'Engineering – The GitHub Blog',
  'Atlassian Developer Blog', 'Engineering at Meta', 'eBay Tech Blog', 'Spotify Engineering',
  'Twitter Engineering', 'Stripe Blog', 'Instagram Engineering', 'The Cloudflare Blog',
  'Engineering – The Asana Blog', 'Canva Engineering Blog', 'The Airbnb Tech Blog',
  'Dropbox Tech', 'Julia Evans', 'Martin Kleppmann\'s blog', 'Dan Abramov\'s Overreacted Blog',
  'Dan Luu', 'Shopify Engineering', 'Josh Comeau\'s blog', 'Uber Engineering Blog',
  'Flurries of latent creativity - Stripe CTO blog', 'Sophie Alpert', 'Amjad Masad',
  'Signal Blog', 'Joel on Software', 'The Pragmatic Engineer', 'Machine Learning Blog | ML@CMU',
  'DeepMind', 'Jay Alammar', 'Lil\'Log', 'MIT News - Artificial intelligence',
  'Sebastian Ruder', 'The Berkeley AI Research Blog', 'Eric Jang', 'OpenAI',
  'The Gradient', 'Google AI Blog', 'Towards Data Science', 'Unite.AI',
  'Amazon Science Homepage', 'UX Planet', 'NN/g latest articles', 'UX Movement',
  'Inside Design', 'UXmatters', 'Smashing Magazine', 'UX Collective', 'Airbnb Design',
  'web.dev', 'Slack Design', 'CSS-Tricks', 'PsyBlog', 'Psychology Blog',
  'Psychology Headlines Around the World', 'Nautilus', 'Psychology Today',
  'Neuroscience News', 'Neuroscience News -- ScienceDaily', 'SharpBrains',
  'Quanta Magazine', 'Nature', 'MIT News', 'ScienceAlert', 'Singularity Hub',
  'Moz', 'Content Marketing Institute', 'Neil Patel', 'MarketingProfs',
  'Social Media Examiner', 'Seth Godin\'s Blog', 'Backlinko', 'HBR.org'
]);
export const timeFilterSchema = z.enum(['today', 'week', 'month', 'all']);

// Form validation schemas
export const searchFormSchema = z.object({
  query: z.string().min(1, 'Please enter a search term'),
  category: z.string().optional(),
  source: z.string().optional(),
  sentiment: z.string().optional(),
});

export const chatFormSchema = z.object({
  message: z.string().min(1, 'Please enter a message').max(1000, 'Message is too long'),
});

// API response wrapper schema
export const apiResponseSchema = <T>(dataSchema: z.ZodSchema<T>) =>
  z.object({
    data: dataSchema,
    success: z.boolean().default(true),
    message: z.string().optional(),
  });

// Error response schema
export const errorResponseSchema = z.object({
  error: z.string(),
  message: z.string(),
  status_code: z.number(),
  details: z.record(z.string(), z.unknown()).optional(),
});

// Type exports
export type Article = z.infer<typeof articleSchema>;
export type ArticleListResponse = z.infer<typeof articleListResponseSchema>;
export type ChatMessage = z.infer<typeof chatMessageSchema>;
export type ChatResponse = z.infer<typeof chatResponseSchema>;
export type ChatHistory = z.infer<typeof chatHistorySchema>;
export type SearchFilters = z.infer<typeof searchFiltersSchema>;
export type SearchRequest = z.infer<typeof searchRequestSchema>;
export type Bookmark = z.infer<typeof bookmarkSchema>;
export type TrendingTopic = z.infer<typeof trendingTopicSchema>;
export type Category = z.infer<typeof categorySchema>;
export type Source = z.infer<typeof sourceSchema>;
export type TimeFilter = z.infer<typeof timeFilterSchema>;
export type SearchFormData = z.infer<typeof searchFormSchema>;
export type ChatFormData = z.infer<typeof chatFormSchema>;
export type ErrorResponse = z.infer<typeof errorResponseSchema>;