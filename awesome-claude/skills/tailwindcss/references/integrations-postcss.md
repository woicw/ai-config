# Tailwind CSS with PostCSS

## Installation

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init
```

## PostCSS Configuration

Create `postcss.config.js` in your project root:

```js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  }
}
```

### With Additional Plugins

```js
module.exports = {
  plugins: {
    'postcss-import': {},
    'tailwindcss/nesting': {},
    tailwindcss: {},
    autoprefixer: {},
  }
}
```

## Tailwind Configuration

Create `tailwind.config.js`:

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js}'],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

## CSS Setup

Create your main CSS file (e.g., `src/input.css`):

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Build Process

### Using PostCSS CLI

Install PostCSS CLI:

```bash
npm install -D postcss-cli
```

Add build script to `package.json`:

```json
{
  "scripts": {
    "build:css": "postcss src/input.css -o dist/output.css",
    "watch:css": "postcss src/input.css -o dist/output.css --watch"
  }
}
```

Run the build:

```bash
npm run build:css
```

### With Webpack

```js
// webpack.config.js
module.exports = {
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader',
          'postcss-loader',
        ],
      },
    ],
  },
}
```

### With Parcel

Parcel automatically detects and uses your PostCSS config. Just import your CSS:

```js
import './styles.css'
```

### With Rollup

```js
// rollup.config.js
import postcss from 'rollup-plugin-postcss'

export default {
  plugins: [
    postcss({
      extensions: ['.css'],
    }),
  ],
}
```

## Using PostCSS Nesting

Enable CSS nesting with Tailwind:

```bash
npm install -D tailwindcss/nesting
```

```js
// postcss.config.js
module.exports = {
  plugins: {
    'tailwindcss/nesting': {},
    tailwindcss: {},
    autoprefixer: {},
  }
}
```

Usage:

```css
.card {
  @apply bg-white rounded-lg shadow;

  & .title {
    @apply text-xl font-bold;
  }

  & .content {
    @apply text-gray-600;
  }
}
```

## Using PostCSS Import

Enable `@import` statements:

```bash
npm install -D postcss-import
```

```js
// postcss.config.js
module.exports = {
  plugins: {
    'postcss-import': {},
    tailwindcss: {},
    autoprefixer: {},
  }
}
```

Usage:

```css
/* input.css */
@import "tailwindcss/base";
@import "./custom-base.css";
@import "tailwindcss/components";
@import "./custom-components.css";
@import "tailwindcss/utilities";
```

## Environment-Specific Configuration

```js
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
    ...(process.env.NODE_ENV === 'production' ? { cssnano: {} } : {})
  }
}
```

## Custom PostCSS Plugin Order

The order of PostCSS plugins matters:

```js
module.exports = {
  plugins: {
    'postcss-import': {},           // 1. Process imports first
    'tailwindcss/nesting': {},      // 2. Handle nesting
    tailwindcss: {},                // 3. Process Tailwind
    autoprefixer: {},               // 4. Add vendor prefixes
    ...(process.env.NODE_ENV === 'production' ? {
      cssnano: {                    // 5. Minify in production
        preset: 'default',
      },
    } : {}),
  }
}
```

## Troubleshooting

### PostCSS not processing Tailwind

1. Ensure `postcss.config.js` is in the project root
2. Check that Tailwind is listed in the plugins
3. Verify your build tool is configured to use PostCSS

### Styles not updating

1. Restart your build process
2. Check content paths in `tailwind.config.js`
3. Clear any build caches