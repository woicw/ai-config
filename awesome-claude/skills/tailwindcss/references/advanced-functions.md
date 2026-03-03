# Tailwind CSS Functions & Expressions

## Arbitrary Values

Use square brackets to use arbitrary values for any utility:

### Arbitrary Sizes

```html
<div class="w-[300px] h-[200px]">
  Custom dimensions
</div>
```

### Arbitrary Colors

```html
<div class="bg-[#1da1f2] text-[rgb(123,31,162)]">
  Custom colors
</div>
```

### Arbitrary Spacing

```html
<div class="m-[13px] p-[17px]">
  Custom spacing
</div>
```

### CSS Variables

```html
<div class="bg-[var(--brand-color)] text-[length:var(--font-size)]">
  Using CSS variables
</div>
```

## theme() Function

Reference design tokens from your Tailwind config:

### In CSS

```css
.custom {
  color: theme('colors.blue.500');
  padding: theme('spacing.4');
  font-size: theme('fontSize.xl');
  border-radius: theme('borderRadius.lg');
}
```

### With Arbitrary Values

```html
<div class="bg-[theme(colors.blue.500)]">
  Using theme in arbitrary values
</div>
```

### With Default Values

```css
.custom {
  color: theme('colors.brand', #3490dc);
}
```

## Arbitrary Properties

Use arbitrary CSS properties:

```html
<div class="[mask-type:luminance]">
  Custom CSS property
</div>

<div class="[--scroll-offset:56px]">
  CSS custom property
</div>
```

## Arbitrary Variants

Create custom variant conditions:

```html
<div class="[@media(any-hover:hover){&:hover}]:opacity-100">
  Custom media query
</div>

<div class="[@supports(display:grid)]:grid">
  Feature query
</div>

<div class="[&:nth-child(3)]:bg-blue-500">
  Custom selector
</div>
```

### Parent Selectors

```html
<div class="[.dark_&]:bg-gray-900">
  When parent has .dark class
</div>
```

### Sibling Selectors

```html
<div class="[&+div]:mt-4">
  Next sibling div
</div>
```

## Calc() Expressions

Use calc() in arbitrary values:

```html
<div class="w-[calc(100%-2rem)]">
  Calculated width
</div>

<div class="h-[calc(100vh-64px)]">
  Viewport height minus header
</div>
```

## Color Opacity Modifiers

Adjust opacity of colors:

```html
<div class="bg-blue-500/50">
  50% opacity
</div>

<div class="text-red-600/75">
  75% opacity
</div>

<div class="border-gray-300/[0.37]">
  Arbitrary opacity
</div>
```

## Space-Separated Values

Use underscores for spaces in arbitrary values:

```html
<div class="grid-cols-[1fr_500px_2fr]">
  Grid template columns
</div>

<div class="bg-[url('/img/hero.jpg')]">
  Background image
</div>
```

## Important Modifier

Make any utility important:

```html
<div class="!font-bold">
  Important font weight
</div>

<div class="!m-0">
  Important margin
</div>
```

## Negative Values

Use negative values with a minus prefix:

```html
<div class="-mt-4">
  Negative margin
</div>

<div class="-translate-x-1/2">
  Negative transform
</div>
```