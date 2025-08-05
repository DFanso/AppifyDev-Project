'use client';

import { useQuery } from '@tanstack/react-query';
import { ArticleCard } from './article-card';
import { LoadingSpinner } from '../ui/loading-spinner';
import { ErrorDisplay } from '../ui/error-display';
import { articlesApi, searchApi } from '@/lib/api';
import { type Article } from '@/lib/validations';

interface NewsFeedProps {
  searchQuery: string;
  selectedCategory: string;
  onArticleSelect: (article: Article) => void;
}

export function NewsFeed({ searchQuery, selectedCategory, onArticleSelect }: NewsFeedProps) {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['articles', searchQuery, selectedCategory],
    queryFn: async () => {
      if (searchQuery) {
        return searchApi.searchArticles({
          q: searchQuery,
          category: selectedCategory === 'all' ? undefined : selectedCategory,
          page: 1,
          page_size: 20,
        });
      }
      
      return articlesApi.getArticles({
        category: selectedCategory === 'all' ? undefined : selectedCategory,
        page: 1,
        page_size: 20,
      });
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 2,
    retryDelay: 1000,
  });

  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return (
      <ErrorDisplay 
        error={error as Error}
        onRetry={() => refetch()}
        title="Failed to load articles"
      />
    );
  }

  if (!data?.articles?.length) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">No articles found.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">
          {searchQuery ? `Search Results: "${searchQuery}"` : 'Latest Tech News'}
        </h2>
        <span className="text-sm text-muted-foreground">
          {data.total} articles
        </span>
      </div>
      
      <div className="grid gap-6">
        {data.articles.map((article) => (
          <ArticleCard
            key={article.id}
            article={article}
            onClick={() => onArticleSelect(article)}
          />
        ))}
      </div>
      
      {data.has_next && (
        <div className="text-center py-4">
          <button className="text-primary hover:underline">
            Load more articles
          </button>
        </div>
      )}
    </div>
  );
}