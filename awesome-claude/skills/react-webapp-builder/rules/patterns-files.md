---
name: patterns-files
description: File and folder naming conventions, component directory layout, and unified named exports
---

# File Naming & Export Patterns

## 1. Naming Rules

- All file and folder names must use `kebab-case`.
- Do not use `PascalCase` or `camelCase` for filenames.
- Use explicit, business-meaningful names:
  - `order-list.tsx`
  - `user-service.ts`
  - `auth-store.ts`

## 2. Component File Layout

- A component must be represented by a folder.
- Component folder name must be `kebab-case`.
- Component entry must be `index.tsx`.
- Recommended: expose public API through parent/module-level `index.ts`.

Example:

```txt
src/pages/order-list/
├── components/
│   └── order-table/
│       ├── hooks/
│       │   └── use-order-table.ts
│       └── index.tsx
├── hooks/
│   └── use-order-list.ts
├── index.ts
└── index.tsx
```

## 3. Export Rules

- Prefer named exports everywhere (`export const`, `export function`, `export type`).
- Avoid `export default`.
- Use barrel export (`index.ts`) as stable external entry.

```tsx
// components/order-table/index.tsx
export function OrderTable() {
  return <div>...</div>;
}
```

```ts
// pages/order-list/index.ts
export { OrderTable } from './components/order-table';
```

## 4. Strict Mode (Optional)

- Page folder should contain: `index.tsx`, `components/`, `hooks/`, `services/`, `types.ts`.
- Hook files must follow `use-*.ts` naming.
- Service files must follow `*-service.ts` naming.
- Store files must follow `*-store.ts` naming.
- Avoid deep relative imports (e.g. `../../../`); use barrel export or alias paths.

## 5. Recommended ESLint Constraints

- Enforce no default export: `import/no-default-export`.
- Enforce filename style: `unicorn/filename-case` with kebab-case.
- Limit deep relative import depth via `no-restricted-imports` (project-specific).
