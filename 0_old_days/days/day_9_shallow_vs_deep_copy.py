
shallow_copy = "one level deep, only references of nested child objects"
deep_copy = " a fully independent object"

ls = [1,2,3]

import copy

cpy = copy.copy(ls) #same as ls.copy(), list(ls), ls[:]

cpy.append(-10)

# print(ls)
# print(cpy)

#this works fine with one level deep, not for example a list of lists

mat = [[1,2,3],[4,5,6],[7,8,9]]
print(mat)
#mat2 = mat.copy()
mat2 = copy.deepcopy(mat) #with copy

mat2[0][0] = -10
print(mat2)
print(mat) #still references old mat

class Person():
    def __init__(self,name,age):
        self.name = name
        self.age = age

p1 = Person("alex",10)
p2 = Person("jax",15) #mutable, same problem as lists, dicts

#same as previous, use shallow copy if one level, else if nested deep copy

class Company():
    def __init__(self,boss,worker):
        self.boss = boss
        self.worker = worker

comp = Company(p1,p2)

#comp2 = copy.copy(comp)
comp2 = copy.deepcopy(comp)

comp2.boss.age = 100

print(comp.boss.age)
print(comp2.boss.age)