'use client';

import { type Article } from '@/lib/validations';
import { formatDistanceToNow } from 'date-fns';
import { BookmarkButton } from '../bookmarks/bookmark-button';

interface ArticleCardProps {
  article: Article;
  onClick: () => void;
}

export function ArticleCard({ article, onClick }: ArticleCardProps) {
  const getSentimentColor = (sentiment?: string) => {
    switch (sentiment) {
      case 'positive':
        return 'text-green-600 bg-green-50 dark:bg-green-900/20';
      case 'negative':
        return 'text-red-600 bg-red-50 dark:bg-red-900/20';
      default:
        return 'text-gray-600 bg-gray-50 dark:bg-gray-800';
    }
  };

  return (
    <article 
      className="group cursor-pointer rounded-lg border bg-card p-6 transition-all hover:shadow-md hover:border-primary/20"
      onClick={onClick}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 space-y-3">
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <span className="font-medium">{article.source}</span>
            <span>•</span>
            <span>{article.category}</span>
            <span>•</span>
            <span>{formatDistanceToNow(new Date(article.published_at || article.created_at))} ago</span>
          </div>
          
          <h3 className="font-semibold leading-tight group-hover:text-primary transition-colors line-clamp-2">
            {article.title}
          </h3>
          
          {article.content && (
            <p className="text-sm text-muted-foreground line-clamp-3">
              {article.content.length > 200 ? `${article.content.substring(0, 200)}...` : article.content}
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
              <BookmarkButton articleId={article.id} />
              <button className="text-xs text-primary hover:underline">
                Discuss with AI →
              </button>
            </div>
          </div>
        </div>
        
        {article.image_url && (
          <div className="w-24 h-24 flex-shrink-0">
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
}