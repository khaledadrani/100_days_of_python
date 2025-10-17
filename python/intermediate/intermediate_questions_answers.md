# Top Intermediate Python Interview Questions with Answers

Based on the Intermediate level roadmap, here are brief answers to each question. Answers emphasize **key keywords** (highlighted in bold) for quick recall and mastery.

## Advanced Object-Oriented Programming
1. **How does Python handle multiple inheritance?**  
   **Answer:** Python uses **Method Resolution Order (MRO)** via **C3 linearization algorithm** to resolve method calls in diamond inheritance hierarchies, ensuring consistent class precedence while avoiding ambiguity.

2. **What is Method Resolution Order (MRO) in Python?**  
   **Answer:** **MRO** is a class attribute (`__mro__`) that defines the linear order of superclasses for method lookup during **multiple inheritance**, computed using **C3 linearization** to merge hierarchies without cycles.

3. **What are mixins in Python?**  
   **Answer:** **Mixins** are classes providing specific functionality (e.g., logging) via **multiple inheritance**, designed for composition over inheritance, without a common base class, to reuse code horizontally.

4. **What is the diamond problem in multiple inheritance and how does Python resolve it?**  
   **Answer:** The **diamond problem** occurs when a class inherits from two subclasses of a common parent, causing duplicate method calls; Python resolves it with **MRO** and **C3 linearization** for unambiguous, linear resolution.

5. **What are abstract classes and interfaces in Python? How do you create them?**  
   **Answer:** **Abstract classes** enforce structure via **abc.ABC** and `@abstractmethod`; **interfaces** are abstract classes with only abstract methods. Create using `from abc import ABC, abstractmethod` and subclass.

6. **How do you implement abstract base classes (ABCs) in Python?**  
   **Answer:** Use `from abc import ABC, abstractmethod`; define class as `class MyABC(ABC):` and decorate methods with `@abstractmethod` to enforce **virtual subclassing** and **structural typing**.

7. **Explain the concept of composition over inheritance. When is composition preferred?**  
   **Answer:** **Composition** embeds objects as attributes for flexible behavior (e.g., "has-a" relationships); prefer over **inheritance** ("is-a") for **tight coupling avoidance**, **single responsibility**, and easier maintenance in large systems.

## Magic Methods and Data Models
1. **Explain the difference between `__str__` and `__repr__` methods in Python.**  
   **Answer:** **`__str__`** returns a **human-readable string** (via `str()` or `print()`); **`__repr__`** returns a **developer-friendly, unambiguous string** (via `repr()`) for debugging and reconstruction.

2. **What are magic methods (dunder methods) in Python?**  
   **Answer:** **Magic methods** (e.g., `__init__`, `__add__`, `__len__`) are **dunder methods** (double-underscore) that customize **object behavior**, enabling **operator overloading** and **data model** integration.

3. **What are slots (`__slots__`) and why use them?**  
   **Answer:** **`__slots__`** is a class attribute restricting instance attributes to a fixed set, saving **memory** (no `__dict__`), improving **performance** in large object collections, but limiting dynamic attribute addition.

## Descriptors and Properties
1. **Explain descriptors in Python.**  
   **Answer:** **Descriptors** are objects with `__get__`, `__set__`, `__delete__` methods controlling attribute access; used for **validation**, **lazy loading**, and **properties** via class-level definition.

2. **What are properties in Python and how do they work?**  
   **Answer:** **Properties** use `@property` decorator for **getter**, `@<attr>.setter` for **setter**, enabling **computed attributes** with validation; they leverage **descriptor protocol** for controlled access.

3. **How does the descriptor protocol (`__get__`, `__set__`, `__delete__`) work?**  
   **Answer:** **`__get__(self, obj, type)`** retrieves values; **`__set__(self, obj, value)`** sets with validation; **`__delete__(self, obj)`** deletes; invoked automatically during **attribute access** in classes.

## Metaclasses
1. **What are metaclasses in Python? When are they useful?**  
   **Answer:** **Metaclasses** are "classes of classes" (e.g., `type`) customizing **class creation** via `__new__` or `__init__`; useful for **enforcing patterns**, **logging class defs**, or **ORM** field validation.

2. **How do you create custom metaclasses to influence class behavior?**  
   **Answer:** Define `class MyMeta(type): def __new__(cls, name, bases, dct): ...`; assign `metaclass=MyMeta` in class; overrides **class construction** for adding methods or validation.

3. **Discuss metaclasses in the context of implementing design patterns like Abstract Base Classes.**  
   **Answer:** **ABCs** use metaclasses (e.g., `ABCMeta`) to enforce **abstractmethod** registration and **virtual subclass checks**; enables **duck typing** enforcement in **multiple inheritance** scenarios.

## Advanced Decorators and Context Managers
1. **What is a decorator in Python, and how is it used?**  
   **Answer:** A **decorator** is a callable wrapping functions/classes for **AOP** (e.g., timing); use `@decorator` syntax or `func = decorator(func)` to modify behavior without altering code.

2. **How can decorators be used for performance monitoring and caching?**  
   **Answer:** **Decorators** wrap functions with **@wraps** for metadata; for **caching** (e.g., `@lru_cache`), store results in **dict**; for **monitoring**, use `time.perf_counter()` to log execution time.

3. **Explain context managers and the `with` statement.**  
   **Answer:** **Context managers** handle **resource setup/teardown** via `__enter__` (entry) and `__exit__` (exit, exception handling); used with **`with`** for RAII-like safety in files, locks.

## Concurrency and Parallelism
1. **What are Python's concurrency mechanisms and how do they differ from traditional threading models?**  
   **Answer:** **Concurrency**: **threading** (OS threads, GIL-limited), **multiprocessing** (processes, CPU-bound); differs from traditional by **GIL** restricting true parallelism in threads, favoring **asyncio** for I/O.

2. **How do you create and manage threads in Python, and what are their limitations?**  
   **Answer:** Use `threading.Thread(target=func).start()`; manage with `join()`, `Lock`; **limitations**: **GIL** blocks CPU parallelism, race conditions need **synchronization** (e.g., `Queue`).

3. **Explain the Global Interpreter Lock (GIL) in Python and its implications for concurrent programming.**  
   **Answer:** **GIL** serializes **bytecode execution** in CPython for thread safety; implications: no **true parallelism** for CPU-bound tasks in **multithreading**, pushes to **multiprocessing** or **asyncio**.

4. **What is the multiprocessing module in Python and how does it help bypass the GIL?**  
   **Answer:** **`multiprocessing`** spawns **separate processes** with `Process(target=func)`; bypasses **GIL** by isolating interpreters, enabling **true parallelism** for CPU-intensive tasks via `Pool`.

5. **How does multithreading work in Python despite the GIL?**  
   **Answer:** **Multithreading** excels in **I/O-bound** tasks where threads yield (releasing **GIL** briefly); **GIL** allows context switches, but CPU-bound tasks serialize, mitigated by C extensions releasing GIL.

## Async Programming
1. **What is asynchronous programming in Python, and how does the async/await syntax work?**  
   **Answer:** **Asynchronous programming** uses **coroutines** for non-blocking I/O; **`async def`** defines functions returning **awaitables**; **`await`** suspends until complete, run via **event loop**.

2. **Explain the use of async/await for asynchronous I/O operations.**  
   **Answer:** **`async/await`** with `asyncio` (e.g., `await aiohttp.get()`) enables **concurrent I/O** without blocking; **event loop** schedules tasks, improving throughput in **networking** or **file ops**.

3. **How do coroutines differ from threads?**  
   **Answer:** **Coroutines** are **lightweight**, user-space scheduled via **event loop** (no OS overhead); **threads** are OS-managed with **context switching** costs; coroutines avoid **GIL** issues for I/O.

4. **What is the difference between asynchronous programming and multithreading?**  
   **Answer:** **Async** uses **cooperative multitasking** (explicit yields via `await`) for **I/O-bound**; **multithreading** is **preemptive** (OS-scheduled) but **GIL-limited**; async scales better for concurrency.

5. **How does async/await syntax work under the hood?**  
   **Answer:** **`async def`** yields **coroutine objects**; **`await`** calls `.__await__()` to suspend; **event loop** (e.g., `asyncio.run()`) resumes via **Future** resolution in **state machine**.

## Typing
1. **What is typing in Python, and how do type hints improve code?**  
   **Answer:** **Typing** uses annotations (e.g., `def func(x: int)`) for **static analysis**; improves **readability**, **IDE support**, **error catching** via tools like **mypy**, without runtime cost.

2. **How do you use type hints with libraries like typing module for function annotations?**  
   **Answer:** Import `from typing import List, Optional`; annotate as `def func(items: List[str]) -> Optional[int]:`; supports **generics**, **unions** for complex types in **function signatures**.

3. **How does Python's type hinting improve code quality?**  
   **Answer:** **Type hinting** enables **static checking** (mypy), reduces **runtime errors**, enhances **documentation**, and supports **refactoring** in large codebases.

## Performance and Profiling
1. **What is performance profiling in Python, and how do you use tools like cProfile?**  
   **Answer:** **Profiling** measures execution time/memory; `cProfile` via `cProfile.run('code')` or `@profile` decorator outputs **call counts**, **cumulative time** for bottleneck identification.

2. **Explain how to identify bottlenecks using Python's profiling tools.**  
   **Answer:** Use **`cProfile`** for **deterministic** stats, **`timeit`** for microbenchmarks, **`line_profiler`** for per-line; sort by **total time** to pinpoint **hot paths** and optimize.

## Design Patterns
1. **Describe the Singleton design pattern and its implementation in Python.**  
   **Answer:** **Singleton** ensures one instance via **module-level** or **metaclass** lock; implement with `__new__` checking `instance` attribute, or `@singleton` decorator for thread-safe creation.

2. **Explain the Factory design pattern and its application in Python.**  
   **Answer:** **Factory** creates objects without specifying exact class (e.g., `AnimalFactory.create('dog')`); uses **if/elif** or **dict mapping** for **encapsulation** of instantiation logic.

3. **How does the Observer design pattern work in Python for event handling?**  
   **Answer:** **Observer** notifies dependents of state changes; implement with **Subject** (add/remove observers, notify via callback list) for **decoupled** pub-sub in **GUI** or **events**.

## Advanced Testing (Mocks, Fixtures, Hypothesis)
1. **What is the difference between a fixture and a mock in Pytest?**  
   **Answer:** **Fixture** sets up/teardown resources (e.g., `@pytest.fixture` for DB conn); **mock** replaces dependencies (e.g., `Mock()`) for **isolation** and side-effect simulation.

2. **What is the pytest-mock plugin, and how do you use it?**  
   **Answer:** **`pytest-mock`** provides `mocker` fixture for easy **patching**; use `mocker.patch('module.func', return_value=42)` to mock calls in tests.

3. **What is a parametrized fixture in Pytest?**  
   **Answer:** **Parametrized fixture** uses `@pytest.fixture(params=[1,2])` to run setup multiple times with different **parameters**, enabling **data-driven** testing.

4. **How do you use fixtures in a class with Pytest?**  
   **Answer:** Declare `def test_method(self, fixture):` in `class TestClass:`; **autouse=True** applies globally; supports **class-level** setup via `setup_method`.

5. **What is the scope of a fixture in Pytest, and how do you control it?**  
   **Answer:** **Scope** ('function', 'class', 'module', 'session') controls reuse; set via `scope='module'` to minimize setup overhead across tests.

## Packaging, Deployment, and CI/CD Basics
1. **How would you build and distribute a Python package as a wheel using setuptools?**  
   **Answer:** In `setup.py`: `from setuptools import setup; setup(...)`; build with `python setup.py bdist_wheel`; distribute via **PyPI** upload with `twine`.

2. **Explain how to set up continuous integration for a Python project using GitHub Actions.**  
   **Answer:** Create `.github/workflows/ci.yml` with `on: push`; steps: checkout, `pip install -r requirements.txt`, `pytest`; runs on **pull requests** for automated testing.

3. **What are common deployment strategies like blue-green deployments in Python applications?**  
   **Answer:** **Blue-green** runs two environments (blue live, green staging); switch traffic atomically post-deploy; minimizes **downtime** in **Flask/Django** apps via load balancers.

4. **How do you Dockerize a Python application for production?**  
   **Answer:** `Dockerfile`: `FROM python:3.12`, `COPY . /app`, `RUN pip install -r requirements.txt`, `CMD ["python", "app.py"]`; build/tag with `docker build -t app .`; run with **multi-stage** for optimization.