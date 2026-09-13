# Frontend: Web Interface

This folder contains Phase 3 and beyond of the project.

## Phase 3: Web Interface (Next.js + TypeScript)

Build a user-facing search application with React.

### What You'll Build

- **Search Bar**: Input field for queries
- **Results Display**: Show documents with similarity scores
- **Responsive Design**: Works on desktop & mobile
- **Real-time Search**: Updates as you type (optional)

### What You'll Learn

- React component structure
- Next.js app routing
- TypeScript type safety
- API integration from frontend
- State management (React hooks)

### Expected Output

```
┌──────────────────────────────────┐
│ 🔍 Semantic Search Engine        │
├──────────────────────────────────┤
│ [     Search query...          ] │
│ [Search]                         │
├──────────────────────────────────┤
│ Results:                         │
│ ▶ Apple (0.98)                   │
│   Sweet red fruit...             │
│ ▶ Cherry (0.95)                  │
│   Small red fruit...             │
│ ▶ Strawberry (0.93)              │
│   Berries with seeds...          │
└──────────────────────────────────┘
```

---

## Phase 4: Production Features

Enhance document handling and metadata.

### Phase 5: Vector Database

Scale to millions of documents using Pinecone.

---

## Implementation Status

- [ ] Phase 3: Next.js setup
- [ ] Phase 3: React components
- [ ] Phase 3: API integration
- [ ] Phase 4: Document ingestion
- [ ] Phase 5: Pinecone integration

---

## Dependencies (Will Install in Phase 3)

```
next                    # React framework
typescript              # Type safety
tailwindcss             # Styling (optional)
axios                   # HTTP client
```

---

## Folder Structure (Will Grow)

```
frontend/
├── README.md
├── package.json
├── tsconfig.json
├── app/
│   ├── layout.tsx
│   ├── page.tsx          (main search page)
│   └── api/              (optional backend routes)
├── components/
│   ├── SearchBar.tsx
│   ├── ResultsList.tsx
│   └── ResultItem.tsx
├── lib/
│   └── api.ts            (API client)
└── public/               (static files)
```

---

## Getting Started

Phase 3 starts after backend is complete.

**Prerequisites**:
- Backend API running (Phase 2)
- Understanding of React & Next.js basics
- TypeScript fundamentals

**Next**: Build Phase 1 backend first, then return here.
