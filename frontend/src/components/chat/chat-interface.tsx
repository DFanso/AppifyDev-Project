'use client';

import { useState, useRef, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Send, MessageCircle, X, Sparkles } from 'lucide-react';
import { chatApi } from '@/lib/api';
import { type Article, type ChatHistory } from '@/lib/validations';
import { LoadingSpinner } from '../ui/loading-spinner';
import { ErrorDisplay } from '../ui/error-display';

interface ChatInterfaceProps {
  selectedArticle: Article | null;
  isOpen: boolean;
  onClose: () => void;
}

export function ChatInterface({ selectedArticle, isOpen, onClose }: ChatInterfaceProps) {
  const [message, setMessage] = useState('');
  const [userId] = useState('user_' + Math.random().toString(36).substr(2, 9));
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const queryClient = useQueryClient();

  const { data: chatHistory, isLoading } = useQuery({
    queryKey: ['chat-history', userId],
    queryFn: () => chatApi.getChatHistory(userId, 50),
    enabled: isOpen,
  });

  const sendMessageMutation = useMutation({
    mutationFn: (messageData: { message: string; article_id?: number; user_id: string }) =>
      chatApi.sendMessage(messageData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chat-history', userId] });
      setMessage('');
    },
    onError: (error: any) => {
      console.error('Chat error:', error);
      // You could show a toast or error message here
    },
  });

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;

    sendMessageMutation.mutate({
      message: message.trim(),
      article_id: selectedArticle?.id,
      user_id: userId,
    });
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory, sendMessageMutation.isPending]);

  if (!isOpen) {
    return (
      <div className="bg-card rounded-lg border p-6">
        <div className="text-center">
          <MessageCircle className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
          <h3 className="font-semibold mb-2">AI Chat Assistant</h3>
          <p className="text-sm text-muted-foreground">
            Select an article to start a conversation
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-card rounded-lg border flex flex-col h-[600px]">
      {/* Header */}
      <div className="p-4 border-b flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Sparkles className="h-4 w-4 text-primary" />
          <h3 className="font-semibold">AI Assistant</h3>
        </div>
        <button
          onClick={onClose}
          className="p-1 hover:bg-secondary rounded"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      {/* Selected Article Context */}
      {selectedArticle && (
        <div className="p-3 bg-primary/5 border-b">
          <p className="text-xs text-muted-foreground mb-1">Discussing:</p>
          <p className="text-sm font-medium line-clamp-2">
            {selectedArticle.title}
          </p>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {isLoading ? (
          <LoadingSpinner />
        ) : chatHistory?.length ? (
          chatHistory.map((chat) => (
            <div key={chat.id} className="space-y-3">
              <div className="flex justify-end">
                <div className="bg-primary text-primary-foreground p-3 rounded-lg max-w-[80%]">
                  <p className="text-sm">{chat.message}</p>
                </div>
              </div>
              <div className="flex justify-start">
                <div className="bg-secondary p-3 rounded-lg max-w-[80%]">
                  <div className="flex items-start gap-2">
                    <Sparkles className="h-3 w-3 text-primary mt-1 flex-shrink-0" />
                    <p className="text-sm">{chat.response}</p>
                  </div>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center text-muted-foreground">
            <p className="text-sm">Start a conversation about the article!</p>
            {selectedArticle && (
              <div className="mt-4 space-y-2">
                <button
                  onClick={() => setMessage('Can you summarize this article?')}
                  className="block w-full text-left p-2 text-xs bg-secondary hover:bg-secondary/80 rounded"
                >
                  💡 Can you summarize this article?
                </button>
                <button
                  onClick={() => setMessage('What are the key takeaways?')}
                  className="block w-full text-left p-2 text-xs bg-secondary hover:bg-secondary/80 rounded"
                >
                  🎯 What are the key takeaways?
                </button>
                <button
                  onClick={() => setMessage('How does this impact the industry?')}
                  className="block w-full text-left p-2 text-xs bg-secondary hover:bg-secondary/80 rounded"
                >
                  🌍 How does this impact the industry?
                </button>
              </div>
            )}
          </div>
        )}

        {sendMessageMutation.isPending && (
          <div className="flex justify-start">
            <div className="bg-secondary p-3 rounded-lg">
              <LoadingSpinner />
            </div>
          </div>
        )}

        {sendMessageMutation.error && (
          <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-3">
            <div className="flex items-start gap-2">
              <X className="h-4 w-4 text-destructive mt-0.5 flex-shrink-0" />
              <div className="text-sm">
                <p className="font-medium text-destructive mb-1">Failed to send message</p>
                <p className="text-muted-foreground">
                  {(sendMessageMutation.error as any)?.response?.status === 500 
                    ? "The AI service is currently unavailable. Please check that the OpenAI API key is configured in the backend."
                    : "Unable to send message. Please try again."}
                </p>
                <button 
                  onClick={() => sendMessageMutation.reset()} 
                  className="text-xs text-primary hover:underline mt-1"
                >
                  Dismiss
                </button>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSendMessage} className="p-4 border-t">
        <div className="flex gap-2">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder={
              selectedArticle
                ? 'Ask about this article...'
                : 'Ask about tech news...'
            }
            className="flex-1 px-3 py-2 border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            disabled={sendMessageMutation.isPending}
          />
          <button
            type="submit"
            disabled={!message.trim() || sendMessageMutation.isPending}
            className="p-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
      </form>
    </div>
  );
}