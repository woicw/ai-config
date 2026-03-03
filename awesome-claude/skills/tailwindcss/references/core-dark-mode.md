# Tailwind CSS Dark Mode

## Configuration

Configure dark mode in `tailwind.config.js`:

### Class Strategy (Recommended)

```js
module.exports = {
  darkMode: 'class',
}
```

Toggle dark mode by adding the `dark` class to the `html` or `body` element:

```html
<html class="dark">
  <!-- Dark mode enabled -->
</html>
```

### Media Strategy

```js
module.exports = {
  darkMode: 'media',
}
```

Automatically uses the system's dark mode preference.

### Custom Selector

```js
module.exports = {
  darkMode: ['class', '[data-mode="dark"]'],
}
```

## Usage

### Basic Dark Mode Styling

```html
<div class="bg-white dark:bg-gray-900">
  <p class="text-gray-900 dark:text-white">
    Content that adapts to dark mode
  </p>
</div>
```

### Dark Mode with Hover

```html
<button class="bg-blue-500 hover:bg-blue-600 dark:bg-blue-700 dark:hover:bg-blue-800">
  Button
</button>
```

### Dark Mode with Responsive

```html
<div class="bg-white md:bg-gray-100 dark:bg-gray-900 dark:md:bg-gray-800">
  Responsive dark mode
</div>
```

## Implementation Example

### React/Next.js with next-themes

```jsx
import { ThemeProvider } from 'next-themes'

function App({ Component, pageProps }) {
  return (
    <ThemeProvider attribute="class">
      <Component {...pageProps} />
    </ThemeProvider>
  )
}
```

### Toggle Component

```jsx
import { useTheme } from 'next-themes'

function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  return (
    <button
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      class="p-2 rounded-lg bg-gray-200 dark:bg-gray-800"
    >
      {theme === 'dark' ? '🌞' : '🌙'}
    </button>
  )
}
```

### Vanilla JavaScript

```html
<script>
  // Check for saved theme preference or default to system
  const theme = localStorage.getItem('theme') ||
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')

  if (theme === 'dark') {
    document.documentElement.classList.add('dark')
  }

  // Toggle function
  function toggleTheme() {
    const isDark = document.documentElement.classList.toggle('dark')
    localStorage.setItem('theme', isDark ? 'dark' : 'light')
  }
</script>
```

## Common Patterns

### Card Component

```html
<div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg dark:shadow-gray-900/50 p-6">
  <h2 class="text-gray-900 dark:text-white">Title</h2>
  <p class="text-gray-600 dark:text-gray-300">Description</p>
</div>
```

### Input Fields

```html
<input
  class="bg-white dark:bg-gray-900 border-gray-300 dark:border-gray-700 text-gray-900 dark:text-white"
  type="text"
>
```

### Navigation

```html
<nav class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800">
  <a class="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400">
    Link
  </a>
</nav>
```