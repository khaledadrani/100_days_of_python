
#real parallel programming
process = {"def":"an instance of a program like Python Interpreter",
           "Memory": "Not shared between processes",
           "Great":["Intensive computation, (with a lot of data)",
                    "independent","easily interruptable killable","avoids GIL"],
            "Bad":["heavyweight, slower startup, more memory","inter communic is diffic"]}


thread = {"def":"an entity within a process that can be scheduled",
           "Memory": "shares between threas, they are spawned from same process",
           "Great":["IO bound tasks, talk to a device, connection",
                    "faster startup"],
            "Bad":["GIL limitation","not interruptable","no for CPU intensive tasks","careful race condition"]}

gil = {"def":"global interpreter locker",
        "need":"CPython is not thread safe",
        "issue":'''memorize references counting to objects in code, 
        need to keep track of it so it can be released, so when two threads modify this count, risk''',
        "avoid":["multiprocessing","free-threaded like Jython, IronPython", "python as wrapper for 3rd party library, numpy, scipy, c,c++"]}

import random
import time

def my_func(max,i):
    print(f"{i} is running!")
    time.sleep(30)
    random.seed(i)
    return random.randint(0,max)

from multiprocessing import Process
import os

def test_proc():
    print("Start processing")
    processes = []
    num_proc = os.cpu_count()
    print(num_proc)

    for i in range(num_proc):
        p = Process(target=my_func, args=(10,i))
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes: #block main thread until all processes are done
        p.join()

from threading import Thread

def test_thread():
    print("Start threading")
    threads = []
    num_threads = 10

    for i in range(num_threads):
        t = Thread(target=my_func,args=(10,i))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    test_proc()

