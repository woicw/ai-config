# Tailwind CSS Responsive Design

## Breakpoint Prefixes

Tailwind uses a mobile-first breakpoint system. Apply utilities at specific breakpoints using responsive prefixes:

```html
<!-- Width of 16 by default, 32 on medium screens, and 48 on large screens -->
<img class="w-16 md:w-32 lg:w-48" src="...">
```

## Default Breakpoints

| Prefix | Minimum Width | CSS |
|--------|---------------|-----|
| `sm` | 640px | `@media (min-width: 640px) { ... }` |
| `md` | 768px | `@media (min-width: 768px) { ... }` |
| `lg` | 1024px | `@media (min-width: 1024px) { ... }` |
| `xl` | 1280px | `@media (min-width: 1280px) { ... }` |
| `2xl` | 1536px | `@media (min-width: 1536px) { ... }` |

## Usage Examples

### Responsive Layout

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <!-- Mobile: 1 column, Tablet: 2 columns, Desktop: 3 columns -->
</div>
```

### Responsive Typography

```html
<h1 class="text-2xl md:text-4xl lg:text-6xl">
  Responsive Heading
</h1>
```

### Responsive Spacing

```html
<div class="p-4 md:p-6 lg:p-8">
  Content with responsive padding
</div>
```

### Responsive Display

```html
<!-- Hidden on mobile, visible on desktop -->
<div class="hidden lg:block">
  Desktop only content
</div>

<!-- Visible on mobile, hidden on desktop -->
<div class="block lg:hidden">
  Mobile only content
</div>
```

## Targeting a Single Breakpoint

Use `max-*` variants to target a specific range:

```html
<!-- Only applies between md and lg -->
<div class="md:max-lg:text-center">
  ...
</div>
```

## Custom Breakpoints

Define custom breakpoints in your config:

```js
module.exports = {
  theme: {
    screens: {
      'tablet': '640px',
      'laptop': '1024px',
      'desktop': '1280px',
    },
  },
}
```

Usage:

```html
<div class="tablet:text-center laptop:text-left">
  ...
</div>
```