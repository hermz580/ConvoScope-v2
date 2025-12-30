# ConvoScope Frontend

Modern React + TypeScript frontend for ConvoScope conversation analytics.

## Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Lint code
npm run lint
```

## Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Zustand** - State management
- **Recharts** - Visualizations
- **Socket.IO** - Real-time updates

## Project Structure

```
src/
├── components/   # Reusable UI components
├── pages/        # Page components
├── hooks/        # Custom React hooks
├── store/        # State management
├── types/        # TypeScript types
├── utils/        # Helper functions
└── assets/       # Static assets
```

## Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:5000
VITE_WS_URL=ws://localhost:5000
```

## License

MIT
