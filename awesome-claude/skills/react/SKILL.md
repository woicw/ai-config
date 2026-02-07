---
name: react
description: React JavaScript library for building user interfaces. Use when building React components, working with hooks (useState, useEffect, useContext, useReducer, useMemo, useCallback, useRef), or implementing React patterns.
metadata:
  author: woic
  version: "2026.2.5"
  source: Generated from https://react.dev
---

# React

React is a JavaScript library for building user interfaces with reusable components. It uses a declarative approach with hooks for state management and side effects. The functional component pattern with hooks and TypeScript is the recommended approach for building React applications.

> The skill is based on React 18/19+, generated at 2026-02-05.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Components & JSX | Functional components, JSX syntax, props, composition | [core-components](references/core-components.md) |
| State Management | useState hook, state updates, batching, functional updates | [core-state](references/core-state.md) |

## Hooks

| Topic | Description | Reference |
|-------|-------------|-----------|
| useEffect | Side effects, cleanup, dependencies, lifecycle equivalents | [hooks-use-effect](references/hooks-use-effect.md) |
| useContext | Context API, provider/consumer pattern, dependency injection | [hooks-use-context](references/hooks-use-context.md) |
| useReducer | Complex state management, reducers, actions, dispatch | [hooks-use-reducer](references/hooks-use-reducer.md) |
| useRef & Imperative | DOM refs, mutable values, useImperativeHandle, forwardRef | [hooks-use-ref](references/hooks-use-ref.md) |
| Performance Hooks | React Compiler (recommended), useMemo, useCallback, React.memo | [hooks-performance](references/hooks-performance.md) |
| Custom Hooks | Reusable logic, composition, naming conventions | [hooks-custom](references/hooks-custom.md) |

## Patterns

| Topic | Description | Reference |
|-------|-------------|-----------|
| Lists & Keys | Rendering arrays, key prop, unique identifiers | [patterns-lists-keys](references/patterns-lists-keys.md) |
| Conditional Rendering | Ternary operators, && operator, early returns | [patterns-conditional](references/patterns-conditional.md) |
| Forms & Inputs | Controlled components, form handling, validation | [patterns-forms](references/patterns-forms.md) |

## TypeScript

| Topic | Description | Reference |
|-------|-------------|-----------|
| TypeScript with React | Typing props, state, hooks, children, events | [typescript](references/typescript.md) |

## Key Recommendations

- **Use React Compiler** - enables automatic performance optimizations (React 19+)
- **Use functional components with hooks** - avoid class components
- **Prefer useState for simple state** - use useReducer for complex state
- **Always specify dependency arrays** for useEffect, useMemo, useCallback
- **With React Compiler: write code naturally** - compiler handles most optimizations automatically
- **Without React Compiler: use useCallback** for stable function references passed to memoized children
- **Use keys from data (IDs)** - avoid array indices as keys
- **Keep effects focused** - one effect per concern
- **Extract custom hooks** for reusable stateful logic
- **Use TypeScript** for type safety and better DX
- **Follow hooks rules** - only call at top level, only in function components
