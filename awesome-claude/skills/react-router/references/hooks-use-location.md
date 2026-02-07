---
name: react-router-use-location
description: useLocation hook to access current location information. Use when you need pathname, search, state, or key for analytics, scroll restoration, or side effects.
---

# useLocation

The `useLocation` hook returns a `location` object that contains useful information about the current URL. This is useful for analytics, scroll restoration, and other location-based side effects.

## Basic Usage

```tsx
import { useLocation } from "react-router";

function Component() {
  const location = useLocation();
  
  return (
    <div>
      <p>Current path: {location.pathname}</p>
      <p>Search: {location.search}</p>
    </div>
  );
}
```

## Location Object Properties

The location object contains:

```tsx
interface Location {
  pathname: string;  // Path portion of URL
  search: string;     // Query string including ?
  hash: string;       // Hash portion including #
  state: unknown;     // Location state
  key: string;        // Unique key for this location
}
```

## Pathname

Access the current pathname:

```tsx
function Component() {
  const location = useLocation();
  
  return <div>Current path: {location.pathname}</div>;
}
```

## Search

Access the query string:

```tsx
function Component() {
  const location = useLocation();
  
  // location.search includes the "?" prefix
  // e.g., "?tab=1&filter=active"
  const searchParams = new URLSearchParams(location.search);
  const tab = searchParams.get("tab");
  
  return <div>Tab: {tab}</div>;
}
```

## Hash

Access the hash portion:

```tsx
function Component() {
  const location = useLocation();
  
  // location.hash includes the "#" prefix
  // e.g., "#section-1"
  return <div>Hash: {location.hash}</div>;
}
```

## State

Access location state (set via `navigate`):

```tsx
import { useNavigate, useLocation } from "react-router";

function Component() {
  const navigate = useNavigate();
  const location = useLocation();
  
  const handleNavigate = () => {
    navigate("/other", { state: { from: "home" } });
  };
  
  // In /other component
  const from = location.state?.from; // "home"
  
  return <button onClick={handleNavigate}>Navigate</button>;
}
```

## Key

Each location has a unique `key` useful for scroll restoration:

```tsx
function useScrollRestoration() {
  const location = useLocation();
  
  useEffect(() => {
    // Save scroll position with location key
    const scrollKey = `scroll-${location.key}`;
    const scrollY = window.scrollY;
    sessionStorage.setItem(scrollKey, scrollY.toString());
  }, [location]);
  
  useEffect(() => {
    // Restore scroll position
    const scrollKey = `scroll-${location.key}`;
    const savedScroll = sessionStorage.getItem(scrollKey);
    if (savedScroll) {
      window.scrollTo(0, parseInt(savedScroll));
    }
  }, [location]);
}
```

## Common Use Cases

### Analytics

Track page views:

```tsx
function useAnalytics() {
  const location = useLocation();
  
  useEffect(() => {
    // Send analytics event
    sendAnalytics({
      pathname: location.pathname,
      search: location.search,
      timestamp: Date.now(),
    });
  }, [location]);
}
```

### Scroll Restoration

Restore scroll position on navigation:

```tsx
function useScrollRestoration() {
  const location = useLocation();
  
  useEffect(() => {
    const scrollKey = `scroll-${location.key}`;
    const savedScroll = sessionStorage.getItem(scrollKey);
    
    if (savedScroll) {
      window.scrollTo(0, parseInt(savedScroll));
    }
    
    return () => {
      // Save scroll position before unmount
      sessionStorage.setItem(scrollKey, window.scrollY.toString());
    };
  }, [location]);
}
```

### Conditional Rendering

Render based on current pathname:

```tsx
function Component() {
  const location = useLocation();
  const isHomePage = location.pathname === "/";
  
  return (
    <div>
      {isHomePage && <HomeBanner />}
      <Content />
    </div>
  );
}
```

### Side Effects

Run side effects on location change:

```tsx
function Component() {
  const location = useLocation();
  
  useEffect(() => {
    // Reset form when pathname changes
    if (location.pathname !== "/form") {
      resetForm();
    }
  }, [location.pathname]);
  
  return <div>Content</div>;
}
```

### Highlight Active Route

```tsx
function NavLink({ to, children }) {
  const location = useLocation();
  const isActive = location.pathname === to;
  
  return (
    <a href={to} className={isActive ? "active" : ""}>
      {children}
    </a>
  );
}
```

## Location Changes

The location object changes on navigation, triggering re-renders:

```tsx
function Component() {
  const location = useLocation();
  
  // This effect runs whenever location changes
  useEffect(() => {
    console.log("Location changed:", location.pathname);
  }, [location]);
  
  return <div>Content</div>;
}
```

## Key Points

- **Reactive** - Location updates on navigation, triggers re-renders
- **Unique key** - Each location has a unique `key` for tracking
- **State persistence** - Location state persists across navigations
- **Side effects** - Use in `useEffect` for analytics, scroll restoration, etc.
- **Pathname matching** - Use `pathname` for route matching logic

<!--
Source references:
- https://reactrouter.com/start/declarative/url-values#location-object
-->
