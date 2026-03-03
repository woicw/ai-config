# Tailwind CSS Content Configuration

## Content Paths

Configure which files Tailwind should scan for class names:

```js
module.exports = {
  content: [
    './src/**/*.{html,js,jsx,ts,tsx}',
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
}
```

## Glob Patterns

Use glob patterns to match files:

```js
module.exports = {
  content: [
    './src/**/*.{html,js}',           // All HTML and JS in src
    './pages/**/*.tsx',                // All TSX in pages
    './components/**/*.{jsx,tsx}',     // JSX and TSX in components
    '!./src/excluded/**/*',            // Exclude specific paths
  ],
}
```

## Content with Options

### Transform Content

Transform file content before extraction:

```js
module.exports = {
  content: {
    files: ['./src/**/*.{html,js}'],
    transform: {
      md: (content) => {
        // Remove frontmatter from markdown files
        return content.replace(/^---[\s\S]*?---/, '')
      }
    }
  }
}
```

### Extract Patterns

Customize how classes are extracted:

```js
module.exports = {
  content: {
    files: ['./src/**/*.{html,js}'],
    extract: {
      js: (content) => {
        // Custom extraction logic
        return content.match(/[^<>"'`\s]*[^<>"'`\s:]/g) || []
      }
    }
  }
}
```

## Safelisting Classes

Force Tailwind to include specific classes:

### Basic Safelist

```js
module.exports = {
  safelist: [
    'bg-red-500',
    'text-3xl',
    'lg:text-4xl',
  ]
}
```

### Pattern-Based Safelist

```js
module.exports = {
  safelist: [
    {
      pattern: /bg-(red|green|blue)-(100|200|300)/,
    },
    {
      pattern: /text-(sm|base|lg|xl)/,
      variants: ['lg', 'hover', 'focus'],
    },
  ]
}
```

### Safelist Everything (Not Recommended)

```js
module.exports = {
  safelist: [
    {
      pattern: /.*/,
    },
  ]
}
```

## Blocklisting Classes

Prevent specific classes from being generated:

```js
module.exports = {
  blocklist: [
    'container',
    'collapse',
  ]
}
```

### Pattern-Based Blocklist

```js
module.exports = {
  blocklist: [
    /^debug-/,
  ]
}
```

## Dynamic Class Names

### ❌ Don't construct class names dynamically

```jsx
// Bad - Tailwind won't detect these
<div className={`text-${size}`}>
<div className={`bg-${color}-500`}>
```

### ✅ Use complete class names

```jsx
// Good - Tailwind can detect these
<div className={size === 'large' ? 'text-lg' : 'text-sm'}>
<div className={color === 'red' ? 'bg-red-500' : 'bg-blue-500'}>
```

### ✅ Or use safelist

```js
// tailwind.config.js
module.exports = {
  safelist: [
    'text-sm',
    'text-base',
    'text-lg',
    'bg-red-500',
    'bg-blue-500',
  ]
}
```

## Node Modules

Include classes from node_modules:

```js
module.exports = {
  content: [
    './src/**/*.{html,js}',
    './node_modules/@my-company/ui/**/*.js',
  ],
}
```

## Raw Content

Provide content directly:

```js
module.exports = {
  content: {
    files: ['./src/**/*.{html,js}'],
    raw: {
      css: ['@tailwind base; @tailwind components; @tailwind utilities;'],
    }
  }
}
```