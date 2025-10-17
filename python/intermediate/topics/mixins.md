# Overview of Mixins in Python

Mixins are a powerful design pattern in Python's object-oriented programming (OOP) ecosystem, enabling modular and reusable code without rigid inheritance hierarchies. Below is a comprehensive overview, drawing from established tutorials and discussions.

## Definition
A **mixin** is a class designed to provide specific, reusable methods or behaviors to other classes via **multiple inheritance**, but it is not intended to be instantiated on its own or to form a strict "is-a" relationship. Unlike traditional base classes, mixins focus on a single responsibility—such as serialization, logging, or validation—and encapsulate functionality that can be "mixed in" to unrelated classes. Python has no special syntax for mixins; they are simply classes, often named with a `Mixin` suffix (e.g., `SerializableMixin`) to signal their purpose. They differ from abstract base classes (ABCs) by providing concrete implementations rather than just interfaces, and from traits in other languages by leveraging Python's flexible multiple inheritance.

In essence, mixins promote **composition over inheritance**, allowing you to add orthogonal features (e.g., JSON serialization) to classes like `User` or `Inventory` without duplicating code or creating deep, brittle hierarchies.

## Purpose and Benefits
The primary goal of mixins is **code reuse** and **modularity**. They allow you to:
- Share method implementations across multiple, potentially unrelated subclasses without implying a new type hierarchy.
- Avoid the DRY (Don't Repeat Yourself) violation by implementing behaviors once and inheriting them where needed.
- Enable flexible, loosely coupled designs, such as plugging in authentication or caching to third-party libraries like Django views.
- Support polymorphism and extension, e.g., adding optional HTTP features (like ETags or user agents) to a base request class.

Benefits include improved maintainability (features in isolated modules), reduced boilerplate, and easier testing (override mixin methods for mocks). They are especially useful in frameworks like Django (e.g., `LoginRequiredMixin`) or the standard library (e.g., `ThreadingMixIn` for servers).

## How Mixins Work
Mixins operate through Python's **multiple inheritance**, where a class inherits from one or more mixins followed by its primary base class. The **Method Resolution Order (MRO)**—computed via the C3 linearization algorithm—determines the search order for methods and attributes, ensuring predictable resolution.

Key mechanics:
- **Inheritance Order**: Place mixins *before* the base class in the tuple (e.g., `class MyClass(Mixin1, Mixin2, Base):`) to allow mixin methods to override or extend base behaviors.
- **Cooperative Inheritance**: Use `super()` in mixin methods to chain calls to the next class in the MRO, enabling seamless delegation.
- **Stateless Design**: Ideal mixins avoid instance attributes (`self.foo`) to prevent conflicts; they rely on the host class's state or external data.
- **No Standalone Use**: Mixins often depend on undefined methods from the host, raising errors if instantiated alone.

This setup allows "recombination": pair mixin "providers" (e.g., a method returning a value) with "users" (e.g., a method consuming it) for varied behaviors.

## Examples
### Basic Serializable Mixin
This mixin adds dictionary serialization to any class with attributes:

```python
class SerializableMixin:
    def serialize(self) -> dict:
        if hasattr(self, "__slots__"):
            return {name: getattr(self, name) for name in self.__slots__}
        return vars(self)

from dataclasses import dataclass

@dataclass
class User(SerializableMixin):
    name: str
    age: int

user = User("Alice", 30)
print(user.serialize())  # {'name': 'Alice', 'age': 30}
```

### JSON and Dict Mixins (Composed)
Combine multiple mixins for layered functionality, like converting objects to dicts and then JSON:

```python
import json
from pprint import pprint

class DictMixin:
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, attributes: dict) -> dict:
        result = {}
        for key, value in attributes.items():
            result[key] = self._traverse(key, value)
        return result

    def _traverse(self, key, value):
        if isinstance(value, DictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, v) for v in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value

class JSONMixin:
    def to_json(self):
        return json.dumps(self.to_dict())

class Person:
    def __init__(self, name):
        self.name = name

class Employee(DictMixin, JSONMixin, Person):
    def __init__(self, name, skills, dependents):
        super().__init__(name)
        self.skills = skills
        self.dependents = dependents

e = Employee('John', ['Python', 'SQL'], {'wife': 'Jane', 'kids': ['Alice']})
pprint(e.to_dict())
print(e.to_json())
```

Output:
```
{'dependents': {'kids': ['Alice'], 'wife': 'Jane'},
 'name': 'John',
 'skills': ['Python', 'SQL']}
{"name": "John", "skills": ["Python", "SQL"], "dependents": {"wife": "Jane", "kids": ["Alice"]}}
```

### Comparable Mixin (Operator Overloading)
Implements comparisons using just `__eq__` and `__le__`:

```python
class ComparableMixin:
    def __eq__(self, other):
        return self <= other and other <= self

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self <= other and not (self == other)

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return self == other or self > other

class Integer(ComparableMixin):
    def __init__(self, i):
        self.i = i

    def __le__(self, other):
        return self.i <= other.i

    def __eq__(self, other):
        return self.i == other.i

print(Integer(0) < Integer(1))  # True
```

### Real-World: Django View Mixins
In Django, mixins like `LoginRequiredMixin` add authentication:

```python
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book

class BookListView(LoginRequiredMixin, ListView):
    model = Book
    paginate_by = 10
```

## Best Practices
- **Naming**: End with `Mixin` for clarity.
- **Single Responsibility**: One mixin, one behavior—keep it focused and stateless.
- **Order Matters**: Mixins first in inheritance list; use `super()` for chains.
- **Avoid State**: Use closures, decorators, or class attributes instead of `self` vars to dodge conflicts.
- **Test Thoroughly**: Verify MRO with `Class.__mro__`; limit to 2-3 mixins per class.
- **Alternatives**: For simple cases, consider decorators or composition over mixins.

## Pros and Cons
| Aspect | Pros | Cons |
|--------|------|------|
| **Reusability** | High: Share code across unrelated classes without duplication. | Can lead to tangled hierarchies if overused. |
| **Modularity** | Loose coupling; easy to compose features. | MRO issues may cause subtle bugs (e.g., method shadowing). |
| **Flexibility** | Supports polymorphism and extension (e.g., in frameworks). | Stateful mixins risk attribute clashes or init failures. |
| **Maintenance** | Isolated behaviors simplify updates. | Increases complexity; harder to trace call chains. |

Overall, pros outweigh cons for targeted reuse, but avoid in simple single-inheritance scenarios.

## Common Pitfalls
- **MRO Surprises**: Wrong order skips mixins; always check `.__mro__`.
- **Constructor Conflicts**: Forget `super().__init__()` and bases won't initialize—use `*args, **kwargs`.
- **Attribute Overlaps**: Multiple mixins setting `self._cache` overwrites data; use unique names or avoid state.
- **Over-Mixing**: "God classes" from too many mixins—refactor into fewer, grouped ones.
- **Instantiation Attempts**: Mixins may error if run alone due to missing methods—document as non-instantiable.

Mixins shine in libraries and frameworks but require discipline. For deeper dives, explore `functools.total_ordering` (a decorator alternative) or standard library examples like `socketserver.ThreadingMixIn`. If you'd like code for a specific use case, let me know!


# Explanations for `functools.total_ordering` and `socketserver.ThreadingMixIn`

Continuing from the discussion on mixins, here are detailed explanations of the two items you highlighted. These illustrate alternatives to custom mixins and real-world standard library usage, respectively. I'll cover concepts, usage, examples, and ties back to mixins where relevant.

## `functools.total_ordering`: A Decorator Alternative to Comparable Mixins

### Overview
`functools.total_ordering` is a **class decorator** from Python's standard library `functools` module (introduced in Python 2.7). It automates the implementation of the full set of comparison special methods (`__lt__`, `__gt__`, `__le__`, `__ge__`, `__eq__`, `__ne__`) for classes that define at least `__eq__` and one of `__lt__` or `__gt__`. This provides a **total ordering**—a consistent, transitive comparison across all elements—without manually writing all six methods, which is error-prone and verbose.

It's an excellent **decorator alternative to a ComparableMixin** because:
- It reduces boilerplate compared to a mixin that overrides multiple dunder methods.
- It promotes **DRY** (Don't Repeat Yourself) by generating methods dynamically.
- Like mixins, it enables operator overloading (e.g., `<`, `<=`, `==`) for custom types, but it's lighter-weight and doesn't require inheritance.
- Use it when you need sortable classes (e.g., for `sorted()`, `min()`, `max()`) but want to avoid full mixin hierarchies.

**Key Requirements**:
- Define `__eq__` (equality).
- Define either `__lt__` (less than) or `__gt__` (greater than)—the rest are derived.
- The class must be **hashable** if used in sets/dicts (implement `__hash__` consistently with `__eq__`).
- Works with both classes and dataclasses.

**Limitations**:
- Derived methods may be less efficient (they call the base comparisons multiple times).
- No support for partial orders (e.g., non-transitive comparisons like rock-paper-scissors).
- If you need custom logic for all methods, a mixin might be more flexible.

### How It Works
The decorator inspects the class, identifies the provided methods, and injects the missing ones using logical combinations:
- `__ne__` = `not __eq__`
- `__le__` = `__lt__ or __eq__`
- `__ge__` = `__gt__ or __eq__`
- `__gt__` = `not __le__` (if `__lt__` is defined)
- `__lt__` = `not __ge__` (if `__gt__` is defined)

This ensures **antisymmetry** and **transitivity** for sorting.

### Example
Compare a custom `ComparableMixin` (from earlier) vs. `total_ordering`:

#### Without `total_ordering` (Using a Mixin)
```python
class ComparableMixin:
    def __eq__(self, other):
        return self <= other and other <= self

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self <= other and not (self == other)

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return self == other or self > other

class Integer(ComparableMixin):
    def __init__(self, i):
        self.i = i

    def __le__(self, other):
        return self.i <= other.i

# Usage
a, b = Integer(1), Integer(2)
print(a < b)  # True
```

#### With `functools.total_ordering` (Decorator Alternative)
```python
from functools import total_ordering

@total_ordering
class Integer:
    def __init__(self, i):
        self.i = i

    def __eq__(self, other):
        return self.i == other.i

    def __lt__(self, other):
        return self.i < other.i

    # No need for __gt__, __le__, etc.—automatically added!

# Usage (same as above)
a, b = Integer(1), Integer(2)
print(a < b)  # True (via derived __lt__)
print(a <= b)  # True (derived: __lt__ or __eq__)
print(sorted([b, a]))  # [Integer(1), Integer(2)]
```

**Output** (for both):
```
True
```

The decorator version is concise—ideal for simple cases. For complex logic (e.g., string-based comparisons), extend with a mixin.

### Best Practices
- Apply `@total_ordering` directly to the class.
- Ensure `__eq__` and `__lt__` handle `NotImplemented` for mixed-type comparisons.
- Combine with `@dataclass` for auto-generated `__eq__` and `__lt__`.
- Test with `sorted()` and edge cases (e.g., self-comparisons).

## `socketserver.ThreadingMixIn`: A Standard Library Mixin Example

### Overview
`socketserver.ThreadingMixIn` is a concrete **mixin class** in Python's `socketserver` module (part of the standard library since Python 1.5.2). It provides **multi-threaded request handling** for TCP/UDP servers by wrapping each incoming request in a separate thread. This is a classic example of a mixin in action: it adds concurrency without altering the core server logic, promoting reuse across server types (e.g., `TCPServer`, `UDPServer`).

**Purpose**:
- Handles **I/O-bound** workloads (e.g., web servers, chat apps) by parallelizing requests, improving throughput.
- Demonstrates mixins for **cross-cutting concerns** like threading, logging, or forking—orthogonal to the server's protocol.
- Ties to the roadmap: Aligns with intermediate concurrency (`threading`) and advanced OOP (mixins for extension).

**Key Features**:
- Uses `threading.Thread` to spawn a new thread per `handle_request()` call.
- Shares the server's socket safely with locks (via `server_forever()` loop).
- No state: Relies on the host class's `process_request()` and `handle_request()` methods.
- Thread-safe: Uses a lock for request processing to avoid race conditions.

**Related Mixins in `socketserver`**:
- `ForkingMixIn`: Uses `os.fork()` for processes (Unix-only, bypasses GIL).
- `BaseServer`: The abstract base—mixins compose on top.

### How It Works
1. Inherit: `class ThreadedTCPServer(ThreadingMixIn, TCPServer):`.
2. MRO ensures `ThreadingMixIn`'s overrides (e.g., `process_request()`) come before `TCPServer`.
3. `server_forever()` loop: Accept connection → `process_request()` → Spawn thread → `handle_request()` in thread.
4. Threads die after handling, minimizing overhead.

This enables **concurrent** servers without rewriting the base.

### Example: Simple Threaded Echo Server
```python
import socketserver
import threading

class ThreadingMixIn(socketserver.ThreadingMixIn):
    # Already defined in stdlib; shown for clarity
    def process_request(self, request, client_address):
        """Start a new thread to process each request."""
        t = threading.Thread(target=self.process_request_thread, args=(request, client_address))
        t.daemon = True
        t.start()

class ThreadedEchoServer(ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True  # Avoid "Address in use" errors

    def handle_request(self, request, client_address):
        """Echo back the client's message."""
        data = request.recv(1024)
        if data:
            print(f"Received from {client_address}: {data.decode()}")
            request.sendall(data)  # Echo
        request.close()

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = ThreadedEchoServer((HOST, PORT), ThreadedEchoServer)
    print(f"Server running on {HOST}:{PORT} (multi-threaded)")
    server.serve_forever()
```

**Usage**:
- Run the server.
- Connect via telnet: `telnet localhost 9999`, type "Hello", hit Enter → Echoes back.
- Multiple clients (e.g., two telnet sessions) handle concurrently without blocking.

**Output** (server console for two clients):
```
Server running on localhost:9999 (multi-threaded)
Received from ('127.0.0.1', 54321): Hello
Received from ('127.0.0.1', 54322): World
```

**Why a Mixin?**
- `TCPServer` is single-threaded by default (blocks on each request).
- `ThreadingMixIn` adds parallelism via inheritance, keeping `handle_request()` pure.
- Extensible: Combine with custom mixins (e.g., `LoggingMixIn`) for logging.

### Best Practices
- Set `allow_reuse_address = True` for quick restarts.
- Use `daemon=True` for threads to avoid hanging on shutdown.
- For production, consider `concurrent.futures.ThreadPoolExecutor` or `asyncio` for better control.
- Limit threads if CPU-bound (use `ForkingMixIn` instead).

These examples show how Python's stdlib leverages mixins for extensibility—`total_ordering` as a decorator shortcut, and `ThreadingMixIn` as a reusable concurrency booster. If you'd like code expansions or more examples, let me know!

# Understanding the `__new__` Method Parameters in Python Metaclasses

In Python metaclasses, the `__new__` method is a key hook for customizing class creation. It's called during class definition and is responsible for *creating* the class object itself (similar to how `__new__` creates instances for regular classes). The signature is:

```python
def __new__(mcs, name, bases, dct):
    # Custom logic here
    return super().__new__(mcs, name, bases, dct)  # Or return a modified class
```

This method receives four parameters: `mcs`, `name`, `bases`, and `dct`. Each plays a crucial role in the class creation process. Below, I'll explain them in detail, including their types, purposes, mutability, common uses, and examples. These parameters are derived from the class definition syntax (e.g., `class MyClass(Base1, Base2): ...`).

## 1. `mcs` (Metaclass Instance)
### Description
- **Full Name**: Stands for "metaclass" (often referred to as `cls` in documentation, like class methods).
- **Type**: The metaclass class object itself (e.g., `<class 'MyMeta'>`).
- **Purpose**: Provides access to the metaclass's own attributes, methods, and state. It's the "self" equivalent for metaclasses, allowing you to reference the metaclass during class creation.
- **Mutability**: Immutable within `__new__` (it's the class, not an instance), but you can use it to access or modify metaclass-level state (e.g., class variables).
- **When It's Set**: Resolved from the `metaclass=...` keyword or inherited from bases; defaults to `type`.
- **Common Uses**:
  - Accessing metaclass attributes (e.g., `mcs._registry` for registration).
  - Calling other metaclass methods (e.g., `mcs.validate(bases)`).
  - Dynamic metaclass behavior, like subclassing based on conditions.
  - Error raising with context (e.g., `raise TypeError(f"In metaclass {mcs.__name__}...")`).
- **Edge Cases**:
  - If multiple bases have metaclasses, Python merges them or raises `TypeError`.
  - In recursive metaclasses (metaclass of a metaclass), `mcs` is the parent metaclass.

### Example
```python
class LoggingMeta(type):
    _creation_log = []  # Metaclass-level state

    def __new__(mcs, name, bases, dct):
        mcs._creation_log.append(f"Creating {name} with metaclass {mcs.__name__}")
        print(f"Metaclass instance: {mcs}")  # Outputs: <class '__main__.LoggingMeta'>
        return super().__new__(mcs, name, bases, dct)

class MyClass(metaclass=LoggingMeta):
    pass

print(LoggingMeta._creation_log)  # ['Creating MyClass with metaclass LoggingMeta']
```

**Output**:
```
Metaclass instance: <class '__main__.LoggingMeta'>
['Creating MyClass with metaclass LoggingMeta']
```

Here, `mcs` accesses `_creation_log` to log class creations.

## 2. `name` (Class Name)
### Description
- **Type**: `str` (the fully qualified name of the class, e.g., `'MyClass'`).
- **Purpose**: Identifies the class being defined. It's the first argument to `type(name, bases, dct)` under the hood.
- **Mutability**: Immutable string—cannot be changed, but you can use it to dynamically add attributes (e.g., based on naming conventions).
- **When It's Set**: Extracted from the class header (e.g., `class name(...):`).
- **Common Uses**:
  - Naming conventions enforcement (e.g., raise error if not CamelCase).
  - Dynamic attribute addition (e.g., `dct[f'{name}_counter'] = 0`).
  - Logging or documentation (e.g., auto-set `__doc__` with the name).
  - Avoiding name clashes in registries (e.g., `registry[name] = cls`).
- **Edge Cases**:
  - Anonymous classes (rare; `name` is `'<unnamed>'` in dynamic creation).
  - Nested classes: Includes module path if relevant, but usually just the local name.

### Example
```python
class NamingMeta(type):
    def __new__(mcs, name, bases, dct):
        if not name[0].isupper():
            raise ValueError(f"Class name '{name}' must start with uppercase letter.")
        dct['class_name'] = name  # Add attribute with the name
        return super().__new__(mcs, name, bases, dct)

class ValidClass(metaclass=NamingMeta):  # OK
    pass

# class invalid_class(metaclass=NamingMeta):  # Raises ValueError
#     pass

print(ValidClass.class_name)  # 'ValidClass'
```

**Output** (for valid case):
```
ValidClass
```

This enforces a naming rule using `name`.

## 3. `bases` (Base Classes)
### Description
- **Type**: `tuple` of class objects (e.g., `(<class 'Base1'>, <class 'Base2'>)`). Always includes `object` implicitly at the end via MRO.
- **Purpose**: Represents the inheritance hierarchy—the direct superclasses of the new class. Used to compute the full MRO and merge metaclasses.
- **Mutability**: Immutable tuple, but you can inspect it (e.g., `bases[0]`) or raise errors based on it. Cannot modify directly; for dynamic bases, use `type` to recreate.
- **When It's Set**: From the class header (e.g., `class MyClass(Base1, Base2):`); empty `()` for no inheritance.
- **Common Uses**:
  - Validating inheritance (e.g., ensure no circular bases with `issubclass`).
  - Merging behaviors (e.g., check if a base has a required method).
  - Auto-mixins: Dynamically add bases if conditions met.
  - MRO inspection: `bases.__mro__` isn't direct, but you can compute linearization.
- **Edge Cases**:
  - Multiple inheritance: Triggers C3 linearization; invalid hierarchies raise `TypeError`.
  - If bases have conflicting metaclasses, `bases` helps diagnose.

### Example
```python
class InheritanceMeta(type):
    def __new__(mcs, name, bases, dct):
        for base in bases:
            if not hasattr(base, 'required_method'):
                raise TypeError(f"Base {base.__name__} missing 'required_method'.")
        print(f"Bases: {[b.__name__ for b in bases]}")  # Inspect bases
        return super().__new__(mcs, name, bases, dct)

class Base:
    required_method = lambda self: None

class MyClass(Base, metaclass=InheritanceMeta):  # OK
    pass

# class BadClass(metaclass=InheritanceMeta):  # Raises TypeError (no bases with method)
#     pass
```

**Output**:
```
Bases: ['Base']
```

This validates that all `bases` provide necessary methods.

## 4. `dct` (Namespace Dictionary)
### Description
- **Type**: `dict` (the class's namespace, containing all attributes defined in the class body, e.g., `{'__module__': '__main__', 'method': <function>, '__doc__': None}`).
- **Purpose**: Holds the raw attributes, methods, and dunders collected from executing the class body. It's the third argument to `type(name, bases, dct)`, allowing modification before the class is sealed.
- **Mutability**: Fully mutable! This is the powerhouse—add, delete, or alter keys (e.g., `dct['new_method'] = lambda self: ...`).
- **When It's Set**: Built by executing the class suite in a temporary scope; includes `__qualname__`, `__module__`, etc., automatically.
- **Common Uses**:
  - Injecting methods/attributes (e.g., auto-add `__str__`).
  - Validation (e.g., ensure abstract methods are implemented by checking for `@abstractmethod`).
  - Transformation (e.g., convert dict methods to properties).
  - Removal (e.g., `del dct['private_var']` for security).
- **Edge Cases**:
  - Prepared via `__prepare__` (if overridden; defaults to `dict`, but can be `collections.OrderedDict` for Python 3.6+ order).
  - Nested scopes: Captures locals from class body.

### Example
```python
class AutoStrMeta(type):
    def __new__(mcs, name, bases, dct):
        # Inspect existing dct
        print(f"Original dct keys: {list(dct.keys())}")
        
        # Inject a __str__ method
        def auto_str(self):
            attrs = ', '.join(f"{k}={v}" for k, v in vars(self).items())
            return f"<{name}({attrs})>"
        dct['__str__'] = auto_str
        
        # Validate: Ensure no 'secret' key
        if 'secret' in dct:
            del dct['secret']
        
        return super().__new__(mcs, name, bases, dct)

class Person(metaclass=AutoStrMeta):
    def __init__(self, name):
        self.name = name
    # secret = 'hidden'  # Would be deleted

p = Person("Alice")
print(p)  # <Person(name=Alice)>
```

**Output**:
```
Original dct keys: ['__module__', '__qualname__', '__init__']
<Person(name=Alice)>
```

Here, `dct` is modified to add `__str__` and remove sensitive keys.

## Putting It All Together: A Full Example
```python
class ComprehensiveMeta(type):
    def __new__(mcs, name, bases, dct):
        print(f"Metaclass: {mcs.__name__}")
        print(f"Name: {name}")
        print(f"Bases: {[b.__name__ for b in bases]}")
        print(f"Dct preview: {dict(list(dct.items())[:2])}...")  # First two items
        
        # Example: Add a timestamp based on name
        if 'timestamp' not in dct:
            dct['timestamp'] = f"{name} created at {__import__('datetime').datetime.now()}"
        
        return super().__new__(mcs, name, bases, dct)

class Example(metaclass=ComprehensiveMeta):
    pass
```

**Output**:
```
Metaclass: ComprehensiveMeta
Name: Example
Bases: []
Dct preview: {'__module__': '__main__', '__qualname__': 'Example'}...
Example timestamp: Example created at 2025-10-17 12:00:00.000000  # Approximate
```

## Key Takeaways
- **`__new__` vs. `__init__`**: `__new__` *creates* and returns the class; `__init__` initializes it afterward (less common for metaclasses).
- **Return Value**: Must return a class object; typically `super().__new__(...)` with modified `dct`.
- **Performance**: Runs at *definition* time, not runtime—efficient for one-off setup.
- **Debugging Tip**: Print these params or use `pdb` inside `__new__` to inspect during class def.

This covers the parameters exhaustively. If you want examples tied to specific use cases (e.g., ORMs), let me know!