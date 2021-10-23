
ls = [1,2,3]

dic = {"name":"khaled","city":"ariana","age":10}

def power_func(*args):
    for arg in args:
        print("before ",arg)
        yield arg * 2

def print_dic(**kwargs):
    for k in kwargs:
        print(k,"=> ",kwargs[k])

def both_args(a,b,*args,**kwargs):
    print(a,b)
    for arg in args:
        print(args)
    for k in kwargs:
        print(k,kwargs[k])


# for e in power_func(*ls):
#     print("after ",e)

#both_args(10,20,*ls,**dic)

#both_args(10,20,30,40,first=5,second=4)

def forced_args_as_keywords(a,b,*,c,d):
    print(a,b,c,d)

if False:
    forced_args_as_keywords(10,20,30,d=40) #false
    forced_args_as_keywords(10,20,c=30,d=40) #correct
    forced_args_as_keywords(a=10,b=20,c=30,d=40) #correct: positional can be keywords

def forced_last_keywords(*args,last):
    print([arg for arg in args],last)

#forced_last_keywords(ls,last=15)

def my_func(*args):
    for arg in args:
        print(arg)


gen = (i for i in range(10))

#my_func(*gen)

def my_func(name,age,city):
    print(name,age)


my_func(**dic)


