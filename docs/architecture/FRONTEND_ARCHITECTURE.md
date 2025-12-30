# ConvoScope Frontend Architecture

## Technology Stack

### Core Framework
- **React 18.3+** with TypeScript
- **Vite 5.x** for blazing-fast builds
- **React Router v6** for navigation

### State Management
- **Zustand** - Lightweight, performant state management
  - Global app state (uploaded data, analysis results, user settings)
  - Persistent state (settings saved to localStorage)
  - Middleware for debugging and devtools

### UI Framework
- **Tailwind CSS 3.x** - Utility-first styling
- **shadcn/ui** - High-quality React components
  - Accessible by default (WCAG 2.1 AA)
  - Customizable and themeable
  - No runtime dependencies

### Data Visualization
- **Recharts 2.x** - React-native charting library
  - Composable chart components
  - Responsive and interactive
  - TypeScript support

### Data Tables
- **TanStack Table v8** - Headless table library
  - Powerful filtering, sorting, pagination
  - Fully customizable
  - Type-safe

### Communication
- **Axios** - HTTP client for REST API
- **Socket.IO Client** - WebSocket for real-time updates

### Development Tools
- **TypeScript 5.x** - Type safety
- **ESLint** - Code linting
- **Prettier** - Code formatting
- **Vitest** - Unit testing

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── common/          # Generic components (Button, Card, etc.)
│   │   ├── dashboard/       # Dashboard-specific components
│   │   ├── charts/          # Chart components
│   │   ├── upload/          # File upload components
│   │   └── layout/          # Layout components (Header, Sidebar)
│   │
│   ├── pages/               # Page-level components
│   │   ├── Dashboard.tsx    # Main overview page
│   │   ├── Topics.tsx       # Topics exploration
│   │   ├── Quality.tsx      # Quality analysis
│   │   ├── Timeline.tsx     # Temporal analysis
│   │   ├── Conversations.tsx # Conversation browser
│   │   ├── Privacy.tsx      # Privacy dashboard
│   │   └── Upload.tsx       # Upload & onboarding
│   │
│   ├── hooks/               # Custom React hooks
│   │   ├── useAnalysis.ts   # Hook for analysis data
│   │   ├── useWebSocket.ts  # WebSocket connection hook
│   │   ├── useFilters.ts    # Data filtering hook
│   │   └── useExport.ts     # Export functionality hook
│   │
│   ├── store/               # Zustand stores
│   │   ├── analysisStore.ts # Analysis data store
│   │   ├── uiStore.ts       # UI state (modals, sidebar, etc.)
│   │   └── settingsStore.ts # User settings store
│   │
│   ├── types/               # TypeScript type definitions
│   │   ├── analysis.ts      # Analysis data types
│   │   ├── api.ts           # API response types
│   │   └── common.ts        # Shared types
│   │
│   ├── utils/               # Helper functions
│   │   ├── api.ts           # API client
│   │   ├── formatters.ts    # Data formatting
│   │   ├── validators.ts    # Input validation
│   │   └── exports.ts       # Export utilities
│   │
│   ├── assets/              # Static assets
│   │   ├── images/
│   │   └── fonts/
│   │
│   ├── App.tsx              # Main app component
│   ├── main.tsx             # Entry point
│   └── index.css            # Global styles
│
├── public/                  # Static files
│   ├── favicon.ico
│   └── manifest.json
│
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
└── README.md
```

## State Management Architecture

### Zustand Stores

**1. Analysis Store**
```typescript
interface AnalysisState {
  // Data
  uploadedFile: File | null
  analysisResults: AnalysisResults | null
  isAnalyzing: boolean
  progress: number

  // Actions
  setUploadedFile: (file: File) => void
  startAnalysis: () => Promise<void>
  updateProgress: (progress: number) => void
  setResults: (results: AnalysisResults) => void
  reset: () => void
}
```

**2. UI Store**
```typescript
interface UIState {
  // UI State
  sidebarOpen: boolean
  currentModal: string | null
  theme: 'light' | 'dark' | 'system'

  // Actions
  toggleSidebar: () => void
  openModal: (modalId: string) => void
  closeModal: () => void
  setTheme: (theme: Theme) => void
}
```

**3. Settings Store**
```typescript
interface SettingsState {
  // Settings
  privacySettings: PrivacySettings
  exportSettings: ExportSettings

  // Actions
  updatePrivacySettings: (settings: Partial<PrivacySettings>) => void
  updateExportSettings: (settings: Partial<ExportSettings>) => void
  resetToDefaults: () => void
}
```

## Routing Structure

```typescript
<BrowserRouter>
  <Routes>
    <Route path="/" element={<Upload />} />
    <Route path="/app" element={<Layout />}>
      <Route index element={<Dashboard />} />
      <Route path="topics" element={<Topics />} />
      <Route path="quality" element={<Quality />} />
      <Route path="timeline" element={<Timeline />} />
      <Route path="conversations" element={<Conversations />} />
      <Route path="conversations/:id" element={<ConversationDetail />} />
      <Route path="privacy" element={<Privacy />} />
      <Route path="settings" element={<Settings />} />
    </Route>
    <Route path="*" element={<NotFound />} />
  </Routes>
</BrowserRouter>
```

## Component Architecture

### Atomic Design Principles

**Atoms** - Basic building blocks
- Button, Input, Label, Badge, Icon

**Molecules** - Simple component groups
- StatCard, ChartCard, FilterBar, SearchInput

**Organisms** - Complex components
- TopicExplorer, QualityDashboard, ConversationList

**Templates** - Page layouts
- DashboardLayout, DetailLayout

**Pages** - Actual pages
- Dashboard, Topics, Quality, etc.

## Data Flow

```
User Action
    ↓
Component Event Handler
    ↓
Zustand Store Action
    ↓
API Call (if needed)
    ↓
Update Store State
    ↓
React Re-renders Components
    ↓
User Sees Updated UI
```

## Performance Optimizations

### Code Splitting
```typescript
// Lazy load heavy pages
const Topics = lazy(() => import('./pages/Topics'))
const Timeline = lazy(() => import('./pages/Timeline'))

// Wrap in Suspense
<Suspense fallback={<LoadingSpinner />}>
  <Topics />
</Suspense>
```

### Memoization
```typescript
// Memoize expensive calculations
const filteredData = useMemo(() => {
  return data.filter(item => filters.apply(item))
}, [data, filters])

// Memoize callbacks
const handleClick = useCallback(() => {
  // Handle click
}, [dependencies])
```

### Virtualization
```typescript
// For long lists (conversation browser)
import { useVirtualizer } from '@tanstack/react-virtual'

const rowVirtualizer = useVirtualizer({
  count: conversations.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 100,
})
```

## Accessibility Features

### Keyboard Navigation
- All interactive elements keyboard-accessible
- Focus indicators visible
- Tab order logical

### Screen Reader Support
- Semantic HTML
- ARIA labels where needed
- Descriptive alt text
- Live regions for dynamic updates

### Visual Accessibility
- High contrast mode support
- Respects `prefers-reduced-motion`
- Minimum 4.5:1 color contrast
- Scalable fonts (rem units)

## Responsive Design

### Breakpoints
```typescript
// Tailwind breakpoints
sm: '640px'   // Mobile landscape
md: '768px'   // Tablet
lg: '1024px'  // Desktop
xl: '1280px'  // Large desktop
2xl: '1536px' // Extra large
```

### Mobile-First Approach
```jsx
// Design for mobile, enhance for desktop
<div className="flex flex-col md:flex-row">
  <Sidebar className="w-full md:w-64" />
  <Main className="flex-1" />
</div>
```

## Error Handling

### Error Boundaries
```typescript
<ErrorBoundary fallback={<ErrorPage />}>
  <App />
</ErrorBoundary>
```

### API Error Handling
```typescript
try {
  const data = await api.analyze(file)
  setResults(data)
} catch (error) {
  if (error instanceof ValidationError) {
    toast.error('Invalid file format')
  } else if (error instanceof NetworkError) {
    toast.error('Network error. Please try again.')
  } else {
    toast.error('Unexpected error occurred')
  }
}
```

## Testing Strategy

### Unit Tests
- Test utility functions
- Test custom hooks
- Test store actions

### Component Tests
- Test user interactions
- Test rendering
- Test accessibility

### Integration Tests
- Test page flows
- Test API integration
- Test WebSocket connection

## Build & Deployment

### Development
```bash
npm run dev        # Start dev server
npm run test       # Run tests
npm run lint       # Lint code
```

### Production Build
```bash
npm run build      # Create optimized build
npm run preview    # Preview production build
```

### Bundle Analysis
```bash
npm run build -- --mode analyze  # Analyze bundle size
```

## Environment Variables

```env
VITE_API_URL=http://localhost:5000
VITE_WS_URL=ws://localhost:5000
VITE_APP_VERSION=2.0.0
```

## Type Safety

### Strict TypeScript Configuration
```json
{
  "compilerOptions": {
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

### Type-Safe API Calls
```typescript
// Define API response types
interface AnalysisResponse {
  id: string
  status: 'pending' | 'processing' | 'complete'
  results?: AnalysisResults
  error?: string
}

// Type-safe API client
const api = {
  analyze: (file: File): Promise<AnalysisResponse> => {
    return axios.post('/api/analyze', file)
      .then(res => res.data)
  }
}
```

## Security Considerations

### Input Validation
- Validate file size (< 100MB)
- Validate file type (JSON only)
- Sanitize user inputs

### XSS Prevention
- React escapes by default
- No `dangerouslySetInnerHTML` without sanitization
- Content Security Policy headers

### CORS Configuration
```typescript
// Backend CORS config
app.use(cors({
  origin: 'http://localhost:3000',
  credentials: true
}))
```

## Future Enhancements

- [ ] Progressive Web App (PWA) support
- [ ] Offline mode with Service Workers
- [ ] Dark mode support
- [ ] Internationalization (i18n)
- [ ] Advanced analytics
- [ ] Plugin system for custom analyzers
- [ ] Collaboration features
- [ ] Mobile app (React Native)
