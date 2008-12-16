'''Classes representing C types for pyflow'''

class ScalarType(object):
    '''This represents atomic types like int, long, float, char etc...'''
    
    def __init__(self, type_name, size):
        '''ScalarType(type_name, size):
            type_name = name of the type, ie int, char ....
            size = size in bytes'''
        self.type_name = type_name
        self.size = size

class VectorType(ScalarType):
    '''This represents arrays ie int[5] or int[2][3][4][5] doesn't matter the demension'''
    
    def __init__(self, base_type, length):
        '''VectorType(base_type, length):
            base_type = any other kind of type including ScalarType, VectorType, UnionType, StructType
            length = how long the vector should be'''
        super(VectorType, self).__init__(base_type.type_name, base_type.size)
        self.length = length
        self.size = self.length * self.size

class UnionType(ScalarType):
    '''Represents C unions'''
    
    def __init__(self, type_name, members):
        '''UnionType(type_name, members):
            type_name = name of the union
            members = a list of Identifiers'''
        self.members = members
        longest = 0
        for member in members:
            if longest < member.type.size: longest = member.type.size
        super(UnionType, self).__init__(type_name, longest)

class StructType(UnionType):
    '''Represents C structs'''
    
    def __init__(self, type_name, members):
        '''StructType(type_name, members):
            type_name = name of the union
            members = a list of Identifiers'''
        super(StructType, self).__init__(type_name, members)
        self.size = len(self.members) * self.size

class FunctionType(object):
    '''Represents functions'''
    
    def __init__(self, name, return_type, parameters=None, code=None):
        '''FunctionType(name, return_type, parameters=None, code=None)'''
        self.name = name
        self.return_type = return_type
        self.parameters = parameters
        self.code = code

class Identifier(object):
    '''Represents an identifier. Each Identifier has a name, value, type and address'''
    
    def __init__(self, name, value=None, type=None, address=None):
        '''Identifier(name, value=None, type=None, address=None)'''
        self.name = name
        self.value = value
        self.type = type
        self.address = address
    
    def __str__(self):
        return str(self.name) + ' -> ' + str(self.value)