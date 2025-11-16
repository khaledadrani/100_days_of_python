from threading import Thread, Lock, current_thread
import functools
import time



database_value = 0

def timer(arg):
    print(arg)
    def decorator_timer(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            start = time.time()
            res = func(*args,**kwargs)
            end = time.time()
            print(f"Thread {args[0]} duration => {end-start}")
            return res
        return wrapper
    return decorator_timer


@timer(arg=0)
def my_func(x):
    s = 0
    for i in range(x*10):
        s += i
    return s

@timer(arg=1)
def increase(x,lock):
    global database_value
    try:
        time.sleep(0.1*x)
        with lock:
            database_value += x
        return True
    except:
        return False



if __name__=="__main__":

    print("start ",database_value)
    lock = Lock()

    t1 = Thread(target=increase,args=(1,lock))
    t2 = Thread(target=increase,args=(15,lock))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    
    print("end ",database_value)

    