---
name: ahooks
description: A high-quality React Hooks library for common business scenarios. Use when building React applications with data fetching, state management, DOM manipulation, and side effects.
metadata:
  author: woic
  version: "2026.2.6"
  source: Generated from https://ahooks.js.org
---

# ahooks

ahooks is a high-quality and reliable React Hooks library that provides a comprehensive collection of practical hooks covering state management, side effects, DOM manipulation, network requests, and other common business scenarios.

> The skill is based on ahooks v3.9.6+, generated at 2026-02-06.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| useRequest | Powerful async data fetching hook with caching, polling, debouncing, throttling | [core-use-request](references/core-use-request.md) |
| useAntdTable | Table data management hook integrated with Ant Design Table component | [core-use-antd-table](references/core-use-antd-table.md) |

## State Hooks

| Hook | Description | Usage |
|------|-------------|-------|
| useBoolean | Boolean state management | `const [state, { toggle, setTrue, setFalse }] = useBoolean(defaultValue)` |
| useCounter | Counter state management | `const [current, { inc, dec, set, reset }] = useCounter(initialValue, options)` |
| useToggle | Toggle state management | `const [state, { toggle, setLeft, setRight }] = useToggle(defaultValue, reverseValue)` |
| useSetState | Object state management, similar to setState | `const [state, setState] = useSetState(initialState)` |
| useLocalStorageState | State persisted to localStorage | `const [state, setState] = useLocalStorageState(key, defaultValue)` |
| useSessionStorageState | State persisted to sessionStorage | `const [state, setState] = useSessionStorageState(key, defaultValue)` |
| useMap / useSet | Map and Set data structure state management | `const [map, { set, get, remove, reset }] = useMap(initialMap)` / `const [set, { add, remove, reset }] = useSet(initialSet)` |

## Effect Hooks

| Hook | Description | Usage |
|------|-------------|-------|
| useUpdateEffect | useEffect that ignores first execution | `useUpdateEffect(effect, deps)` - Only executes when deps update |
| useDebounceEffect | Debounced useEffect | `useDebounceEffect(effect, deps, options)` - `options: { wait: number }` |
| useThrottleEffect | Throttled useEffect | `useThrottleEffect(effect, deps, options)` - `options: { wait: number }` |
| useDeepCompareEffect | useEffect with deep comparison of dependencies | `useDeepCompareEffect(effect, deps)` - Uses deep comparison to detect dependency changes |

## DOM Hooks

| Hook | Description | Usage |
|------|-------------|-------|
| useEventListener | Event listener management | `useEventListener(eventName, handler, target, options)` |
| useClickAway | Trigger on click outside area | `useClickAway(onClickAway, target, eventName)` |
| useHover | Mouse hover state | `const isHovering = useHover(target)` |
| useScroll | Scroll position and state | `const position = useScroll(target, shouldUpdate)` |
| useSize | Element size monitoring | `const size = useSize(target)` |
| useFullscreen | Fullscreen operations | `const { isFullscreen, enterFullscreen, exitFullscreen, toggleFullscreen } = useFullscreen(target)` |

## Advanced Hooks

| Hook | Description | Usage |
|------|-------------|-------|
| useInfiniteScroll | Infinite scroll loading | `const { data, loading, loadMore, noMore } = useInfiniteScroll(service, options)` |
| useVirtualList | Virtual list optimization | `const { list, scrollTo } = useVirtualList(dataSource, options)` |
| useWebSocket | WebSocket connection management | `const { readyState, latestMessage, sendMessage, disconnect, connect } = useWebSocket(url, options)` |
| useNetwork | Network state monitoring | `const networkState = useNetwork()` - Returns `{ online, effectiveType, downlink, rtt }` |

## Key Recommendations

- **Prefer useRequest** - Handle all async data fetching scenarios
- **useAntdTable for tables** - Use with Ant Design Table component
- **Choose appropriate state hooks** - Select useBoolean, useCounter, useSetState based on scenarios
- **Use dedicated DOM hooks** - useEventListener, useClickAway simplify DOM operations
- **Manage dependencies carefully** - Use useDeepCompareEffect for object dependencies
