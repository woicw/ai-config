# Tailwind CSS Aspect Ratio Plugin

## Installation

```bash
npm install -D @tailwindcss/aspect-ratio
```

## Configuration

```js
module.exports = {
  plugins: [
    require('@tailwindcss/aspect-ratio'),
  ],
}
```

## Usage

Use the `aspect-w-{n}` and `aspect-h-{n}` utilities to create fixed aspect ratio containers:

```html
<div class="aspect-w-16 aspect-h-9">
  <iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>
```

## Common Aspect Ratios

### 16:9 (Video)

```html
<div class="aspect-w-16 aspect-h-9">
  <img src="video-thumbnail.jpg" alt="Video">
</div>
```

### 4:3 (Standard)

```html
<div class="aspect-w-4 aspect-h-3">
  <img src="photo.jpg" alt="Photo">
</div>
```

### 1:1 (Square)

```html
<div class="aspect-w-1 aspect-h-1">
  <img src="avatar.jpg" alt="Avatar">
</div>
```

### 21:9 (Ultrawide)

```html
<div class="aspect-w-21 aspect-h-9">
  <img src="banner.jpg" alt="Banner">
</div>
```

## Responsive Aspect Ratios

```html
<div class="aspect-w-16 aspect-h-9 md:aspect-w-4 md:aspect-h-3">
  <img src="image.jpg" alt="Responsive aspect ratio">
</div>
```

## With Images

```html
<div class="aspect-w-16 aspect-h-9">
  <img src="image.jpg" class="object-cover" alt="Cover image">
</div>
```

## With Videos

```html
<div class="aspect-w-16 aspect-h-9">
  <video controls>
    <source src="video.mp4" type="video/mp4">
  </video>
</div>
```

## With Iframes

```html
<div class="aspect-w-16 aspect-h-9">
  <iframe src="https://example.com"></iframe>
</div>
```

## Modern Alternative

Note: Modern browsers support the native `aspect-ratio` CSS property. You can use Tailwind's built-in `aspect-*` utilities instead:

```html
<div class="aspect-video">
  <iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ"></iframe>
</div>

<div class="aspect-square">
  <img src="avatar.jpg" alt="Avatar">
</div>

<div class="aspect-[4/3]">
  <img src="photo.jpg" alt="Photo">
</div>
```

Built-in aspect ratio utilities (no plugin needed):
- `aspect-auto` - Auto aspect ratio
- `aspect-square` - 1:1 aspect ratio
- `aspect-video` - 16:9 aspect ratio
- `aspect-[4/3]` - Custom aspect ratio using arbitrary values