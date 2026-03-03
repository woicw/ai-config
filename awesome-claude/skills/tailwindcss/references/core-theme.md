# Tailwind CSS Theme Configuration

## Theme Structure

The `theme` section defines your design system including colors, spacing, typography, breakpoints, and more.

### Extending the Theme

Use `theme.extend` to add to the default theme without replacing it:

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        'brand': '#3490dc',
      },
      spacing: {
        '128': '32rem',
      }
    }
  }
}
```

### Overriding the Theme

Define values directly in `theme` to replace defaults:

```js
module.exports = {
  theme: {
    colors: {
      // This replaces all default colors
      primary: '#3490dc',
      secondary: '#ffed4e',
    }
  }
}
```

## Colors

### Custom Colors

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        'brand-blue': '#1fb6ff',
        'brand-purple': '#7e5bef',
        'brand-pink': '#ff49db',
      }
    }
  }
}
```

### Color Shades

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          900: '#0c4a6e',
        }
      }
    }
  }
}
```

## Spacing

Customize spacing scale for padding, margin, width, height, etc:

```js
module.exports = {
  theme: {
    extend: {
      spacing: {
        '128': '32rem',
        '144': '36rem',
      }
    }
  }
}
```

## Typography

### Font Family

```js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        serif: ['Merriweather', 'serif'],
        mono: ['Fira Code', 'monospace'],
      }
    }
  }
}
```

### Font Size

```js
module.exports = {
  theme: {
    extend: {
      fontSize: {
        'xxs': '0.625rem',
        '10xl': '10rem',
      }
    }
  }
}
```

### Font Weight

```js
module.exports = {
  theme: {
    extend: {
      fontWeight: {
        'extra-light': 200,
        'extra-bold': 800,
      }
    }
  }
}
```

## Breakpoints

Customize responsive breakpoints:

```js
module.exports = {
  theme: {
    screens: {
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px',
    }
  }
}
```

### Custom Breakpoints

```js
module.exports = {
  theme: {
    extend: {
      screens: {
        '3xl': '1920px',
        'tablet': '640px',
        'laptop': '1024px',
        'desktop': '1280px',
      }
    }
  }
}
```

## Other Theme Options

### Border Radius

```js
module.exports = {
  theme: {
    extend: {
      borderRadius: {
        '4xl': '2rem',
      }
    }
  }
}
```

### Box Shadow

```js
module.exports = {
  theme: {
    extend: {
      boxShadow: {
        '3xl': '0 35px 60px -15px rgba(0, 0, 0, 0.3)',
      }
    }
  }
}
```

### Z-Index

```js
module.exports = {
  theme: {
    extend: {
      zIndex: {
        '100': '100',
      }
    }
  }
}
```

## Referencing Theme Values

Use the `theme()` function in CSS:

```css
.custom {
  color: theme('colors.brand-blue');
  padding: theme('spacing.4');
}
```
