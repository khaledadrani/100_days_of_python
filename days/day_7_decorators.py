import functools

#decorator template with args
def decor(repeat):
    def decorator_decor(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            res = 0
            for _ in range(repeat):
                res += func(*args,**kwargs)
            return res

        return wrapper
    return decorator_decor
class countCalls:
    def __init__(self,func):
        self.func = func
        self.n_calls = 0

    def __call__(self, *args, **kwds):
        self.n_calls += 1
        res = self.func(*args,**kwds)
        print(f"Function executed {self.n_calls} times")
        return res

@countCalls
@decor(repeat=3)
def do_stuff(i):
    return i * 5

#print(help(do_stuff))
print(do_stuff(10))
print(do_stuff(20))
print(do_stuff(5))

#usage: check debug time cach update state logging
