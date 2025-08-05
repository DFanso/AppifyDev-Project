'use client';

import { type Category } from '@/lib/validations';

const categories: { value: string; label: string }[] = [
  { value: 'all', label: 'All' },
  { value: 'AI/ML', label: 'AI/ML' },
  { value: 'Startups', label: 'Startups' },
  { value: 'Cybersecurity', label: 'Security' },
  { value: 'Mobile', label: 'Mobile' },
  { value: 'Web3', label: 'Web3' },
  { value: 'General', label: 'General' },
];

interface CategoryFilterProps {
  selectedCategory: string;
  onCategoryChange: (category: string) => void;
}

export function CategoryFilter({ selectedCategory, onCategoryChange }: CategoryFilterProps) {
  return (
    <div className="flex flex-wrap gap-2">
      {categories.map((category) => (
        <button
          key={category.value}
          onClick={() => onCategoryChange(category.value)}
          className={`px-3 py-1.5 text-sm rounded-full transition-colors ${
            selectedCategory === category.value
              ? 'bg-primary text-primary-foreground'
              : 'bg-secondary hover:bg-secondary/80 text-secondary-foreground'
          }`}
        >
          {category.label}
        </button>
      ))}
    </div>
  );
}