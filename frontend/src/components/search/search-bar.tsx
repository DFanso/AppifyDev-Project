'use client';

import { useState, useEffect } from 'react';
import { Search } from 'lucide-react';

interface SearchBarProps {
  query: string;
  onQueryChange: (query: string) => void;
  className?: string;
}

export function SearchBar({ query, onQueryChange, className = '' }: SearchBarProps) {
  const [localQuery, setLocalQuery] = useState(query);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (localQuery.trim()) {
      onQueryChange(localQuery.trim());
    }
  };

  // Debounce search queries
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (localQuery.trim().length >= 2) {
        onQueryChange(localQuery.trim());
      } else if (localQuery.trim().length === 0 && query !== '') {
        onQueryChange(''); // Clear search when input is empty
      }
    }, 500);

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
          placeholder="Search tech news..."
          className="w-full pl-10 pr-4 py-2 border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
        />
      </div>
    </form>
  );
}