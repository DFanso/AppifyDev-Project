'use client';

import { useState } from 'react';
import { NewsFeed } from '@/components/news/news-feed';
import { ChatInterface } from '@/components/chat/chat-interface';
import { SearchBar } from '@/components/search/search-bar';
import { TrendingTopics } from '@/components/trending/trending-topics';
import { CategoryFilter } from '@/components/filters/category-filter';
import { ThemeToggle } from '@/components/ui/theme-toggle';
import { Article } from '@/types';

export default function Home() {
  const [selectedArticle, setSelectedArticle] = useState<Article | null>(null);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  const handleArticleSelect = (article: Article) => {
    setSelectedArticle(article);
    setIsChatOpen(true);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-bold text-primary">TechFlow</h1>
              <div className="hidden md:block">
                <CategoryFilter 
                  selectedCategory={selectedCategory}
                  onCategoryChange={setSelectedCategory}
                />
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <SearchBar 
                query={searchQuery}
                onQueryChange={setSearchQuery}
                className="hidden sm:block"
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
