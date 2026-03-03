# Tailwind CSS Directives

## @tailwind

Use `@tailwind` to insert Tailwind's styles into your CSS:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## @layer

Add custom styles to Tailwind's layers:

### Base Layer

```css
@layer base {
  h1 {
    @apply text-2xl font-bold;
  }
  a {
    @apply text-blue-600 underline;
  }
}
```

### Components Layer

```css
@layer components {
  .btn-primary {
    @apply py-2 px-4 bg-blue-500 text-white rounded-lg hover:bg-blue-700;
  }
  .card {
    @apply bg-white rounded-lg shadow-md p-6;
  }
}
```

### Utilities Layer

```css
@layer utilities {
  .content-auto {
    content-visibility: auto;
  }
  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
}
```

## @apply

Extract repeated utility patterns into custom classes:

```css
.btn {
  @apply px-4 py-2 rounded-lg font-semibold;
}

.btn-primary {
  @apply btn bg-blue-500 text-white hover:bg-blue-700;
}

.btn-secondary {
  @apply btn bg-gray-500 text-white hover:bg-gray-700;
}
```

### With Modifiers

```css
.input {
  @apply border rounded px-3 py-2;
  @apply focus:outline-none focus:ring-2 focus:ring-blue-500;
}
```

### Important Modifier

```css
.btn {
  @apply px-4 py-2 !font-bold;
}
```

## @config

Specify which config file to use:

```css
@config "./tailwind.site.config.js";

@tailwind base;
@tailwind components;
@tailwind utilities;
```

## @import

Import other CSS files:

```css
@import "tailwindcss/base";
@import "./custom-base.css";
@import "tailwindcss/components";
@import "./custom-components.css";
@import "tailwindcss/utilities";
```

## theme()

Reference theme values in custom CSS:

```css
.content {
  background-color: theme('colors.blue.500');
  padding: theme('spacing.4');
  border-radius: theme('borderRadius.lg');
}
```

### With Default Values

```css
.custom {
  color: theme('colors.brand', #3490dc);
}
```

## screen()

Create media queries using configured breakpoints:

```css
@media screen(md) {
  .custom {
    /* Styles for md breakpoint and up */
  }
}
```

## Arbitrary Variants

Create one-off variants:

```css
@layer utilities {
  @variants hover, focus {
    .filter-none {
      filter: none;
    }
  }
}
```