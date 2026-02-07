---
name: react-router-use-search-params
description: useSearchParams hook to read and update URL search parameters. Use when you need to work with query string parameters.
---

# useSearchParams

The `useSearchParams` hook returns a tuple containing the current URL's `URLSearchParams` and a function to update them. Setting search params causes a navigation.

## Basic Usage

```tsx
import { useSearchParams } from "react-router";

function SearchResults() {
  const [searchParams] = useSearchParams();
  const query = searchParams.get("q");
  
  return (
    <div>
      <p>You searched for <i>{query}</i></p>
    </div>
  );
}
```

## Reading Search Params

Use `URLSearchParams` methods to read values:

```tsx
function Component() {
  const [searchParams] = useSearchParams();
  
  // Get single value
  const tab = searchParams.get("tab");
  
  // Get all values for a key
  const brands = searchParams.getAll("brand");
  
  // Check if param exists
  const hasFilter = searchParams.has("filter");
  
  // Iterate over all params
  for (const [key, value] of searchParams.entries()) {
    console.log(key, value);
  }
}
```

## Updating Search Params

Use `setSearchParams` to update search params:

```tsx
function Component() {
  const [searchParams, setSearchParams] = useSearchParams();
  
  const handleTabChange = (tab: string) => {
    setSearchParams({ tab });
  };
  
  return (
    <div>
      <button onClick={() => setSearchParams({ tab: "1" })}>
        Tab 1
      </button>
    </div>
  );
}
```

## setSearchParams Formats

`setSearchParams` accepts multiple formats:

```tsx
const [searchParams, setSearchParams] = useSearchParams();

// Search param string
setSearchParams("?tab=1");

// Shorthand object
setSearchParams({ tab: "1" });

// Object with arrays for multiple values
setSearchParams({ brand: ["nike", "reebok"] });

// Array of tuples
setSearchParams([["tab", "1"]]);

// URLSearchParams object
setSearchParams(new URLSearchParams("?tab=1"));
```

## Function Callback

Supports function callback like React's `setState`:

```tsx
function Component() {
  const [searchParams, setSearchParams] = useSearchParams();
  
  const handleUpdate = () => {
    setSearchParams((prev) => {
      prev.set("tab", "2");
      return prev;
    });
  };
  
  return <button onClick={handleUpdate}>Update</button>;
}
```

Note: Multiple calls to `setSearchParams` in the same tick will not build on the prior value (unlike React's `setState`).

## Default Init

Initialize search params with default values (does not change URL on first render):

```tsx
// Search param string
const [searchParams] = useSearchParams("?tab=1");

// Shorthand object
const [searchParams] = useSearchParams({ tab: "1" });

// Object with arrays
const [searchParams] = useSearchParams({ brand: ["nike", "reebok"] });

// Array of tuples
const [searchParams] = useSearchParams([["tab", "1"]]);

// URLSearchParams object
const [searchParams] = useSearchParams(new URLSearchParams("?tab=1"));
```

## useEffect Dependency

`searchParams` is a stable reference, safe to use in `useEffect`:

```tsx
function Component() {
  const [searchParams] = useSearchParams();
  
  useEffect(() => {
    console.log(searchParams.get("tab"));
  }, [searchParams]);
  
  return <div>Content</div>;
}
```

## Common Patterns

### Filter Component

```tsx
function FilterComponent() {
  const [searchParams, setSearchParams] = useSearchParams();
  
  const handleFilter = (key: string, value: string) => {
    setSearchParams((prev) => {
      prev.set(key, value);
      return prev;
    });
  };
  
  return (
    <div>
      <button onClick={() => handleFilter("category", "electronics")}>
        Electronics
      </button>
    </div>
  );
}
```

### Pagination

```tsx
function Pagination() {
  const [searchParams, setSearchParams] = useSearchParams();
  const page = parseInt(searchParams.get("page") || "1");
  
  const handlePageChange = (newPage: number) => {
    setSearchParams({ page: newPage.toString() });
  };
  
  return (
    <div>
      <button onClick={() => handlePageChange(page + 1)}>Next</button>
    </div>
  );
}
```

### Multiple Values

```tsx
function MultiSelect() {
  const [searchParams, setSearchParams] = useSearchParams();
  
  const selectedBrands = searchParams.getAll("brand");
  
  const toggleBrand = (brand: string) => {
    setSearchParams((prev) => {
      if (prev.getAll("brand").includes(brand)) {
        prev.delete("brand", brand);
      } else {
        prev.append("brand", brand);
      }
      return prev;
    });
  };
  
  return (
    <div>
      {["nike", "adidas", "puma"].map((brand) => (
        <button
          key={brand}
          onClick={() => toggleBrand(brand)}
          className={selectedBrands.includes(brand) ? "active" : ""}
        >
          {brand}
        </button>
      ))}
    </div>
  );
}
```

## Key Points

- **Stable reference** - `searchParams` is stable, safe for `useEffect` dependencies
- **Navigation** - Setting search params causes navigation
- **Multiple formats** - Accepts strings, objects, arrays, or URLSearchParams
- **Function callback** - Supports callback pattern like `setState`
- **No batching** - Multiple calls don't batch (unlike React state)

<!--
Source references:
- https://reactrouter.com/api/hooks/useSearchParams
- https://reactrouter.com/start/declarative/url-values#url-search-params
-->
