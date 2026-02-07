---
name: app-development
description: Building web applications with React, Vite/Next, and TailwindCSS
---

# App Development Preferences

Preferences for building web applications.

## Stack Overview

| Aspect | Choice |
|--------|--------|
| Framework | React (Functional Components) |
| Build Tool | Vite (SPA) or Next (SSR/SSG) |
| Styling | TailwindCSS |
| hooks | ahooks |
| Components | antd / shadcn/ui |
| Routing | React Router |
| State Management | Zustand |
| Data Fetching | useRequest |
| HTTP | axios |

---

## Framework Selection

| Use Case | Choice |
|----------|--------|
| SPA, client-only, library playgrounds | Vite + React |
| SSR, SSG, SEO-critical, file-based routing, API routes | Next |

---

## React Conventions

## Directory Structure

```
src/
├── components/             # Shared components
│   ├── custom-component
│   │   └── index.tsx       # Custom component implementation
│   └── ui/                 # shadcn/ui UI components
├── hooks/                  # Custom hooks
├── constants/              # Constants
├── routes/                 # Route configuration
├── stores/                 # Zustand stores
├── pages/                  # Page components
│   └── custom-page 
│        ├── components/         # Page-specific components
│        ├── hooks/              # Page-specific hooks
│        ├── helpers.ts(x)       # Page helper functions
│        ├── types.ts(x)         # Page type definitions
│        └── index.tsx           # Page entry point
├── services/               # API services
├── styles/                 # Style files
├── utils/                  # Utility functions
└── types/                  # Type definitions
```
