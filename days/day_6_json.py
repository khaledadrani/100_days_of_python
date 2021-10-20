data = {"name":"khaled","age":10,"city":"Ariana","family":["ramadhan","khadija","riadh","khouloud"]}

import json

jsdata = json.dumps(data,indent=4)
#print(jsdata)

# with open("person.json","w") as file:
#     json.dump(data,file,indent=4)


with open("person.json","r") as file:
    person = json.load(file)
    #print(person)

class Person:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def encode_user(self):
        if isinstance(self,Person):
            print(True)

user = Person("Joe",10)

def encode_person(o):
    if isinstance(o,Person):
        return {"name":o.name,
                "age":o.age,
                o.__class__.__name__: True}
    else:
        raise TypeError("Object of type Person is not JSON serializable")

data = json.dumps(user,default=encode_person,indent=4)

# print(data)
# print(type(data))

obj = json.loads(data)
# print(obj)
# print(type(obj))

def decode_person(dic):
    if Person.__name__ in dic:
        return Person(dic['name'],dic['age'])
    else:
        return dic

print(obj)
perso = json.loads(data,object_hook=decode_person)
print(perso.name)

