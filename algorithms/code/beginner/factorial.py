# factoriel


import time 
import math

def measure_time(func):
  def wrap(*args, **kwargs):
    start = time.time()
    res = func(*args, **kwargs)
    print("duration ", time.time() - start)
    return res 
  return wrap

@measure_time
def fact(n):
  res = 1 
  for i in range(1,n+1):
    res = res * i 

  return res 

n = 100
fact(n)
start = time.time()
math.factorial(n)
end = time.time() - start
print("duration ", end)