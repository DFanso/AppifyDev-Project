# TechFlow - AI-Powered Tech News Frontend

A modern, minimalist frontend for the tech news aggregation platform built with Next.js 15, TypeScript, and Tailwind CSS.

## 🚀 Features

### Core Features
- **Clean News Feed**: Responsive article cards with previews and metadata
- **AI Chat Interface**: Context-aware discussions about articles
- **Smart Search**: Real-time search with suggestions
- **Category Filtering**: Filter by AI/ML, Startups, Cybersecurity, Mobile, Web3, etc.
- **Trending Dashboard**: Real-time trending topics and analytics
- **Bookmarks**: Save articles for later reading
- **Dark/Light Mode**: System-aware theme switching

### UX/UI Highlights
- **Minimalist Design**: Clean, modern aesthetic inspired by Feedly
- **Mobile-First**: Fully responsive design
- **Fast Loading**: Optimized with React Query caching
- **Smooth Transitions**: Polished animations and interactions

## 🛠️ Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS with CSS variables
- **State Management**: TanStack Query (React Query)
- **Icons**: Lucide React
- **Theming**: next-themes
- **Date Handling**: date-fns
- **HTTP Client**: Axios

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- npm or yarn
- Backend API running on http://localhost:8000

### Installation

```bash
# Install dependencies
npm install

# Set up environment variables
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

### Available Scripts

```bash
npm run dev      # Start development server with Turbopack
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint
```

## 📁 Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout with providers
│   ├── page.tsx           # Main application page
│   └── globals.css        # Global styles and CSS variables
├── components/            # React components
│   ├── bookmarks/         # Bookmark functionality
│   ├── chat/              # AI chat interface
│   ├── filters/           # Category and search filters
│   ├── news/              # News feed and article cards
│   ├── providers/         # Context providers
│   ├── search/            # Search components
│   ├── trending/          # Trending topics dashboard
│   └── ui/                # Reusable UI components
├── lib/
│   ├── api.ts             # API client with all endpoints
│   └── utils.ts           # Utility functions
└── types/
    └── index.ts           # TypeScript type definitions
```

## 🎯 Key Features Implementation

### 1. News Aggregation Display
- Clean, card-based layout with article metadata
- Sentiment analysis indicators
- Source attribution and categorization
- Click-to-discuss AI integration

### 2. AI Chat Integration
- Context-aware conversations about articles
- Conversation history and suggested prompts
- Real-time message handling with loading states

### 3. Real-time Search & Filtering
- Instant search with category filtering
- Trending topics sidebar
- Advanced search capabilities

### 4. Responsive Design
- Mobile-first approach with adaptive layout
- Touch-friendly interactions
- Dark/light mode support

## 🔄 Usage Flow

1. **Browse Articles**: View trending tech news in a clean feed
2. **Filter Content**: Use category filters or search functionality
3. **Engage with AI**: Click any article to start an AI conversation
4. **Save for Later**: Bookmark interesting articles
5. **Discover Trends**: Check the trending topics sidebar

## 🎨 Design Philosophy

- **Minimalist**: Clean interface focusing on content
- **Fast**: Optimized loading and smooth interactions
- **Accessible**: Keyboard navigation and screen reader support
- **Modern**: Latest Next.js features and best practices

## 🚀 Deployment

### Vercel (Recommended)
```bash
npm run build
npx vercel --prod
```

### Environment Variables
```bash
NEXT_PUBLIC_API_URL=your_backend_url
```

## 🔮 Future Enhancements

- Real-time updates via WebSocket
- Advanced analytics dashboard
- User personalization features
- Social sharing capabilities
- PWA support with offline reading

## 📱 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

This frontend is designed to work seamlessly with the TechFlow backend API to provide a complete tech news aggregation and AI discussion platform.
