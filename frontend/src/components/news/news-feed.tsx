'use client';

import { useState, useEffect } from 'react';
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
  const [currentPage, setCurrentPage] = useState(1);
  const [allArticles, setAllArticles] = useState<Article[]>([]);
  
  const { data, isLoading, error, refetch, isFetching } = useQuery({
    queryKey: ['articles', searchQuery, selectedCategory, currentPage],
    queryFn: async () => {
      if (searchQuery) {
        return searchApi.searchArticles({
          q: searchQuery,
          category: selectedCategory === 'all' ? undefined : selectedCategory,
          page: currentPage,
          page_size: 20,
        });
      }
      
      return articlesApi.getArticles({
        category: selectedCategory === 'all' ? undefined : selectedCategory,
        page: currentPage,
        page_size: 20,
      });
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 2,
    retryDelay: 1000,
  });

  // Reset page and articles when search query or category changes
  useEffect(() => {
    setCurrentPage(1);
    setAllArticles([]);
  }, [searchQuery, selectedCategory]);

  // Update articles when data changes
  useEffect(() => {
    if (data) {
      if (currentPage === 1) {
        // Reset articles for new search/category
        setAllArticles(data.articles);
      } else {
        // Append new articles for pagination
        setAllArticles(prev => [...prev, ...data.articles]);
      }
    }
  }, [data, currentPage]);

  const handleLoadMore = () => {
    if (data?.has_next) {
      setCurrentPage(prev => prev + 1);
    }
  };

  const articlesToShow = allArticles.length > 0 ? allArticles : data?.articles || [];

  if (isLoading && currentPage === 1) {
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

  if (!articlesToShow?.length) {
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
          {searchQuery ? (
            `Search Results: "${searchQuery}"`
          ) : selectedCategory !== 'all' ? (
            selectedCategory.toLowerCase().includes('news') ? selectedCategory : `${selectedCategory} News`
          ) : (
            'Latest Tech News'
          )}
        </h2>
        <span className="text-sm text-muted-foreground">
          {data?.total || 0} articles
        </span>
      </div>
      
      <div className="grid gap-6">
        {articlesToShow.map((article) => (
          <ArticleCard
            key={article.id}
            article={article}
            onDiscussClick={() => onArticleSelect(article)}
          />
        ))}
      </div>
      
      {data?.has_next && (
        <div className="text-center py-4">
          <button 
            onClick={handleLoadMore}
            disabled={isFetching}
            className="text-primary hover:underline disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 mx-auto"
          >
            {isFetching ? (
              <>
                <LoadingSpinner className="h-4 w-4" />
                Loading more articles...
              </>
            ) : (
              'Load more articles'
            )}
          </button>
        </div>
      )}
    </div>
  );
}