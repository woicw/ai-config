# Tailwind CSS with Next.js

## Installation

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

## Configuration

### tailwind.config.js

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### TypeScript Configuration

```ts
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
export default config
```

## CSS Setup

### App Router (Next.js 13+)

Create or update `app/globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Import in `app/layout.tsx`:

```tsx
import './globals.css'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

### Pages Router (Next.js 12 and below)

Create or update `styles/globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Import in `pages/_app.tsx`:

```tsx
import '@/styles/globals.css'
import type { AppProps } from 'next/app'

export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />
}
```

## Usage

### App Router Page

```tsx
export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="container mx-auto px-4 py-16">
        <h1 className="text-4xl font-bold text-center text-gray-900">
          Welcome to Next.js with Tailwind
        </h1>
      </div>
    </main>
  )
}
```

### Component

```tsx
export default function Button({ children }: { children: React.ReactNode }) {
  return (
    <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
      {children}
    </button>
  )
}
```

## Using with CSS Modules

You can use Tailwind's `@apply` directive in CSS Modules:

```css
/* components/Button.module.css */
.button {
  @apply px-4 py-2 bg-blue-600 text-white rounded-lg;
  @apply hover:bg-blue-700 transition-colors;
}
```

```tsx
import styles from './Button.module.css'

export default function Button({ children }: { children: React.ReactNode }) {
  return <button className={styles.button}>{children}</button>
}
```

## Dark Mode with next-themes

Install next-themes:

```bash
npm install next-themes
```

### App Router Setup

```tsx
// app/providers.tsx
'use client'

import { ThemeProvider } from 'next-themes'

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </ThemeProvider>
  )
}
```

```tsx
// app/layout.tsx
import { Providers } from './providers'
import './globals.css'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
```

### Theme Toggle Component

```tsx
'use client'

import { useTheme } from 'next-themes'
import { useEffect, useState } from 'react'

export function ThemeToggle() {
  const [mounted, setMounted] = useState(false)
  const { theme, setTheme } = useTheme()

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return null
  }

  return (
    <button
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      className="p-2 rounded-lg bg-gray-200 dark:bg-gray-800"
    >
      {theme === 'dark' ? '🌞' : '🌙'}
    </button>
  )
}
```

## Optimizing for Production

Next.js automatically optimizes Tailwind CSS in production:
- Removes unused styles
- Minifies CSS
- Enables CSS code splitting

## Turbopack Support

Tailwind CSS works with Next.js Turbopack (Next.js 13+):

```bash
npm run dev --turbo
```

No additional configuration needed.