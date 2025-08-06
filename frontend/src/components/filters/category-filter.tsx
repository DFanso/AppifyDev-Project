'use client';

import { useRef, useEffect, useState } from 'react';

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
  const [isDragging, setIsDragging] = useState(false);
  const [startX, setStartX] = useState(0);
  const [scrollLeft, setScrollLeft] = useState(0);
  const [hasActuallyDragged, setHasActuallyDragged] = useState(false);

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

  // Global mouse events for smooth dragging
  useEffect(() => {
    const handleGlobalMouseMove = (e: MouseEvent) => {
      if (!isDragging || !scrollContainerRef.current) return;
      e.preventDefault();
      const x = e.pageX - scrollContainerRef.current.offsetLeft;
      const walk = (x - startX) * 2;
      const newDragDistance = Math.abs(walk);
      
      // Only mark as actually dragged if we've moved more than 3px
      if (newDragDistance > 3) {
        setHasActuallyDragged(true);
      }
      
      scrollContainerRef.current.scrollLeft = scrollLeft - walk;
    };

    const handleGlobalMouseUp = () => {
      setIsDragging(false);
      if (scrollContainerRef.current) {
        scrollContainerRef.current.style.cursor = 'grab';
      }
      // Reset drag states after a short delay
      setTimeout(() => {
        setHasActuallyDragged(false);
      }, 50); // Shorter delay for more responsive clicks
    };

    if (isDragging) {
      document.addEventListener('mousemove', handleGlobalMouseMove);
      document.addEventListener('mouseup', handleGlobalMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleGlobalMouseMove);
      document.removeEventListener('mouseup', handleGlobalMouseUp);
    };
  }, [isDragging, startX, scrollLeft]);

  // Drag scrolling functionality
  const handleMouseDown = (e: React.MouseEvent) => {
    if (!scrollContainerRef.current) return;
    setIsDragging(true);
    setHasActuallyDragged(false); // Reset drag state
    setStartX(e.pageX - scrollContainerRef.current.offsetLeft);
    setScrollLeft(scrollContainerRef.current.scrollLeft);
    scrollContainerRef.current.style.cursor = 'grabbing';
    // Don't prevent default here - let buttons handle their own events initially
  };

  // Touch support for mobile
  const handleTouchStart = (e: React.TouchEvent) => {
    if (!scrollContainerRef.current) return;
    setIsDragging(true);
    setHasActuallyDragged(false);
    setStartX(e.touches[0].pageX - scrollContainerRef.current.offsetLeft);
    setScrollLeft(scrollContainerRef.current.scrollLeft);
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (!isDragging || !scrollContainerRef.current) return;
    const x = e.touches[0].pageX - scrollContainerRef.current.offsetLeft;
    const walk = (x - startX) * 2;
    const newDragDistance = Math.abs(walk);
    
    // Mark as dragged if moved more than 3px
    if (newDragDistance > 3) {
      setHasActuallyDragged(true);
    }
    
    scrollContainerRef.current.scrollLeft = scrollLeft - walk;
  };

  const handleTouchEnd = () => {
    setIsDragging(false);
    // Reset drag states after a short delay
    setTimeout(() => {
        setHasActuallyDragged(false);
    }, 50);
  };

  return (
    <div className="relative flex items-center w-full">
      {/* Drag-scrollable categories container */}
      <div 
        ref={scrollContainerRef}
        className="flex gap-2 overflow-x-auto scrollbar-hide px-2 w-full cursor-grab select-none"
        style={{
          scrollbarWidth: 'none',
          msOverflowStyle: 'none',
          cursor: isDragging ? 'grabbing' : 'grab'
        } as React.CSSProperties}
        onMouseDown={handleMouseDown}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      >
        {categories.map((category) => {
          const isSelected = selectedCategory === category.value;
          return (
            <button
              key={category.value}
              ref={isSelected ? selectedButtonRef : null}
              onClick={(e) => {
                // Only prevent click if we actually dragged significantly
                if (hasActuallyDragged) {
                  e.preventDefault();
                  e.stopPropagation();
                  return;
                }
                onCategoryChange(category.value);
              }}
              className={`px-3 py-1.5 text-sm rounded-full whitespace-nowrap transition-colors flex-shrink-0 ${
                isSelected
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-secondary hover:bg-secondary/80 text-secondary-foreground'
              }`}
              style={{ pointerEvents: hasActuallyDragged ? 'none' : 'auto' }}
            >
              {category.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}