'use client';

import { useRef, useEffect } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { type Category } from '@/lib/validations';

const categories: { value: string; label: string }[] = [
  { value: 'all', label: 'All' },
  { value: 'Learning', label: 'Learning' },
  { value: 'Startup', label: 'Startup' },
  { value: 'Tech News', label: 'Tech News' },
  { value: 'Products & Ideas', label: 'Products & Ideas' },
  { value: 'Engineering blogs', label: 'Engineering' },
  { value: 'Machine Learning', label: 'Machine Learning' },
  { value: 'Design', label: 'Design' },
  { value: 'Psychology', label: 'Psychology' },
  { value: 'Neuroscience', label: 'Neuroscience' },
  { value: 'Science', label: 'Science' },
  { value: 'Marketing', label: 'Marketing' },
  { value: 'Others', label: 'Others' },
];

interface CategoryFilterProps {
  selectedCategory: string;
  onCategoryChange: (category: string) => void;
}

export function CategoryFilter({ selectedCategory, onCategoryChange }: CategoryFilterProps) {
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const selectedButtonRef = useRef<HTMLButtonElement>(null);

  // Auto-scroll to selected category
  useEffect(() => {
    if (selectedButtonRef.current && scrollContainerRef.current) {
      const container = scrollContainerRef.current;
      const button = selectedButtonRef.current;
      const containerRect = container.getBoundingClientRect();
      const buttonRect = button.getBoundingClientRect();
      
      // Check if button is outside the visible area
      if (buttonRect.left < containerRect.left || buttonRect.right > containerRect.right) {
        const scrollLeft = button.offsetLeft - container.offsetWidth / 2 + button.offsetWidth / 2;
        container.scrollTo({ left: scrollLeft, behavior: 'smooth' });
      }
    }
  }, [selectedCategory]);

  const scroll = (direction: 'left' | 'right') => {
    if (scrollContainerRef.current) {
      const scrollAmount = 150;
      const newScrollLeft = scrollContainerRef.current.scrollLeft + 
        (direction === 'left' ? -scrollAmount : scrollAmount);
      scrollContainerRef.current.scrollTo({ left: newScrollLeft, behavior: 'smooth' });
    }
  };

  return (
    <div className="relative flex items-center group w-full">
      {/* Left scroll button */}
      <button
        onClick={() => scroll('left')}
        className="absolute left-0 z-10 flex items-center justify-center w-6 h-6 bg-background/90 backdrop-blur-sm border rounded-full shadow-sm opacity-0 group-hover:opacity-100 transition-opacity hover:bg-background"
        aria-label="Scroll left"
      >
        <ChevronLeft className="h-3 w-3" />
      </button>

      {/* Scrollable categories container */}
      <div 
        ref={scrollContainerRef}
        className="flex gap-2 overflow-x-auto scrollbar-hide px-6 w-full"
        style={{
          scrollbarWidth: 'none',
          msOverflowStyle: 'none',
          WebkitScrollbar: { display: 'none' }
        }}
      >
        {categories.map((category) => {
          const isSelected = selectedCategory === category.value;
          return (
            <button
              key={category.value}
              ref={isSelected ? selectedButtonRef : null}
              onClick={() => onCategoryChange(category.value)}
              className={`px-3 py-1.5 text-sm rounded-full whitespace-nowrap transition-colors flex-shrink-0 ${
                isSelected
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-secondary hover:bg-secondary/80 text-secondary-foreground'
              }`}
            >
              {category.label}
            </button>
          );
        })}
      </div>

      {/* Right scroll button */}
      <button
        onClick={() => scroll('right')}
        className="absolute right-0 z-10 flex items-center justify-center w-6 h-6 bg-background/90 backdrop-blur-sm border rounded-full shadow-sm opacity-0 group-hover:opacity-100 transition-opacity hover:bg-background"
        aria-label="Scroll right"
      >
        <ChevronRight className="h-3 w-3" />
      </button>
    </div>
  );
}