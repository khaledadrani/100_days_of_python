from itertools import product #the Cartesian product of two sets A and B, denoted A × B

a = [1,2]
b = [3,4]

p = product(a,b)
p2 = p = product(a,b, repeat=2)

#print(list(p2))

from itertools import permutations

a = [1,2,3,4]

perm = permutations(a) 

print(list(perm))