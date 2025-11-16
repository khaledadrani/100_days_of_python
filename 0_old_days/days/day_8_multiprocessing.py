from multiprocessing import Process, Value, Array, Lock, current_process, Queue
import os
import time
import random 

def worker(lock,variable):
    time.sleep(0.1)
    with lock:
        variable.value += 1
        print(f"{current_process().name} has value {variable.value}")

    
def array_worker(lock, array,len_arr):
    time.sleep(0.2)
    index = random.randrange(len_arr)
    with lock:
        array[index] += 1
        print(f"{current_process().name} modified index {index} so it becomes {array[index]}")

def queue_worker(lock):
    pass
def first_part():

    nb_procs = os.cpu_count()

    lock = Lock()
    shared_var = Value("i",0)

    len_arr = 10
    shared_array = Array("d",[0]*len_arr)
    #procs = [Process(target=worker,args=(lock,shared_var)) for _ in range(nb_procs)]
    procs = [Process(target=array_worker,args=(lock,shared_array,len_arr)) for _ in range(nb_procs)]

    for p in procs:
        p.start()

    for p in procs:
        p.join()

    print("Final Value ",list(shared_array))


def producer(lock,shared_var,q):
    time.sleep(1)
    with lock:
        if shared_var.value>=0:
            q.put(1)
            shared_var.value += 1
            print(f"Producer {current_process().name} value is {shared_var.value}")

        


def consumer(lock,shared_var,q):
    time.sleep(1)
    with lock:
        if shared_var.value>=0:
            q.get()
            shared_var.value -= 1
            print(f"Consumer {current_process().name} value is {shared_var.value}")
        
if __name__ == "__main__":
    q = Queue()

    nb_producers = 2
    nb_consumers = 2

    shared_var = Value("d",0.0)

    lock = Lock()

    producers = [Process(target=producer,args=(lock,shared_var,q)) for _ in range(nb_producers)]
    consumers = [Process(target=consumer,args=(lock,shared_var,q)) for _ in range(nb_consumers)]

    for p in producers:
        p.start()

    for p in consumers:
        p.start()

    for p in consumers:
        p.join()

    for p in producers:
        p.join()

    print("Final ",shared_var.value)


