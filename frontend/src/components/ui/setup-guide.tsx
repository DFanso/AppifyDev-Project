'use client';

import { AlertTriangle, CheckCircle, ExternalLink } from 'lucide-react';
import { Button } from './button';

interface SetupGuideProps {
  onDismiss?: () => void;
}

export function SetupGuide({ onDismiss }: SetupGuideProps) {
  return (
    <div className="bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800 rounded-lg p-6">
      <div className="flex items-start gap-3">
        <AlertTriangle className="h-5 w-5 text-orange-600 mt-0.5 flex-shrink-0" />
        <div className="flex-1">
          <h3 className="font-semibold text-orange-900 dark:text-orange-100 mb-2">
            Backend Setup Required
          </h3>
          <p className="text-sm text-orange-800 dark:text-orange-200 mb-4">
            Some features may not work correctly. Please ensure the backend is properly configured:
          </p>
          
          <div className="space-y-3 text-sm">
            <div className="flex items-center gap-2">
              <CheckCircle className="h-4 w-4 text-green-600" />
              <span>Backend server running on port 8000</span>
            </div>
            
            <div className="flex items-start gap-2">
              <div className="h-4 w-4 border-2 border-orange-400 rounded-full mt-0.5 flex-shrink-0" />
              <div>
                <span className="block">OpenAI API key configured</span>
                <code className="text-xs bg-orange-100 dark:bg-orange-900 px-1 py-0.5 rounded mt-1 block">
                  OPENAI_API_KEY=your_key_here
                </code>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <CheckCircle className="h-4 w-4 text-green-600" />
              <span>Database initialized with sample data</span>
            </div>
          </div>
          
          <div className="mt-4 space-y-2">
            <p className="text-xs text-orange-700 dark:text-orange-300">
              To fix the AI chat functionality:
            </p>
            <ol className="text-xs text-orange-700 dark:text-orange-300 space-y-1 ml-4">
              <li>1. Create a <code className="bg-orange-100 dark:bg-orange-900 px-1 rounded">.env</code> file in the backend directory</li>
              <li>2. Add your OpenAI API key: <code className="bg-orange-100 dark:bg-orange-900 px-1 rounded">OPENAI_API_KEY=sk-...</code></li>
              <li>3. Restart the backend server</li>
            </ol>
          </div>
          
          <div className="flex items-center justify-between mt-4">
            <a 
              href="https://platform.openai.com/api-keys" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-xs text-orange-600 hover:text-orange-700 flex items-center gap-1"
            >
              Get OpenAI API Key <ExternalLink className="h-3 w-3" />
            </a>
            
            {onDismiss && (
              <Button 
                variant="outline" 
                size="sm" 
                onClick={onDismiss}
                className="text-xs"
              >
                Dismiss
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}