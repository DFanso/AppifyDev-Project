'use client';

import { useQuery } from '@tanstack/react-query';
import { trendingApi } from '@/lib/api';
import { LoadingSpinner } from '../ui/loading-spinner';
import { ErrorDisplay } from '../ui/error-display';
import { TrendingUp } from 'lucide-react';

export function TrendingTopics() {
  const { data: topics, isLoading, error, refetch } = useQuery({
    queryKey: ['trending-topics'],
    queryFn: () => trendingApi.getTrendingTopics(168, 8), // 7 days instead of 24 hours
    staleTime: 15 * 60 * 1000, // 15 minutes
    retry: 2,
  });

  const { data: categories, error: categoriesError } = useQuery({
    queryKey: ['trending-categories'],
    queryFn: () => trendingApi.getTrendingCategories(168), // 7 days instead of 24 hours
    staleTime: 15 * 60 * 1000,
    retry: 2,
  });

  if (isLoading) {
    return (
      <div className="bg-card rounded-lg border p-6">
        <h3 className="font-semibold mb-4 flex items-center gap-2">
          <TrendingUp className="h-4 w-4" />
          Trending Now
        </h3>
        <LoadingSpinner />
      </div>
    );
  }

  if (error || categoriesError) {
    return (
      <div className="bg-card rounded-lg border p-6">
        <h3 className="font-semibold mb-4 flex items-center gap-2">
          <TrendingUp className="h-4 w-4" />
          Trending Topics
        </h3>
        <ErrorDisplay 
          error={(error || categoriesError) as Error}
          onRetry={() => refetch()}
          title="Failed to load trends"
          description="Unable to fetch trending topics right now."
        />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Trending Topics */}
      <div className="bg-card rounded-lg border p-6">
        <h3 className="font-semibold mb-4 flex items-center gap-2">
          <TrendingUp className="h-4 w-4" />
          Trending Topics
        </h3>
        <div className="space-y-3">
          {topics && topics.length > 0 ? (
            topics.slice(0, 6).map((topic, index) => (
              <div key={topic.topic} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-xs font-mono text-muted-foreground w-4">
                    #{index + 1}
                  </span>
                  <span className="text-sm font-medium line-clamp-1">
                    {topic.topic}
                  </span>
                </div>
                <span className="text-xs text-muted-foreground">
                  {topic.count}
                </span>
              </div>
            ))
          ) : (
            <div className="text-center py-4">
              <p className="text-sm text-muted-foreground">
                No trending topics yet
              </p>
              <p className="text-xs text-muted-foreground mt-1">
                Topics will appear as more articles are added
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Trending Categories */}
      <div className="bg-card rounded-lg border p-6">
        <h3 className="font-semibold mb-4">Hot Categories</h3>
        <div className="space-y-2">
          {categories && categories.length > 0 ? (
            categories.slice(0, 5).map((category) => (
              <div key={category.category} className="flex items-center justify-between">
                <span className="text-sm">{category.category}</span>
                <span className="text-xs text-muted-foreground">
                  {category.count}
                </span>
              </div>
            ))
          ) : (
            <div className="text-center py-4">
              <p className="text-sm text-muted-foreground">
                No category data yet
              </p>
              <p className="text-xs text-muted-foreground mt-1">
                Categories will appear as articles are categorized
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}