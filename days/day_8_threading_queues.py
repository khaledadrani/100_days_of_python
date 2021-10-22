from threading import Thread, Lock, current_thread
from queue import Queue
from time import time
from requests import request

def worker(q,lock):
    while True:
        val = q.get()
        with lock:
            print(f"{current_thread().name} is working with {val}")
        q.task_done()

if __name__=="__main__":

    print("START MAIN")

    q = Queue(maxsize=0)
    lock = Lock()
    num_threads = 10

    for i in range(num_threads):
        thread = Thread(target=worker, args=(q,lock))
        thread.daemon = True #obligatory 
        thread.start()

    for i in range(1,30):
        q.put(i)

    q.join()

    print("END MAIN")