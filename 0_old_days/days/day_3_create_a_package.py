#I now know how to create a python package

class PythonPackage(object):
    def __init__(self,args):
        self.init_file = args['init']
        self.files = args['files']
        self.internal_packages = [PythonPackage(p['arguments']) for p in args['internal_packages']]