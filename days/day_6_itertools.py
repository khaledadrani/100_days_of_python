from itertools import product, combinations, permutations, combinations_with_replacement,accumulate, groupby
import operator

a = [1,2,3,4]
b= [-1,-2,-3,-4]

pr = product(a,b) #cartesian product, A x B
p = permutations(a,2) #all possible ORDERING
c = combinations(a,2) #all possible groups, combinations
cr = combinations_with_replacement(a,2)
acc = accumulate(a,func=operator.mul)

# print(a, list(acc))
# print(list(c))
# print(list(cr))
def smaller(x):
    return x<3
gp = groupby(a, key=smaller)

# for key, value in gp:
#     print(key,list(value))


from itertools import count, cycle, repeat

a = [1,2,3]
for i in repeat(a,3):
    print(i)