import random

random.seed(42)
a = random.random()
a = random.uniform(1,10)

a = random.randint(1,10) #max inclusive
a = random.randrange(1,10) 
a= random.normalvariate(0,10)

ls = list("khaled adrani")

a = random.choice(ls)

s = random.sample(ls,3)

s = random.choices(ls,k=3) #with repetition

random.shuffle(ls) #inplace

import secrets
a = secrets.randbelow(10)
b = secrets.randbits(10)
c = secrets.choice(ls)

#print(a,b,c)

import numpy as np

np.random.seed(42)

a = np.random.rand(3,10)

l = np.random.randint(10,20,100)

mat = np.random.randint(10,20,(3,3))

print(mat)
np.random.shuffle(mat)
print(mat)