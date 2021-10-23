class ManagedFile(): #with resources, files, threads,
    def __init__(self, filename):
        self.filename = filename
    
    def __enter__(self):
        print("Enter")
        self.file = open(self.filename,'w')
        return self.file

    def __exit__(self,exc_type,exc_value,exc_traceback):
        if self.file:
            self.file.close()
        if exc_type is not None:
            print("handle exception")
        print("exit")
        return True #add this if you handle exception


# with ManagedFile('some_text.txt') as file:
#     print("do some stuff")
#     file.somemethod()
#     file.write("some todo")


from contextlib import contextmanager

@contextmanager
def open_managed_file(filename):
    f = open(filename,'a+')
    try: #enter
        yield f
    finally: #exit
        f.close()

with open_managed_file("./data/some_text.txt") as f:
    print(f)
    f.write("dodododdod")