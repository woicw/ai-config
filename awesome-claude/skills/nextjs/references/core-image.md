---
name: nextjs-image
description: Next.js Image component for optimized images. Use when displaying images in your application.
---

# Image Component

The Next.js Image component extends the HTML `<img>` element for automatic image optimization.

## Basic Usage

```tsx
import Image from 'next/image'

export default function Page() {
  return (
    <Image
      src="/profile.png"
      width={500}
      height={500}
      alt="Picture of the author"
    />
  )
}
```

## Required Props

### `src`

The source of the image. Can be one of the following:

- An internal path string: `<Image src="/profile.png" />`
- An absolute external URL (must be configured with `remotePatterns`)
- A static import: `import profile from './profile.png'`

### `alt`

The `alt` property is used to describe the image for screen readers and search engines. If the image is purely decorative, the `alt` property should be an empty string.

### `width` and `height`

The `width` and `height` properties represent the [intrinsic](https://developer.mozilla.org/en-US/docs/Glossary/Intrinsic_Size) image size in pixels. Used to infer the correct **aspect ratio** used by browsers to reserve space for the image.

```tsx
<Image src="/profile.png" width={500} height={500} />
```

You **must** set both `width` and `height` properties unless:
- The image is statically imported
- The image has the `fill` property

## Common Props

### `fill`

A boolean that causes the image to expand to the size of the parent element.

```tsx
<div style={{ position: 'relative' }}>
  <Image src="/profile.png" fill />
</div>
```

**Positioning**:
- The parent element **must** assign `position: "relative"`, `"fixed"`, or `"absolute"`
- By default, the `<img>` element uses `position: "absolute"`

### `sizes`

Define the sizes of the image at different breakpoints. Used by the browser to choose the most appropriate size from the generated `srcset`.

```tsx
<Image
  fill
  src="/example.png"
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
/>
```

### `quality`

An integer between `1` and `100` that sets the quality of the optimized image. Default value is 75.

```tsx
<Image quality={80} src="/profile.png" width={500} height={500} />
```

### `placeholder`

Specifies a placeholder to use while the image is loading.

- `empty`: No placeholder while the image is loading
- `blur`: Use a blurred version of the image as a placeholder (must be used with the `blurDataURL` property)
- `data:image/...`: Uses the [Data URL](https://developer.mozilla.org/docs/Web/HTTP/Basics_of_HTTP/Data_URIs) as the placeholder

```tsx
<Image
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
  src="/profile.png"
  width={500}
  height={500}
/>
```

### `loading`

Controls when the image should start loading.

- `lazy` (default): Defer loading the image until it reaches a calculated distance from the viewport
- `eager`: Load the image immediately, regardless of its position in the page

```tsx
<Image loading="eager" src="/profile.png" width={500} height={500} />
```

### `preload`

A boolean that indicates if the image should be preloaded.

```tsx
<Image preload={true} src="/hero.png" width={500} height={500} />
```

**When to use it**:
- The image is the Largest Contentful Paint (LCP) element
- The image is above the fold, typically the hero image
- You want to begin loading the image in the `<head>`

## Configuration Options

Configure the Image Component in `next.config.js`:

### `remotePatterns`

Allow images from specific external paths and block all others.

```js
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
        port: '',
        pathname: '/account123/**',
      },
    ],
  },
}
```

### `localPatterns`

Allow images from specific local paths and block all others.

```js
module.exports = {
  images: {
    localPatterns: [
      {
        pathname: '/assets/images/**',
        search: '',
      },
    ],
  },
}
```

## Key Points

- **Automatic optimization** - Next.js automatically optimizes images (resizing, format conversion, etc.)
- **Responsive** - Use `fill` and `sizes` to create responsive images
- **Lazy loading** - Images are lazy-loaded by default
- **Format support** - Automatically provides WebP and AVIF formats (if browser supports)
- **Layout shift** - Avoid layout shift by setting `width` and `height`

## Examples

### Responsive images

```tsx
import Image from 'next/image'
import mountains from '../public/mountains.jpg'

export default function Responsive() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      <Image
        alt="Mountains"
        src={mountains}
        sizes="100vw"
        style={{
          width: '100%',
          height: 'auto',
        }}
      />
    </div>
  )
}
```

### Responsive image with `fill`

```tsx
<div style={{ position: 'relative', width: '400px' }}>
  <Image
    alt="Mountains"
    src={mountains}
    fill
    sizes="(min-width: 808px) 50vw, 100vw"
    style={{
      objectFit: 'cover',
    }}
  />
</div>
```

### Remote images

```tsx
<Image
  src="https://s3.amazonaws.com/my-bucket/profile.png"
  alt="Picture of the author"
  width={500}
  height={500}
/>
```

<!--
Source references:
- https://nextjs.org/docs/app/api-reference/components/image
-->
