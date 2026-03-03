# Tailwind CSS with Vite

## Installation

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

This creates:
- `tailwind.config.js` - Tailwind configuration
- `postcss.config.js` - PostCSS configuration

## Configuration

### tailwind.config.js

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,vue}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### postcss.config.js

```js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

## CSS Setup

Create a CSS file (e.g., `src/index.css` or `src/style.css`):

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Import CSS

### Vanilla JS / React / Preact

In your main entry file (e.g., `src/main.js` or `src/main.tsx`):

```js
import './index.css'
```

### Vue

In `src/main.js`:

```js
import { createApp } from 'vue'
import App from './App.vue'
import './index.css'

createApp(App).mount('#app')
```

### Svelte

In `src/main.js`:

```js
import App from './App.svelte'
import './index.css'

const app = new App({
  target: document.getElementById('app')
})

export default app
```

## Usage

Start using Tailwind classes in your components:

### React

```jsx
export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <h1 className="text-4xl font-bold text-blue-600">
        Hello Tailwind!
      </h1>
    </div>
  )
}
```

### Vue

```vue
<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center">
    <h1 class="text-4xl font-bold text-blue-600">
      Hello Tailwind!
    </h1>
  </div>
</template>
```

### Svelte

```svelte
<div class="min-h-screen bg-gray-100 flex items-center justify-center">
  <h1 class="text-4xl font-bold text-blue-600">
    Hello Tailwind!
  </h1>
</div>
```

## Development

```bash
npm run dev
```

Vite will automatically:
- Process your CSS with Tailwind
- Enable HMR for instant updates
- Optimize for development

## Production Build

```bash
npm run build
```

Tailwind will automatically:
- Remove unused CSS (tree-shaking)
- Minify the output
- Optimize for production

## TypeScript Support

For TypeScript projects, the setup is the same. Just ensure your content paths include `.ts` and `.tsx` files:

```js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
}
```

## Troubleshooting

### Styles not applying

1. Check that CSS is imported in your entry file
2. Verify content paths in `tailwind.config.js`
3. Ensure PostCSS is configured correctly
4. Restart the dev server

### HMR not working

Restart the Vite dev server after changing Tailwind config.