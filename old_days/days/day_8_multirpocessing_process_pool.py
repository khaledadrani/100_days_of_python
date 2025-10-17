from multiprocessing import Pool
import time

def cube(number):
    time.sleep(1)
    return number**3

if __name__ == "__main__":

    pool = Pool()
    numbers = range(10)

    result = pool.map(cube,numbers)
    #pool.apply
    pool.close()
    pool.join()

    print(result)


