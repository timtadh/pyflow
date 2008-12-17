'''Symbol and TypeDef Tables'''
import c_types

class SymbolTable(object):
    
    def __init__(self):
        self.table = dict()
    
    def create_symbol(self, identifier):
        '''create_symbol(identifier):
            symbol = c_types.Identifier'''
        if self.table.has_key(identifier.name):
            raise Exception, 'identifier "%s" was already in table' % identifier.name
        self.table.update({identifier.name:identifier})
    
    def find_symbol(self, name):
        '''find_symbol(name):
            name = c_types.Identifier.name whatever was in the name field of the id you are 
                   looking for
           returns c_types.Identifier or None if the symbol was not found'''
        if self.table.has_key(name): return self.table[name]
        else: return None
    
    def __str__(self):
        return str(self.table)

class TypedefTable(object):
    
    def __init__(self):
        self.table = dict()
    
    def create_type(self, type):
        '''create_type(type):
            type = one of the types from the c_types module'''
        if self.table.has_key(type.type_name):
            raise Exception, 'type "%s" was already in table' % type.type_name
        self.table.update({type.type_name:type})
    
    def find_type(self, name):
        '''find_type(name):
            name = type_name
           returns a Type from c_types or None if the type was not found'''
        if self.table.has_key(name): return self.table[name]
        else: return None
    
    def __str__(self):
        return str(self.table)

if __name__ == '__main__':
    symbol_table = SymbolTable()
    i = c_types.Identifier('main')
    symbol_table.create_symbol(i)
    print i
    del i
    g = symbol_table.find_symbol('main')
    print g
    g.value = '7'
    print g
    del g
    h = symbol_table.find_symbol('main')
    print h
    
    typedef_table = TypedefTable()
    t = c_types.ScalarType('int', 4)
    typedef_table.create_type(t)
    print t
    del t
    v = typedef_table.find_type('int')
    print v
    v.size = 8
    print v
    del v
    w = typedef_table.find_type('int')
    print w