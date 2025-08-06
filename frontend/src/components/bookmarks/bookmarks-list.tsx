'use client';

import { useQuery } from '@tanstack/react-query';
import { Bookmark, ExternalLink } from 'lucide-react';
import { bookmarksApi } from '@/lib/api';
import { useSession } from '@/hooks/use-session';
import { LoadingSpinner } from '../ui/loading-spinner';
import { ErrorDisplay } from '../ui/error-display';
import { BookmarkButton } from './bookmark-button';
import { formatDistanceToNow } from 'date-fns';
import { type Article } from '@/lib/validations';

interface BookmarksListProps {
  onArticleSelect?: (article: Article) => void;
  searchQuery?: string;
}

export function BookmarksList({ onArticleSelect, searchQuery = '' }: BookmarksListProps) {
  const { userId, isLoading: sessionLoading } = useSession();

  const { data: bookmarks, isLoading, error, refetch } = useQuery({
    queryKey: ['bookmarks', userId],
    queryFn: () => bookmarksApi.getBookmarks(userId, 0, 50),
    enabled: !sessionLoading && !!userId,
    staleTime: 30000, // 30 seconds
  });

  if (sessionLoading || isLoading) {
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
        title="Failed to load bookmarks"
      />
    );
  }

  // Filter bookmarks based on search query
  const filteredBookmarks = bookmarks?.filter(bookmark => {
    if (!searchQuery.trim()) return true;
    
    const query = searchQuery.toLowerCase();
    const article = bookmark.article;
    
    return (
      article.title.toLowerCase().includes(query) ||
      article.content?.toLowerCase().includes(query) ||
      article.source?.toLowerCase().includes(query) ||
      article.category?.toLowerCase().includes(query) ||
      article.author?.toLowerCase().includes(query)
    );
  }) || [];

  if (!bookmarks || bookmarks.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="bg-secondary/20 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
          <Bookmark className="h-6 w-6 text-muted-foreground" />
        </div>
        <h3 className="font-semibold text-lg mb-2">No bookmarks yet</h3>
        <p className="text-muted-foreground">
          Start bookmarking articles to save them for later reading.
        </p>
      </div>
    );
  }

  if (searchQuery.trim() && filteredBookmarks.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="bg-secondary/20 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
          <Bookmark className="h-6 w-6 text-muted-foreground" />
        </div>
        <h3 className="font-semibold text-lg mb-2">No matching bookmarks</h3>
        <p className="text-muted-foreground">
          No bookmarked articles match your search for &ldquo;{searchQuery}&rdquo;.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold flex items-center gap-2">
          <Bookmark className="h-5 w-5" />
          {searchQuery.trim() ? `Search Results` : 'Bookmarked Articles'}
        </h2>
        <span className="text-sm text-muted-foreground">
          {filteredBookmarks.length} {searchQuery.trim() ? 'of ' + bookmarks.length + ' ' : ''}article{filteredBookmarks.length !== 1 ? 's' : ''}
        </span>
      </div>

      <div className="grid gap-4">
        {filteredBookmarks.map((bookmark) => {
          const article = bookmark.article;
          
          const getSentimentColor = (sentiment?: string) => {
            switch (sentiment) {
              case 'positive':
                return 'text-green-600 bg-green-50 dark:bg-green-900/20';
              case 'negative':
                return 'text-red-600 bg-red-50 dark:bg-red-900/20';
              default:
                return 'text-gray-700 bg-gray-100 dark:text-white dark:bg-gray-700';
            }
          };

          const handleArticleClick = () => {
            window.open(article.url, '_blank');
          };

          const handleDiscussClick = () => {
            if (onArticleSelect) {
              onArticleSelect(article);
            }
          };

          return (
            <article 
              key={bookmark.id}
              className="group rounded-lg border bg-card p-4 transition-all hover:shadow-md hover:border-primary/20"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 space-y-3">
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    {article.source && (
                      <>
                        <span className="font-medium">{article.source}</span>
                        <span>•</span>
                      </>
                    )}
                    {article.category && (
                      <>
                        <span>{article.category}</span>
                        <span>•</span>
                      </>
                    )}
                    <span>
                      Bookmarked {formatDistanceToNow(new Date(bookmark.created_at))} ago
                    </span>
                  </div>
                  
                  <h3 
                    className="font-semibold leading-tight cursor-pointer hover:text-primary transition-colors line-clamp-2"
                    onClick={handleArticleClick}
                  >
                    {article.title}
                  </h3>
                  
                  {article.content && (
                    <p 
                      className="text-sm text-muted-foreground line-clamp-2 cursor-pointer hover:text-foreground transition-colors"
                      onClick={handleArticleClick}
                    >
                      {article.content.length > 150 ? `${article.content.substring(0, 150)}...` : article.content}
                    </p>
                  )}
                  
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {article.author && (
                        <span className="text-xs text-muted-foreground">by {article.author}</span>
                      )}
                      {article.sentiment && (
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSentimentColor(article.sentiment)}`}>
                          {article.sentiment}
                        </span>
                      )}
                    </div>
                    
                    <div className="flex items-center gap-2">
                      <button 
                        onClick={handleArticleClick}
                        className="text-xs text-muted-foreground hover:text-primary flex items-center gap-1"
                        title="Open article"
                      >
                        <ExternalLink className="h-3 w-3" />
                        Open
                      </button>
                      {onArticleSelect && (
                        <button 
                          onClick={handleDiscussClick}
                          className="text-xs text-primary hover:underline"
                        >
                          Discuss with AI →
                        </button>
                      )}
                      <BookmarkButton articleId={article.id} />
                    </div>
                  </div>
                </div>
                
                {article.image_url && (
                  <div 
                    className="w-20 h-20 flex-shrink-0 cursor-pointer hover:opacity-80 transition-opacity"
                    onClick={handleArticleClick}
                  >
                    <img 
                      src={article.image_url} 
                      alt={article.title}
                      className="w-full h-full object-cover rounded-md"
                    />
                  </div>
                )}
              </div>
            </article>
          );
        })}
      </div>
    </div>
  );
}