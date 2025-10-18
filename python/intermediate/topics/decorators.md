# Python Decorators: A Comprehensive Guide

Python decorators are a powerful and elegant feature that allows you to modify or enhance functions and methods without changing their source code. They are essentially functions (or classes) that wrap another function, adding behavior before, after, or around the wrapped function's execution. Decorators leverage Python's first-class functions (functions that can be passed as arguments, returned from other functions, or assigned to variables) and the `@` syntax for a clean, readable application.

This guide progresses from simple to advanced examples, providing explanations, code snippets, and practical use cases. By the end, you'll understand how to create, apply, and customize decorators effectively.

## Why Use Decorators?

- **Code Reusability**: Apply common functionality (e.g., logging, caching, authentication) to multiple functions.
- **Separation of Concerns**: Keep core logic separate from cross-cutting concerns like timing or validation.
- **Readability**: The `@decorator` syntax is more intuitive than manual wrapping.
- **Common Applications**: Web frameworks (e.g., Flask routes), memoization, access control.

Decorators are syntactic sugar for function wrapping. The expression `@decorator` above a function is equivalent to `function = decorator(function)`.

## 1. Simple Decorators: Function Wrapping Basics

A basic decorator is a function that takes another function as input, defines a wrapper function, and returns the wrapper.

### Example: A Simple Logging Decorator

This decorator prints a message before and after the wrapped function runs.

```python
def simple_logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@simple_logger
def add_numbers(a, b):
    return a + b

# Usage
result = add_numbers(3, 5)
# Output:
# Calling add_numbers with args=(3, 5), kwargs={}
# add_numbers returned 8
# result: 8
```

**Explanation**:
- `simple_logger` is the decorator function.
- `wrapper` is an inner function that handles the actual wrapping: it logs input, calls the original `func`, logs output, and returns the result.
- `*args` and `**kwargs` make the wrapper flexible for any function signature.
- The `@simple_logger` syntax applies the decorator, effectively replacing `add_numbers` with `wrapper`.

**Pros**: Easy to implement for basic augmentation.  
**Cons**: Loses metadata like the function's name (`wrapper.__name__` becomes `'wrapper'`).

## 2. Intermediate Decorators: Preserving Metadata and Classes as Decorators

Simple decorators can break introspection (e.g., `func.__name__`). Use `functools.wraps` to preserve metadata. Also, explore classes as decorators for stateful behavior.

### Example: Logging Decorator with Metadata Preservation

```python
from functools import wraps

def logger_with_wraps(func):
    @wraps(func)  # Preserves __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} done")
        return result
    return wrapper

@logger_with_wraps
def multiply(x, y):
    """Multiplies two numbers."""
    return x * y

# Usage
print(multiply.__name__)  # Output: 'multiply' (preserved)
print(multiply(4, 3))     # Output: Calling multiply \n multiply done \n 12
print(multiply.__doc__)   # Output: 'Multiplies two numbers.'
```

**Explanation**:
- `@wraps(func)` copies attributes from `func` to `wrapper`, maintaining function identity.
- This is essential for debugging, testing, and tools like `help()` or `inspect`.

### Example: Class-Based Decorator for Stateful Logging

Classes can act as decorators by implementing `__call__`. Useful for decorators that maintain state (e.g., a counter).

```python
class Counter:
    def __init__(self, func):
        self.func = func
        self.call_count = 0
        wraps(func)(self)  # Preserve metadata on the instance

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        print(f"Function {self.func.__name__} called {self.call_count} times")
        return self.func(*args, **kwargs)

@Counter
def greet(name):
    return f"Hello, {name}!"

# Usage
print(greet("Alice"))  # Output: Function greet called 1 times \n Hello, Alice!
print(greet("Bob"))    # Output: Function greet called 2 times \n Hello, Bob!
print(greet.call_count)  # Output: 2 (state preserved)
```

**Explanation**:
- `__init__` stores the function and initializes state (`call_count`).
- `__call__` makes instances callable, incrementing the counter each time.
- `wraps(func)(self)` applies metadata preservation to the class instance.

**When to Use Classes**: For decorators needing internal state, like caches or counters.

## 3. Advanced Decorators: Decorator Factories and Parameters

Decorators can take arguments via a "factory" pattern: the outer function returns a decorator.

### Example: Parameterized Timing Decorator

This factory creates a timing decorator that optionally logs slow functions.

```python
import time
from functools import wraps

def timer(threshold=1.0):  # Factory function with default param
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            if elapsed > threshold:
                print(f"{func.__name__} took {elapsed:.2f}s (> {threshold}s)")
            return result
        return wrapper
    return decorator

@timer(threshold=0.5)  # Pass arg to factory
def slow_function(n):
    time.sleep(n)
    return n * 2

@timer()  # Use default threshold
def fast_function(n):
    return n * 2

# Usage
slow_function(1)  # Output: slow_function took 1.00s (> 0.5s)
fast_function(1)  # No output (under default 1.0s)
```

**Explanation**:
- `timer(threshold)` is the factory: it takes params and returns the actual `decorator`.
- `decorator` is a standard decorator wrapping `func`.
- This enables reusable, configurable decorators (e.g., `@timer(2.0)` for a 2-second threshold).
- Layers: Factory → Decorator → Wrapper.

### Example: Memoization Decorator (Caching)

A classic advanced use: cache results to avoid recomputation.

```python
from functools import wraps

def memoize(func):
    cache = {}  # Simple dict cache
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))  # Hashable key
        if key in cache:
            print(f"Cache hit for {func.__name__}")
            return cache[key]
        result = func(*args, **kwargs)
        cache[key] = result
        print(f"Computed and cached {func.__name__}")
        return result
    wrapper.clear_cache = lambda: cache.clear()  # Bonus: method to clear cache
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Usage
print(fibonacci(10))  # Computes (many recursive calls, but caches)
print(fibonacci(10))  # Cache hit, instant
fibonacci.clear_cache()  # Reset
print(fibonacci(10))  # Recomputes
```

**Explanation**:
- `cache` stores results keyed by arguments.
- Hashable keys ensure dict lookup works (tuples for immutability).
- Recursive functions like Fibonacci benefit hugely (exponential speedup).
- Added `clear_cache` for manual eviction.
- **Limitations**: Not thread-safe; for production, use `functools.lru_cache`.

### Example: Enforcing Preconditions (Validation Decorator Factory)

Validate inputs before execution.

```python
from functools import wraps

def validate_types(*type_checks):  # Factory takes type mappings
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i, (arg, expected_type) in enumerate(zip(args, type_checks)):
                if not isinstance(arg, expected_type):
                    raise TypeError(f"Arg {i} expected {expected_type}, got {type(arg)}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(int, int)  # Specify types for args
def divide(a, b):
    return a / b

# Usage
divide(10, 2)   # Works: 5.0
# divide(10.5, 2)  # Raises: TypeError: Arg 0 expected <class 'int'>, got <class 'float'>
```

**Explanation**:
- Factory `validate_types` accepts type expectations.
- `decorator` zips args with checks, raising `TypeError` on mismatch.
- Extensible: Could add kwarg validation or custom validators.

## Best Practices and Common Pitfalls

| Aspect          | Recommendation                          | Pitfall Example |
|-----------------|-----------------------------------------|-----------------|
| **Metadata**    | Always use `@wraps(func)`              | Losing `__name__` breaks debuggers. |
| **Arguments**   | Use `*args, **kwargs` for flexibility  | Fixed signatures limit reusability. |
| **Performance** | Avoid heavy computation in wrappers    | Timing decorators add overhead. |
| **Stacking**    | Order matters (bottom-up execution)    | `@dec1 @dec2` applies dec1 outer. |
| **Errors**      | Preserve exceptions; don't swallow     | Silent failures hide bugs. |
| **Testing**     | Mock wrappers or use `inspect`         | Hard to unit-test wrapped funcs. |

- **Stacking Decorators**: `@dec1 @dec2 def f(): ...` is `f = dec1(dec2(f))`—innermost runs first.
- **Pitfall**: Infinite recursion if wrapper calls itself instead of `func`.
- **Advanced Tip**: For methods, use `classmethod` or `staticmethod` decorators carefully to avoid `self` issues.

## Conclusion

Decorators transform Python code into modular, expressive art. Start with simple wrappers for logging or timing, then layer in factories for customization. Experiment with built-ins like `@property`, `@dataclass`, or `@lru_cache` to see them in action. For deeper dives, explore libraries like `decorator` or `wrapt`.

Practice by decorating your own functions—it's the best way to master them! If you have questions or want custom examples, ask away.

*Last Updated: October 18, 2025*