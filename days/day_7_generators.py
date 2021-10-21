
def generate_below(max):
    for x in range(max):
        yield x 

max = 1000

gen = generate_below(max)
ls = [i for i in range(max)]

import sys

# print(sys.getsizeof(gen)/1024)
# print(sys.getsizeof(ls)/1024)

# print(next(r))
# print(next(r))
# print(next(r))

def fibon(limit):
    a,b = 0,1
    while a < limit:
        yield a
        a,b=b,a+b

# gen = fibon(1000)

# for i in gen:
#     print(i)

gen = (i for i in range(max) if i%2 == 2 )
