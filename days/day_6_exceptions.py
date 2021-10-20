x = 10

#assert (x>100), "x should be bigger than 100"

class SmallValue(Exception):
    def __init__(self,message,value):
        self.message = message
        self.value = value

def funct(x):
    if x < 100:
        raise SmallValue("Value too small",x)



try:
    funct(30)
except Exception as err:
    print(err)