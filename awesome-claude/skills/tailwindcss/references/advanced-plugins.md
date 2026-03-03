# Tailwind CSS Plugins

## Using Plugins

Add plugins to your `tailwind.config.js`:

```js
module.exports = {
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/container-queries'),
  ],
}
```

## Creating Custom Plugins

### Basic Plugin

```js
const plugin = require('tailwindcss/plugin')

module.exports = {
  plugins: [
    plugin(function({ addUtilities, addComponents, e, config }) {
      // Add your custom styles here
    })
  ]
}
```

### Adding Utilities

```js
const plugin = require('tailwindcss/plugin')

module.exports = {
  plugins: [
    plugin(function({ addUtilities }) {
      addUtilities({
        '.content-auto': {
          'content-visibility': 'auto',
        },
        '.content-hidden': {
          'content-visibility': 'hidden',
        },
        '.content-visible': {
          'content-visibility': 'visible',
        },
      })
    })
  ]
}
```

### Adding Components

```js
const plugin = require('tailwindcss/plugin')

module.exports = {
  plugins: [
    plugin(function({ addComponents, theme }) {
      addComponents({
        '.btn': {
          padding: theme('spacing.4'),
          borderRadius: theme('borderRadius.lg'),
          fontWeight: theme('fontWeight.semibold'),
        },
        '.btn-primary': {
          backgroundColor: theme('colors.blue.500'),
          color: theme('colors.white'),
          '&:hover': {
            backgroundColor: theme('colors.blue.700'),
          },
        },
      })
    })
  ]
}
```

### Adding Variants

```js
const plugin = require('tailwindcss/plugin')

module.exports = {
  plugins: [
    plugin(function({ addVariant }) {
      addVariant('third', '&:nth-child(3)')
      addVariant('hocus', ['&:hover', '&:focus'])
      addVariant('supports-grid', '@supports (display: grid)')
    })
  ]
}
```

### Adding Base Styles

```js
const plugin = require('tailwindcss/plugin')

module.exports = {
  plugins: [
    plugin(function({ addBase, theme }) {
      addBase({
        'h1': { fontSize: theme('fontSize.2xl') },
        'h2': { fontSize: theme('fontSize.xl') },
        'h3': { fontSize: theme('fontSize.lg') },
      })
    })
  ]
}
```

### Extending the Theme

```js
const plugin = require('tailwindcss/plugin')

module.exports = {
  plugins: [
    plugin(function({ matchUtilities, theme }) {
      matchUtilities(
        {
          tab: (value) => ({
            tabSize: value
          }),
        },
        { values: theme('tabSize') }
      )
    }, {
      theme: {
        tabSize: {
          1: '1',
          2: '2',
          4: '4',
          8: '8',
        }
      }
    })
  ]
}
```

## Plugin API

### Available Functions

- `addUtilities(utilities, options)` - Add new utility classes
- `addComponents(components, options)` - Add new component classes
- `addBase(baseStyles)` - Add new base styles
- `addVariant(name, definition)` - Add new variants
- `matchUtilities(utilities, options)` - Add utilities that support arbitrary values
- `matchComponents(components, options)` - Add components that support arbitrary values
- `theme(path, defaultValue)` - Look up values in the theme
- `config(path, defaultValue)` - Look up values in the config
- `e(className)` - Escape class names for use in selectors
- `prefix(className)` - Add the user's configured prefix to a selector

### Example: Complex Plugin

```js
const plugin = require('tailwindcss/plugin')

module.exports = {
  plugins: [
    plugin(function({ addUtilities, matchUtilities, theme }) {
      // Static utilities
      addUtilities({
        '.scrollbar-hide': {
          '-ms-overflow-style': 'none',
          'scrollbar-width': 'none',
          '&::-webkit-scrollbar': {
            display: 'none'
          }
        }
      })

      // Dynamic utilities with arbitrary values
      matchUtilities(
        {
          'text-shadow': (value) => ({
            textShadow: value,
          }),
        },
        { values: theme('textShadow') }
      )
    }, {
      theme: {
        textShadow: {
          sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
          DEFAULT: '0 2px 4px rgba(0, 0, 0, 0.1)',
          lg: '0 8px 16px rgba(0, 0, 0, 0.15)',
        }
      }
    })
  ]
}
```