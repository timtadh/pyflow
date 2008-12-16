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
           returns c_types.Identifier or None if the symbols was not found'''
        if self.table.has_key(name): return self.table[name]
        else: return None
    
    def update_symbol(self, identifier):
        '''update_symbol(identifier):
            symbol = c_types.Identifier'''
        if self.table.has_key(identifier.name): self.table[identifier.name] = identifier
        else: raise Exception, 'identifier "%s" was not in the table' % identifier.name

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
