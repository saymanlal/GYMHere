# Frontend - Gym Management System

Modern, responsive Next.js frontend with TypeScript and TailwindCSS.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS + ShadCN UI
- **State Management**: 
  - React Query (TanStack Query) for server state
  - Zustand for client state
- **Forms**: React Hook Form + Zod validation
- **Tables**: TanStack Table
- **Charts**: Recharts
- **Icons**: Lucide React

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

```bash
# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Start development server
npm run dev
```

The application will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Authentication pages
│   ├── (dashboard)/       # Dashboard pages (protected)
│   └── layout.tsx         # Root layout
├── components/
│   ├── ui/                # Base UI components (ShadCN)
│   ├── forms/             # Form components
│   └── layouts/           # Layout components
├── features/              # Feature-based modules
│   ├── members/           # Member management
│   ├── attendance/        # Attendance tracking
│   └── ...
├── hooks/                 # Shared React hooks
├── services/              # API services
│   ├── api.ts            # Axios configuration
│   └── *.service.ts      # Feature services
├── utils/                 # Utility functions
└── styles/               # Global styles
```

## Key Features

### API Integration

All API calls go through the `apiService` which handles:
- Authentication tokens
- Automatic token refresh
- Error handling
- Request/response interceptors

Example:
```typescript
import { apiService } from "@/services/api";

const response = await apiService.get("/members/");
```

### React Query

Server state management with automatic caching, refetching, and synchronization:

```typescript
import { useMembers } from "@/features/members/hooks/useMemberQueries";

function MembersList() {
  const { data, isLoading } = useMembers({ page: 1 });
  // Component code
}
```

### Form Handling

Forms use React Hook Form with Zod validation:

```typescript
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";

const schema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
});

const form = useForm({
  resolver: zodResolver(schema),
});
```

### Styling

TailwindCSS utilities with custom design system:

```tsx
<div className="flex items-center gap-4 p-6 rounded-lg border bg-card">
  <Button variant="default" size="lg">
    Click Me
  </Button>
</div>
```

## Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript compiler check
```

## Environment Variables

Create `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=Gym Management System
```

## Code Organization

### Feature Modules

Each feature has its own directory with:
- `components/` - Feature-specific components
- `hooks/` - React Query hooks
- `services/` - API calls
- `types.ts` - TypeScript interfaces

### Component Guidelines

1. Use functional components with hooks
2. Define prop types with TypeScript interfaces
3. Use descriptive names (PascalCase for components)
4. Keep components focused and small
5. Extract reusable logic to hooks

Example:
```typescript
interface MemberCardProps {
  member: Member;
  onEdit: (id: string) => void;
}

export function MemberCard({ member, onEdit }: MemberCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{member.fullName}</CardTitle>
      </CardHeader>
      <CardContent>
        <Button onClick={() => onEdit(member.id)}>Edit</Button>
      </CardContent>
    </Card>
  );
}
```

## Authentication Flow

1. User logs in via `/login`
2. Tokens stored in localStorage
3. `apiService` adds token to all requests
4. Automatic token refresh on expiry
5. Redirect to login if refresh fails

## Adding New Features

1. Create feature directory in `features/`
2. Add types in `types.ts`
3. Create service in `services/`
4. Add React Query hooks in `hooks/`
5. Build components in `components/`
6. Create page in `app/(dashboard)/`

See [Developer Guide](../docs/developer-guide.md) for detailed instructions.

## Performance Optimization

- Server Components for static content
- Client Components for interactivity
- Image optimization with `next/image`
- Code splitting with dynamic imports
- React Query caching
- Debounced search inputs

## Best Practices

1. **Type Safety**: Use TypeScript strictly, avoid `any`
2. **Error Handling**: Always handle errors in API calls
3. **Loading States**: Show loading indicators
4. **Accessibility**: Use semantic HTML and ARIA labels
5. **Responsive Design**: Mobile-first approach
6. **Performance**: Optimize renders with React.memo when needed

## Troubleshooting

**API Connection Issues**
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Ensure backend is running on port 8000

**Build Errors**
- Clear `.next` folder and rebuild
- Check for TypeScript errors with `npm run type-check`

**Styling Issues**
- Rebuild Tailwind: restart dev server
- Check class names are in TailwindCSS whitelist

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Query Docs](https://tanstack.com/query/latest)
- [TailwindCSS Docs](https://tailwindcss.com/docs)
- [ShadCN UI](https://ui.shadcn.com/)