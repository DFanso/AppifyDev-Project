/**
 * User session management utilities
 * Provides consistent user identification across the app
 */

const USER_ID_KEY = 'techflow_user_id';

/**
 * Generate a new user ID
 */
function generateUserId(): string {
  return 'user_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now().toString(36);
}

/**
 * Get the current user ID from localStorage or generate a new one
 */
export function getUserId(): string {
  if (typeof window === 'undefined') {
    // Server-side rendering fallback
    return 'user_ssr_' + Math.random().toString(36).substr(2, 9);
  }

  let userId = localStorage.getItem(USER_ID_KEY);
  
  if (!userId) {
    userId = generateUserId();
    localStorage.setItem(USER_ID_KEY, userId);
  }
  
  return userId;
}

/**
 * Clear the current user session (for testing or reset)
 */
export function clearUserSession(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(USER_ID_KEY);
  }
}

/**
 * Check if we have a valid user session
 */
export function hasValidSession(): boolean {
  if (typeof window === 'undefined') return false;
  const userId = localStorage.getItem(USER_ID_KEY);
  return userId !== null && userId.startsWith('user_');
}