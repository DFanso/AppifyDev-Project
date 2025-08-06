'use client';

import { useState, useEffect, useRef } from 'react';
import { useQuery } from '@tanstack/react-query';
import { NewsFeed } from '@/components/news/news-feed';
import { ChatInterface } from '@/components/chat/chat-interface';
import { SearchBar } from '@/components/search/search-bar';
import { TrendingTopics } from '@/components/trending/trending-topics';
import { CategoryFilter } from '@/components/filters/category-filter';
import { ThemeToggle } from '@/components/ui/theme-toggle';
import { SetupGuide } from '@/components/ui/setup-guide';
import { BookmarksList } from '@/components/bookmarks/bookmarks-list';
import { type Article } from '@/lib/validations';
import { articlesApi } from '@/lib/api';

export default function Home() {
  const [selectedArticle, setSelectedArticle] = useState<Article | null>(null);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [showSetupGuide, setShowSetupGuide] = useState(false);
  const [currentView, setCurrentView] = useState<'news' | 'bookmarks'>('news');
  const chatSectionRef = useRef<HTMLDivElement>(null);

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
    
    // Auto-scroll to chat on mobile devices (below lg breakpoint)
    const scrollToChat = () => {
      if (typeof window === 'undefined' || !chatSectionRef.current) return;
      
      // Check if we're on mobile/tablet (below lg breakpoint: 1024px)
      const isMobile = window.innerWidth < 1024;
      if (!isMobile) return;
      
      // Get the element position and account for the sticky header
      const elementTop = chatSectionRef.current.offsetTop;
      const headerHeight = 120; // Approximate header height with padding
      const targetPosition = Math.max(0, elementTop - headerHeight);
      
      window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
      });
    };
    
    // Add a delay to allow the chat to open and render first
    setTimeout(scrollToChat, 150);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            {/* Logo */}
            <h1 className="text-2xl font-bold text-primary flex-shrink-0">TechFlow</h1>
            
            {/* Category Slider - takes remaining space (only in news view) */}
            {currentView === 'news' && (
              <div className="hidden md:block flex-1 min-w-0">
                <CategoryFilter 
                  selectedCategory={selectedCategory}
                  onCategoryChange={setSelectedCategory}
                />
              </div>
            )}
            
            {/* Spacer for bookmarks view to push content right */}
            {currentView === 'bookmarks' && <div className="flex-1" />}
            
            {/* Navigation and Actions - fixed width */}
            <div className="flex items-center gap-4 flex-shrink-0">
              <SearchBar 
                query={searchQuery}
                onQueryChange={setSearchQuery}
                className="hidden sm:block w-64"
                placeholder={currentView === 'bookmarks' ? 'Search bookmarks...' : 'Search articles...'}
              />
              <div className="flex items-center gap-2">
                <button
                  onClick={() => {
                    setCurrentView('news');
                    setSearchQuery('');
                  }}
                  className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                    currentView === 'news' 
                      ? 'bg-primary text-primary-foreground' 
                      : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
                  }`}
                >
                  News
                </button>
                <button
                  onClick={() => {
                    setCurrentView('bookmarks');
                    setSearchQuery('');
                  }}
                  className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                    currentView === 'bookmarks' 
                      ? 'bg-primary text-primary-foreground' 
                      : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
                  }`}
                >
                  Bookmarks
                </button>
              </div>
              <ThemeToggle />
            </div>
          </div>
          
          {/* Mobile filters */}
          {currentView === 'news' && (
            <div className="mt-4 md:hidden">
              <CategoryFilter 
                selectedCategory={selectedCategory}
                onCategoryChange={setSelectedCategory}
              />
            </div>
          )}
          
          {/* Mobile search */}
          <div className="mt-4 sm:hidden">
            <SearchBar 
              query={searchQuery}
              onQueryChange={setSearchQuery}
              placeholder={currentView === 'bookmarks' ? 'Search bookmarks...' : 'Search articles...'}
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
          
          {/* Main Content */}
          <div className="lg:col-span-2 order-1 lg:order-2">
            {currentView === 'news' ? (
              <NewsFeed 
                searchQuery={searchQuery}
                selectedCategory={selectedCategory}
                onArticleSelect={handleArticleSelect}
              />
            ) : (
              <BookmarksList 
                onArticleSelect={handleArticleSelect}
                searchQuery={searchQuery}
              />
            )}
          </div>
          
          {/* Chat Sidebar */}
          <div ref={chatSectionRef} className="lg:col-span-1 order-3">
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
