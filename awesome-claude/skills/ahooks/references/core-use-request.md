---
name: ahooks-use-request
description: useRequest hook for managing asynchronous data requests with caching, polling, debouncing, and more. Use when fetching data from APIs or handling async operations.
---

# useRequest

`useRequest` is a powerful async data fetching hook that provides rich features including caching, polling, debouncing, throttling, dependent requests, pagination, and more.

## Basic Usage

```tsx
import { useRequest } from 'ahooks';

function UserProfile({ userId }: { userId: string }) {
  const { data, error, loading } = useRequest(() => getUserInfo(userId));

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return <div>{data?.name}</div>;
}
```

## Return Values

```tsx
const {
  data,        // Data returned from service
  error,       // Error object
  loading,     // Loading state
  run,         // Manually trigger execution
  runAsync,    // Manually trigger execution (returns Promise)
  params,      // Current request parameters array
  cancel,      // Cancel current request
  refresh,     // Re-execute with last params
  refreshAsync,// Re-execute with last params (returns Promise)
  mutate,      // Directly modify data
  reset,       // Reset to initial state
} = useRequest(service, options);
```

## Manual Trigger

By default, `useRequest` automatically executes when the component mounts. Set `manual: true` to disable auto-execution:

```tsx
const { run } = useRequest(getUserInfo, {
  manual: true,
});

// Manually trigger
<button onClick={() => run(userId)}>Load User</button>
```

## Caching

### cacheKey

Use `cacheKey` to cache request results. Requests with the same `cacheKey` share the cache:

```tsx
const { data } = useRequest(() => getUserInfo(userId), {
  cacheKey: `user-${userId}`,
});
```

### staleTime

Set data freshness time. Within `staleTime`, the request won't be re-executed:

```tsx
useRequest(getUserInfo, {
  cacheKey: 'user-info',
  staleTime: 5 * 60 * 1000, // Data is considered fresh for 5 minutes
});
```

### cacheTime

Set cache retention time. Cache will be cleared after this time:

```tsx
useRequest(getUserInfo, {
  cacheKey: 'user-info',
  cacheTime: 10 * 60 * 1000, // Clear cache after 10 minutes
});
```

## Polling

### pollingInterval

Set polling interval in milliseconds:

```tsx
const { data } = useRequest(getMessages, {
  pollingInterval: 3000, // Poll every 3 seconds
});
```

### pollingWhenHidden

Whether to continue polling when page is hidden:

```tsx
useRequest(getMessages, {
  pollingInterval: 3000,
  pollingWhenHidden: false, // Stop polling when page is hidden
});
```

### Dynamic Polling Control

```tsx
const { data, cancel, run } = useRequest(getMessages, {
  pollingInterval: 3000,
});

// Stop polling
cancel();

// Restart polling
run();
```

## Debouncing and Throttling

### debounceInterval

Debounce delay. Multiple triggers within the delay will only execute the last one:

```tsx
const { data } = useRequest(searchUsers, {
  debounceInterval: 300, // 300ms debounce
});
```

### throttleInterval

Throttle interval. At most one execution within the interval:

```tsx
const { data } = useRequest(getPosition, {
  throttleInterval: 1000, // At most one execution per second
});
```

## Dependent Requests

### refreshDeps

Automatically re-request when dependencies change:

```tsx
const { data } = useRequest(() => getUserInfo(userId), {
  refreshDeps: [userId], // Auto re-request when userId changes
});
```

### ready

Only initiate request when `ready` is `true`:

```tsx
const [ready, setReady] = useState(false);

const { data } = useRequest(getUserInfo, {
  ready, // Only request when ready is true
});
```

## Loading Delay

### loadingDelay

Set delay before showing loading state to avoid flickering:

```tsx
const { loading } = useRequest(getUserInfo, {
  loadingDelay: 300, // Show loading after 300ms
});
```

## Error Retry

### retryCount

Set retry count:

```tsx
const { data, error } = useRequest(getUserInfo, {
  retryCount: 3, // Retry 3 times on failure
});
```

### retryInterval

Set retry interval:

```tsx
useRequest(getUserInfo, {
  retryCount: 3,
  retryInterval: 1000, // 1 second between retries
});
```

## Callbacks

### onSuccess

Callback on successful request:

```tsx
useRequest(getUserInfo, {
  onSuccess: (data, params) => {
    console.log('Success:', data);
  },
});
```

### onError

Callback on request error:

```tsx
useRequest(getUserInfo, {
  onError: (error, params) => {
    console.error('Error:', error);
  },
});
```

### onFinally

Callback when request finishes (success or error):

```tsx
useRequest(getUserInfo, {
  onFinally: (data, error, params) => {
    console.log('Request finished');
  },
});
```

## Direct Data Mutation

Use `mutate` to directly modify `data` without triggering a request:

```tsx
const { data, mutate } = useRequest(getUserInfo);

// Directly modify data
mutate({ ...data, name: 'New Name' });

// Or use function form
mutate((oldData) => ({ ...oldData, name: 'New Name' }));
```

## Reset State

Use `reset` to reset to initial state:

```tsx
const { reset } = useRequest(getUserInfo);

// Reset to initial state
reset();
```

## Pagination

### Basic Pagination

```tsx
const { data, loading, pagination } = useRequest(
  ({ current, pageSize }) => getUsers({ page: current, size: pageSize }),
  {
    paginated: true,
  }
);

// pagination includes current, pageSize, total, onChange, etc.
<Table
  dataSource={data?.list}
  loading={loading}
  pagination={pagination}
/>
```

### Custom Pagination Parameters

```tsx
const { data, pagination } = useRequest(getUsers, {
  paginated: {
    defaultPageSize: 20,
    defaultCurrent: 1,
  },
});
```

## Load More

```tsx
const {
  data,
  loading,
  loadingMore,
  loadMore,
  noMore,
} = useRequest(getList, {
  loadMore: true,
});

return (
  <div>
    {data?.list.map(item => <div key={item.id}>{item.name}</div>)}
    {loadingMore && <div>Loading more...</div>}
    {!noMore && <button onClick={loadMore}>Load More</button>}
  </div>
);
```

## TypeScript

```tsx
interface UserInfo {
  id: string;
  name: string;
  email: string;
}

const { data } = useRequest<UserInfo, [string]>(
  (userId: string) => getUserInfo(userId),
  {
    manual: true,
  }
);

// data type is UserInfo | undefined
```

## Complete Example

```tsx
function UserList() {
  const [keyword, setKeyword] = useState('');
  
  const {
    data,
    loading,
    error,
    run,
    refresh,
    cancel,
  } = useRequest(
    (searchKeyword: string) => searchUsers({ keyword: searchKeyword }),
    {
      manual: true,
      debounceInterval: 300,
      cacheKey: `users-${keyword}`,
      staleTime: 5 * 60 * 1000,
      onSuccess: (data) => {
        console.log('Search success:', data);
      },
      onError: (error) => {
        message.error('Search failed');
      },
    }
  );

  useEffect(() => {
    if (keyword) {
      run(keyword);
    }
  }, [keyword]);

  return (
    <div>
      <Input
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
        placeholder="Search users"
      />
      {loading && <Spin />}
      {error && <Alert message={error.message} type="error" />}
      {data?.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

## Key Points

- **Auto-execution** - Executes automatically on mount by default, set `manual: true` to disable
- **Caching mechanism** - Use `cacheKey` to implement request caching and sharing
- **Polling support** - `pollingInterval` enables timed polling
- **Debouncing and throttling** - `debounceInterval` and `throttleInterval` control request frequency
- **Dependent requests** - `refreshDeps` enables auto re-request on dependency changes
- **Error retry** - `retryCount` and `retryInterval` enable automatic retry
- **Pagination and load more** - `paginated: true` and `loadMore: true` support pagination and load more
- **Type safety** - Full TypeScript support

<!--
Source references:
- https://ahooks.js.org/zh-CN/hooks/use-request/index
- https://ahooks.js.org/hooks/use-request/index
-->
