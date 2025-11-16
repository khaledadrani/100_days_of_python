
points = [(1,3),(1,5),(5,6),(7,7)]

sort_points_x = sorted(points, key=lambda x:x[0],reverse=True)

#print(sort_points_x)

b = map(lambda x: (x[0],-x[1]), points)
#with list comprehension

b = [(e[0],-e[1]) for e in points]

b = filter(lambda x: x[0] < 4, points)

from functools import reduce

ls = [1,2,3,4,5,6,7]

b = reduce(lambda x,y: x*y,ls)
print(b)