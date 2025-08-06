'use client';

import { useState, useEffect } from 'react';
import { Search } from 'lucide-react';

interface SearchBarProps {
  query: string;
  onQueryChange: (query: string) => void;
  className?: string;
  placeholder?: string;
}

export function SearchBar({ query, onQueryChange, className = '', placeholder = 'Search tech news...' }: SearchBarProps) {
  const [localQuery, setLocalQuery] = useState(query);

  // Sync with external query changes
  useEffect(() => {
    setLocalQuery(query);
  }, [query]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmedQuery = localQuery.trim();
    if (trimmedQuery !== query) {
      onQueryChange(trimmedQuery);
    }
  };

  // Debounce search queries
  useEffect(() => {
    const trimmedQuery = localQuery.trim();
    
    // Don't trigger search if the query hasn't actually changed
    if (trimmedQuery === query) return;
    
    const timeoutId = setTimeout(() => {
      if (trimmedQuery.length >= 2) {
        onQueryChange(trimmedQuery);
      } else if (trimmedQuery.length === 0 && query !== '') {
        onQueryChange(''); // Clear search when input is empty
      }
    }, 800); // Increased debounce time to reduce flickering

    return () => clearTimeout(timeoutId);
  }, [localQuery, onQueryChange, query]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLocalQuery(e.target.value);
  };

  return (
    <form onSubmit={handleSubmit} className={`relative ${className}`}>
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <input
          type="text"
          value={localQuery}
          onChange={handleInputChange}
          placeholder={placeholder}
          className="w-full pl-10 pr-4 py-2 border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
        />
      </div>
    </form>
  );
}