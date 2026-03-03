# Tailwind CSS Forms Plugin

## Installation

```bash
npm install -D @tailwindcss/forms
```

## Configuration

```js
module.exports = {
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
```

## What It Does

The Forms plugin provides a basic reset for form styles that makes form elements easy to override with utilities.

### Before (Browser Default)

Form elements have inconsistent styling across browsers.

### After (With Plugin)

All form elements have a consistent, minimal style that's easy to customize.

## Basic Usage

Once installed, all form elements automatically get the base styles:

```html
<input type="text" class="rounded-lg border-gray-300">
<input type="email" class="rounded-lg border-gray-300">
<select class="rounded-lg border-gray-300">
  <option>Option 1</option>
</select>
<textarea class="rounded-lg border-gray-300"></textarea>
```

## Checkboxes and Radio Buttons

```html
<input type="checkbox" class="rounded text-blue-600">
<input type="radio" class="text-blue-600">
```

## Customizing Colors

```html
<input type="checkbox" class="rounded text-pink-500 focus:ring-pink-500">
<input type="radio" class="text-green-500 focus:ring-green-500">
```

## Form Layout Example

```html
<form class="space-y-4">
  <div>
    <label class="block text-sm font-medium text-gray-700">Email</label>
    <input
      type="email"
      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
    >
  </div>

  <div>
    <label class="block text-sm font-medium text-gray-700">Message</label>
    <textarea
      rows="4"
      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
    ></textarea>
  </div>

  <div class="flex items-center">
    <input
      type="checkbox"
      class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
    >
    <label class="ml-2 block text-sm text-gray-900">
      I agree to the terms
    </label>
  </div>

  <button
    type="submit"
    class="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
  >
    Submit
  </button>
</form>
```

## Strategy Option

Choose between two strategies:

### Base Strategy (Default)

Applies styles globally to all form elements:

```js
module.exports = {
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
```

### Class Strategy

Only applies styles when you use the `form-*` classes:

```js
module.exports = {
  plugins: [
    require('@tailwindcss/forms')({
      strategy: 'class',
    }),
  ],
}
```

Usage with class strategy:

```html
<input type="email" class="form-input rounded-lg">
<select class="form-select rounded-lg">
  <option>Option 1</option>
</select>
<textarea class="form-textarea rounded-lg"></textarea>
<input type="checkbox" class="form-checkbox rounded">
<input type="radio" class="form-radio">
```

## Removing Styles

If using the base strategy, use `appearance-none` to remove the plugin styles:

```html
<input type="text" class="appearance-none">
```