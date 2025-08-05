'use client';

import { useState } from 'react';
import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query';
import { Bookmark, BookmarkCheck } from 'lucide-react';
import { bookmarksApi } from '@/lib/api';

interface BookmarkButtonProps {
  articleId: number;
  userId?: string;
}

export function BookmarkButton({ articleId, userId = 'anonymous' }: BookmarkButtonProps) {
  const queryClient = useQueryClient();

  const { data: bookmarkStatus } = useQuery({
    queryKey: ['bookmark-status', articleId, userId],
    queryFn: () => bookmarksApi.checkBookmark(articleId, userId),
  });

  const createBookmarkMutation = useMutation({
    mutationFn: () => bookmarksApi.createBookmark(articleId, userId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['bookmark-status', articleId, userId] });
      queryClient.invalidateQueries({ queryKey: ['bookmarks', userId] });
    },
  });

  const deleteBookmarkMutation = useMutation({
    mutationFn: () => bookmarksApi.deleteBookmarkByArticle(articleId, userId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['bookmark-status', articleId, userId] });
      queryClient.invalidateQueries({ queryKey: ['bookmarks', userId] });
    },
  });

  const isBookmarked = bookmarkStatus?.is_bookmarked;
  const isLoading = createBookmarkMutation.isPending || deleteBookmarkMutation.isPending;

  const handleToggleBookmark = () => {
    if (isBookmarked) {
      deleteBookmarkMutation.mutate();
    } else {
      createBookmarkMutation.mutate();
    }
  };

  return (
    <button
      onClick={handleToggleBookmark}
      disabled={isLoading}
      className={`p-2 rounded-lg transition-colors ${
        isBookmarked
          ? 'text-primary bg-primary/10 hover:bg-primary/20'
          : 'text-muted-foreground hover:text-primary hover:bg-primary/10'
      } disabled:opacity-50`}
      title={isBookmarked ? 'Remove bookmark' : 'Add bookmark'}
    >
      {isBookmarked ? (
        <BookmarkCheck className="h-4 w-4" />
      ) : (
        <Bookmark className="h-4 w-4" />
      )}
    </button>
  );
}