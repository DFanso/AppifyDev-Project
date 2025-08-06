'use client';

import { useState, useEffect } from 'react';
import { getUserId, clearUserSession, hasValidSession } from '@/lib/session';

/**
 * Hook for managing user session state
 */
export function useSession() {
  const [userId, setUserId] = useState<string>('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Initialize user ID on client side
    const currentUserId = getUserId();
    setUserId(currentUserId);
    setIsLoading(false);
  }, []);

  const resetSession = () => {
    clearUserSession();
    const newUserId = getUserId();
    setUserId(newUserId);
  };

  return {
    userId,
    isLoading,
    resetSession,
    hasValidSession: hasValidSession(),
  };
}