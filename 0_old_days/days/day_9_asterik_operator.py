
ls = [i for i in range(10)]

head, *tail = ls
*body, leg = ls
start, *middle, last = ls


print(head,tail)
print(body,leg)
print(start, middle, last)

start, *middle, secondlast, last = ls
print(start, middle, secondlast, last)

print("merging")

ls = [1,2,3]
ls2 = [4,5,6]
sett = {4,5,6} #with tuple too
print([*ls,*ls2])
print([*ls,*sett])

dic1 = {c:ord(c) for c in "khaled"}
dic2 = {c:ord(c) for c in "adrani"}

print({**dic1,**dic2})

