# Tailwind CSS Container Queries Plugin

## Installation

```bash
npm install -D @tailwindcss/container-queries
```

## Configuration

```js
module.exports = {
  plugins: [
    require('@tailwindcss/container-queries'),
  ],
}
```

## Usage

Use the `@container` utility to create a container and query it with `@{size}:` variants:

```html
<div class="@container">
  <div class="@lg:text-xl">
    This text will be xl when the container is large
  </div>
</div>
```

## Container Sizes

Default container query breakpoints:

| Variant | Minimum Width |
|---------|---------------|
| `@xs` | 20rem (320px) |
| `@sm` | 24rem (384px) |
| `@md` | 28rem (448px) |
| `@lg` | 32rem (512px) |
| `@xl` | 36rem (576px) |
| `@2xl` | 42rem (672px) |
| `@3xl` | 48rem (768px) |
| `@4xl` | 56rem (896px) |
| `@5xl` | 64rem (1024px) |
| `@6xl` | 72rem (1152px) |
| `@7xl` | 80rem (1280px) |

## Basic Example

```html
<div class="@container">
  <div class="grid grid-cols-1 @md:grid-cols-2 @lg:grid-cols-3 gap-4">
    <div>Item 1</div>
    <div>Item 2</div>
    <div>Item 3</div>
  </div>
</div>
```

## Named Containers

Create named containers for nested container queries:

```html
<div class="@container/main">
  <div class="@container/sidebar">
    <div class="@lg/main:text-xl @md/sidebar:text-lg">
      Responds to both containers
    </div>
  </div>
</div>
```

## Responsive Card Example

```html
<div class="@container">
  <div class="flex flex-col @md:flex-row gap-4 p-4">
    <img src="image.jpg" class="w-full @md:w-1/3 rounded-lg">
    <div class="flex-1">
      <h2 class="text-lg @md:text-xl @lg:text-2xl font-bold">Title</h2>
      <p class="text-sm @md:text-base">Description</p>
    </div>
  </div>
</div>
```

## Container Type

By default, `@container` queries both width and height. You can specify the type:

```html
<!-- Query only width (default) -->
<div class="@container">...</div>

<!-- Query only height -->
<div class="@container-normal">...</div>
```

## Combining with Media Queries

```html
<div class="@container">
  <div class="text-base md:text-lg @lg:text-xl">
    <!-- Responds to both viewport and container size -->
  </div>
</div>
```

## Custom Container Sizes

Customize container query breakpoints in your config:

```js
module.exports = {
  theme: {
    extend: {
      containers: {
        '8xl': '88rem',
        '9xl': '96rem',
      },
    },
  },
  plugins: [
    require('@tailwindcss/container-queries'),
  ],
}
```

## Practical Use Cases

### Responsive Component Library

```html
<div class="@container">
  <article class="p-4 @md:p-6 @lg:p-8">
    <h1 class="text-xl @md:text-2xl @lg:text-3xl">Heading</h1>
    <div class="grid grid-cols-1 @md:grid-cols-2 gap-4">
      <div>Content 1</div>
      <div>Content 2</div>
    </div>
  </article>
</div>
```

### Sidebar Layout

```html
<div class="flex">
  <aside class="w-64 @container/sidebar">
    <nav class="@md/sidebar:block hidden">
      <!-- Navigation items -->
    </nav>
  </aside>
  <main class="flex-1 @container/main">
    <!-- Main content -->
  </main>
</div>
```