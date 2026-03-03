# Tailwind CSS Typography Plugin

## Installation

```bash
npm install -D @tailwindcss/typography
```

## Configuration

```js
module.exports = {
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
```

## Usage

Add the `prose` class to any vanilla HTML:

```html
<article class="prose lg:prose-xl">
  <h1>Garlic bread with cheese: What the science tells us</h1>
  <p>
    For years parents have espoused the health benefits of eating garlic bread with cheese to their
    children, with the food earning such an iconic status in our culture that kids will often dress
    up as warm, cheesy loaf for Halloween.
  </p>
  <p>
    But a recent study shows that the celebrated appetizer may be linked to a series of rabies cases
    springing up around the country.
  </p>
</article>
```

## Size Modifiers

```html
<article class="prose prose-sm">Small</article>
<article class="prose">Base (default)</article>
<article class="prose prose-lg">Large</article>
<article class="prose prose-xl">Extra Large</article>
<article class="prose prose-2xl">2X Large</article>
```

## Color Themes

```html
<article class="prose prose-slate">Slate</article>
<article class="prose prose-gray">Gray</article>
<article class="prose prose-zinc">Zinc</article>
<article class="prose prose-neutral">Neutral</article>
<article class="prose prose-stone">Stone</article>
```

## Dark Mode

```html
<article class="prose dark:prose-invert">
  Content that adapts to dark mode
</article>
```

## Element Modifiers

Target specific elements within prose:

```html
<article class="prose prose-img:rounded-xl prose-headings:underline prose-a:text-blue-600">
  <!-- Images will be rounded -->
  <!-- Headings will be underlined -->
  <!-- Links will be blue -->
</article>
```

Available element modifiers:
- `prose-headings:{utility}`
- `prose-h1:{utility}`
- `prose-h2:{utility}`
- `prose-h3:{utility}`
- `prose-h4:{utility}`
- `prose-p:{utility}`
- `prose-a:{utility}`
- `prose-blockquote:{utility}`
- `prose-figure:{utility}`
- `prose-figcaption:{utility}`
- `prose-strong:{utility}`
- `prose-em:{utility}`
- `prose-code:{utility}`
- `prose-pre:{utility}`
- `prose-ol:{utility}`
- `prose-ul:{utility}`
- `prose-li:{utility}`
- `prose-table:{utility}`
- `prose-thead:{utility}`
- `prose-tr:{utility}`
- `prose-th:{utility}`
- `prose-td:{utility}`
- `prose-img:{utility}`
- `prose-video:{utility}`
- `prose-hr:{utility}`

## Customization

Customize the typography styles in your config:

```js
module.exports = {
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            color: '#333',
            a: {
              color: '#3182ce',
              '&:hover': {
                color: '#2c5282',
              },
            },
          },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
```

## Removing Prose Styles

Use `not-prose` to exclude elements:

```html
<article class="prose">
  <h1>My Heading</h1>
  <p>This will be styled by prose.</p>
  <div class="not-prose">
    <!-- This won't be styled by prose -->
    <button class="bg-blue-500">Custom Button</button>
  </div>
</article>
```