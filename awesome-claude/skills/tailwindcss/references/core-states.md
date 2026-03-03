# Tailwind CSS Hover, Focus & Other States

## Pseudo-Class Variants

Tailwind provides variants for styling elements based on their state.

### Hover

```html
<button class="bg-blue-500 hover:bg-blue-700">
  Hover me
</button>
```

### Focus

```html
<input class="border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200">
```

### Active

```html
<button class="bg-blue-500 active:bg-blue-800">
  Click me
</button>
```

### Disabled

```html
<button class="bg-blue-500 disabled:bg-gray-300 disabled:cursor-not-allowed" disabled>
  Disabled
</button>
```

### Focus Within

```html
<div class="border-gray-300 focus-within:border-blue-500">
  <input type="text">
</div>
```

### Focus Visible

```html
<button class="focus-visible:ring-2 focus-visible:ring-blue-500">
  Keyboard focus only
</button>
```

## Group Variants

Style an element based on parent state:

```html
<div class="group">
  <img src="..." class="group-hover:opacity-75">
  <p class="group-hover:text-blue-500">Hover the parent</p>
</div>
```

### Named Groups

```html
<div class="group/card">
  <div class="group/item">
    <p class="group-hover/card:text-blue-500 group-hover/item:text-red-500">
      Different hover targets
    </p>
  </div>
</div>
```

## Peer Variants

Style an element based on sibling state:

```html
<input type="checkbox" class="peer" />
<label class="peer-checked:text-blue-500">
  Check the box
</label>
```

### Named Peers

```html
<input type="checkbox" class="peer/draft" />
<input type="checkbox" class="peer/published" />
<span class="peer-checked/draft:text-gray-500 peer-checked/published:text-green-500">
  Status
</span>
```

## Form States

### Placeholder

```html
<input class="placeholder:text-gray-400" placeholder="Enter text...">
```

### Required

```html
<input class="required:border-red-500" required>
```

### Valid & Invalid

```html
<input class="valid:border-green-500 invalid:border-red-500" type="email">
```

### Checked

```html
<input type="checkbox" class="checked:bg-blue-500">
```

## First, Last, Odd, Even

```html
<ul>
  <li class="first:font-bold">First item</li>
  <li class="last:font-bold">Last item</li>
  <li class="odd:bg-gray-100">Odd items</li>
  <li class="even:bg-white">Even items</li>
</ul>
```

## Before & After

```html
<div class="before:content-['→'] before:mr-2">
  With arrow
</div>

<div class="after:content-['*'] after:text-red-500">
  Required field
</div>
```

## Combining Variants

Stack multiple variants:

```html
<button class="bg-blue-500 hover:bg-blue-700 focus:ring-2 focus:ring-blue-300 active:bg-blue-800 disabled:bg-gray-300">
  Multi-state button
</button>
```

Combine with responsive:

```html
<button class="md:hover:bg-blue-700">
  Hover only on medium screens and up
</button>
```