---
name: tailwindcss
description: Tailwind CSS utility-first CSS framework. Use when configuring Tailwind, writing utility classes, customizing theme, or working with plugins and directives.
metadata:
  author: woic
  version: "2026.3.3"
  source: Generated from Tailwind CSS official documentation
---

Tailwind CSS is a utility-first CSS framework for rapidly building custom user interfaces. It provides low-level utility classes that let you build completely custom designs without ever leaving your HTML.

**Important:** Before writing Tailwind CSS code, agents should check for `tailwind.config.js`, `tailwind.config.ts`, or `tailwind.config.mjs` files in the project root to understand the theme customization, plugins, and content paths. If the project setup is unclear, stick to basic utility classes from the default configuration.

> The skill is based on Tailwind CSS v3.x and v4.x, generated at 2026-03-03.

## Core Concepts

| Topic | Description | Reference |
|-------|-------------|-----------|
| Configuration | Config file setup and customization options | [core-config](references/core-config.md) |
| Theme | Customizing colors, spacing, typography, and design tokens | [core-theme](references/core-theme.md) |
| Utility Classes | Core utility classes for layout, typography, colors, etc. | [core-utilities](references/core-utilities.md) |
| Responsive Design | Breakpoints and responsive modifiers | [core-responsive](references/core-responsive.md) |
| Hover, Focus & States | Pseudo-class variants for interactive states | [core-states](references/core-states.md) |
| Dark Mode | Dark mode implementation strategies | [core-dark-mode](references/core-dark-mode.md) |

## Advanced Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Directives | @apply, @layer, @config, and other directives | [advanced-directives](references/advanced-directives.md) |
| Functions & Expressions | theme(), screen(), and arbitrary values | [advanced-functions](references/advanced-functions.md) |
| Plugins | Official and custom plugin system | [advanced-plugins](references/advanced-plugins.md) |
| Content Configuration | Configuring content sources for class detection | [advanced-content](references/advanced-content.md) |

## Official Plugins

| Topic | Description | Reference |
|-------|-------------|-----------|
| Typography | Beautiful typographic defaults with prose classes | [plugin-typography](references/plugin-typography.md) |
| Forms | Better form element styling | [plugin-forms](references/plugin-forms.md) |
| Aspect Ratio | Composable aspect ratio utilities | [plugin-aspect-ratio](references/plugin-aspect-ratio.md) |
| Container Queries | Container query utilities | [plugin-container-queries](references/plugin-container-queries.md) |

## Integrations

| Topic | Description | Reference |
|-------|-------------|-----------|
| Vite Integration | Setting up Tailwind CSS with Vite | [integrations-vite](references/integrations-vite.md) |
| Next.js Integration | Tailwind CSS in Next.js applications | [integrations-nextjs](references/integrations-nextjs.md) |
| PostCSS Integration | Using Tailwind as a PostCSS plugin | [integrations-postcss](references/integrations-postcss.md) |
