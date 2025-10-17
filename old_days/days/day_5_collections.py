from collections import Counter, namedtuple #like struct


ls = [1,2,3,5,6,7]
string = "khaled adrani"

counter = Counter(string)
famous = counter.most_common(3)

#print(famous)

Point = namedtuple("Point","x,y")
pt =  Point(1,-4)
#print(pt, pt.x, pt.y)

from collections import OrderedDict #remember order of insertion,

odic = OrderedDict()

odic["first"] = 1
odic["second"] = 2
odic["third"] = 3

#print(odic)

from collections import defaultdict #default dict value

d = defaultdict(int)

from collections import deque #from the two directions, append, remove

d = deque([i for i in range(0,10)])
print(d)

d.append(10)
d.appendleft(-1)

print(d)

d.extend([20,30,40])

print(d)

d.rotate(2)

print(d)

