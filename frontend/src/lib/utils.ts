import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { formatDistanceToNow, format, isToday, isYesterday } from 'date-fns';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string | Date): string {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  
  if (isToday(dateObj)) {
    return `Today at ${format(dateObj, 'HH:mm')}`;
  }
  
  if (isYesterday(dateObj)) {
    return `Yesterday at ${format(dateObj, 'HH:mm')}`;
  }
  
  return format(dateObj, 'MMM d, yyyy');
}

export function formatRelativeTime(date: string | Date): string {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return formatDistanceToNow(dateObj, { addSuffix: true });
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength).trim() + '...';
}

export function getSentimentColor(sentiment?: 'positive' | 'negative' | 'neutral'): string {
  switch (sentiment) {
    case 'positive':
      return 'text-green-600 bg-green-50';
    case 'negative':
      return 'text-red-600 bg-red-50';
    case 'neutral':
    default:
      return 'text-gray-600 bg-gray-50';
  }
}

export function getCategoryColor(category?: string): string {
  const colors: Record<string, string> = {
    'AI/ML': 'text-purple-600 bg-purple-50',
    'Startups': 'text-blue-600 bg-blue-50',
    'Cybersecurity': 'text-red-600 bg-red-50',
    'Mobile': 'text-green-600 bg-green-50',
    'Web3': 'text-orange-600 bg-orange-50',
    'General': 'text-gray-600 bg-gray-50',
  };
  
  return colors[category || 'General'] || 'text-gray-600 bg-gray-50';
}

export function getSourceColor(source?: string): string {
  const colors: Record<string, string> = {
    'TechCrunch': 'text-green-600 bg-green-50',
    'The Verge': 'text-purple-600 bg-purple-50',
    'Hacker News': 'text-orange-600 bg-orange-50',
    'Ars Technica': 'text-blue-600 bg-blue-50',
  };
  
  return colors[source || ''] || 'text-gray-600 bg-gray-50';
}

export function extractDomain(url: string): string {
  try {
    const domain = new URL(url).hostname;
    return domain.replace('www.', '');
  } catch {
    return url;
  }
}

export function generateUserId(): string {
  const stored = localStorage.getItem('tech-news-user-id');
  if (stored) return stored;
  
  const newId = 'user_' + Math.random().toString(36).substr(2, 9);
  localStorage.setItem('tech-news-user-id', newId);
  return newId;
}

export function debounce<T extends (...args: unknown[]) => unknown>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

export function throttle<T extends (...args: unknown[]) => unknown>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean;
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}