# Tailwind CSS Configuration

## Configuration File

Tailwind CSS is configured via `tailwind.config.js`, `tailwind.config.ts`, or `tailwind.config.mjs` in the project root.

### Basic Configuration Structure

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,jsx,ts,tsx,vue}'],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### TypeScript Configuration

```ts
import type { Config } from 'tailwindcss'

export default {
  content: ['./src/**/*.{html,js,jsx,ts,tsx,vue}'],
  theme: {
    extend: {},
  },
  plugins: [],
} satisfies Config
```

## Content Configuration

The `content` option specifies which files Tailwind should scan for class names.

```js
module.exports = {
  content: [
    './src/**/*.{html,js,jsx,ts,tsx}',
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
}
```

### Content with Transform

```js
module.exports = {
  content: {
    files: ['./src/**/*.{html,js}'],
    transform: {
      md: (content) => {
        return content.replace(/^---[\s\S]*?---/, '')
      }
    }
  }
}
```

## Important Options

### darkMode

Configure dark mode strategy:

```js
module.exports = {
  darkMode: 'class', // or 'media' or ['class', '[data-mode="dark"]']
}
```

### prefix

Add a prefix to all utility classes:

```js
module.exports = {
  prefix: 'tw-',
}
```

### important

Make utilities !important:

```js
module.exports = {
  important: true, // or '#app' for selector strategy
}
```

### separator

Customize the separator for variants:

```js
module.exports = {
  separator: '_', // default is ':'
}
```

### corePlugins

Disable specific core plugins:

```js
module.exports = {
  corePlugins: {
    preflight: false,
    container: false,
  }
}
```

## Presets

Extend from a preset configuration:

```js
module.exports = {
  presets: [
    require('@acme/tailwind-preset')
  ],
  // Your overrides
}
```
