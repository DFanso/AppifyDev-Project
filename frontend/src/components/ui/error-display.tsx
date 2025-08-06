'use client';

import { AlertCircle, RefreshCw, WifiOff } from 'lucide-react';
import { Button } from './button';

interface ErrorDisplayProps {
  error: Error | null;
  onRetry?: () => void;
  title?: string;
  description?: string;
}

export function ErrorDisplay({ error, onRetry, title, description }: ErrorDisplayProps) {
  const isNetworkError = error?.message?.includes('Network Error') || 
                         error?.message?.includes('CORS') ||
                         error?.message?.includes('fetch');

  const getErrorIcon = () => {
    if (isNetworkError) {
      return <WifiOff className="h-8 w-8 text-destructive" />;
    }
    return <AlertCircle className="h-8 w-8 text-destructive" />;
  };

  const getErrorTitle = () => {
    if (title) return title;
    if (isNetworkError) return 'Connection Error';
    return 'Something went wrong';
  };

  const getErrorDescription = () => {
    if (description) return description;
    if (isNetworkError) {
      return 'Unable to connect to the server. Please check your internet connection and make sure the backend is running.';
    }
    return error?.message || 'An unexpected error occurred';
  };

  return (
    <div className="flex flex-col items-center justify-center p-8 text-center space-y-4">
      {getErrorIcon()}
      <div className="space-y-2">
        <h3 className="text-lg font-semibold">{getErrorTitle()}</h3>
        <p className="text-muted-foreground max-w-md text-sm leading-relaxed">
          {getErrorDescription()}
        </p>
      </div>
      
      {isNetworkError && (
        <div className="text-xs text-muted-foreground bg-muted p-3 rounded-lg max-w-sm">
          <p className="font-medium mb-1">Troubleshooting:</p>
          <ul className="text-left space-y-1">
            <li>• Check if the backend is running on port 8000</li>
            <li>• Verify your internet connection</li>
            <li>• Try refreshing the page</li>
          </ul>
        </div>
      )}
      
      {onRetry && (
        <Button onClick={onRetry} variant="outline" className="mt-4">
          <RefreshCw className="h-4 w-4 mr-2" />
          Try Again
        </Button>
      )}
    </div>
  );
}