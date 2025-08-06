'use client';

import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { NewsFeed } from '@/components/news/news-feed';
import { ChatInterface } from '@/components/chat/chat-interface';
import { SearchBar } from '@/components/search/search-bar';
import { TrendingTopics } from '@/components/trending/trending-topics';
import { CategoryFilter } from '@/components/filters/category-filter';
import { ThemeToggle } from '@/components/ui/theme-toggle';
import { SetupGuide } from '@/components/ui/setup-guide';
import { type Article } from '@/lib/validations';
import { articlesApi } from '@/lib/api';

export default function Home() {
  const [selectedArticle, setSelectedArticle] = useState<Article | null>(null);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [showSetupGuide, setShowSetupGuide] = useState(false);

  // Check if backend is working by trying to fetch articles
  const { data: healthCheck, isError: healthError } = useQuery({
    queryKey: ['health-check'],
    queryFn: () => articlesApi.getArticles({ page: 1, page_size: 1 }),
    retry: 1,
    staleTime: 30000, // 30 seconds
  });

  // Show setup guide only if there are backend issues
  useEffect(() => {
    if (healthError) {
      setShowSetupGuide(true);
    } else if (healthCheck) {
      setShowSetupGuide(false);
    }
  }, [healthError, healthCheck]);

  const handleArticleSelect = (article: Article) => {
    setSelectedArticle(article);
    setIsChatOpen(true);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            {/* Logo */}
            <h1 className="text-2xl font-bold text-primary flex-shrink-0">TechFlow</h1>
            
            {/* Category Slider - takes remaining space */}
            <div className="hidden md:block flex-1 min-w-0">
              <CategoryFilter 
                selectedCategory={selectedCategory}
                onCategoryChange={setSelectedCategory}
              />
            </div>
            
            {/* Search and Theme - fixed width */}
            <div className="flex items-center gap-4 flex-shrink-0">
              <SearchBar 
                query={searchQuery}
                onQueryChange={setSearchQuery}
                className="hidden sm:block w-64"
              />
              <ThemeToggle />
            </div>
          </div>
          
          {/* Mobile filters */}
          <div className="mt-4 md:hidden">
            <CategoryFilter 
              selectedCategory={selectedCategory}
              onCategoryChange={setSelectedCategory}
            />
          </div>
          
          {/* Mobile search */}
          <div className="mt-4 sm:hidden">
            <SearchBar 
              query={searchQuery}
              onQueryChange={setSearchQuery}
            />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-6">
        {/* Setup Guide */}
        {showSetupGuide && (
          <div className="mb-6">
            <SetupGuide onDismiss={() => setShowSetupGuide(false)} />
          </div>
        )}
        
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Trending Sidebar */}
          <div className="lg:col-span-1 order-2 lg:order-1">
            <TrendingTopics />
          </div>
          
          {/* News Feed */}
          <div className="lg:col-span-2 order-1 lg:order-2">
            <NewsFeed 
              searchQuery={searchQuery}
              selectedCategory={selectedCategory}
              onArticleSelect={handleArticleSelect}
            />
          </div>
          
          {/* Chat Sidebar */}
          <div className="lg:col-span-1 order-3">
            <div className="sticky top-24">
              <ChatInterface 
                selectedArticle={selectedArticle}
                isOpen={isChatOpen}
                onClose={() => setIsChatOpen(false)}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
