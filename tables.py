'''Symbol and TypeDef Tables'''
import c_types

class SymbolTable(object):
    
    def __init__(self):
        self.levels = list()
        self.global_space = dict()
        self.tables = list()
        self.current_level = -1 #negative one represents the global namespace
        self.current_table = self.global_space
        #self.current_namespace = 0 #zero represents the first namespace encounter
    
    def __namespace(self, level, count):
        return float(str(level) + '.' + str(count))
    
    def current_namespace(self):
        return self.__namespace(self.current_level, self.levels[self.current_level])
    
    def push_level(self):
        self.current_level += 1
        if self.current_level <= len(self.levels): 
            self.levels.append(-1)
            self.tables.append(list())
        self.levels[self.current_level] += 1
        #self.tables.update({self.current_namespace():dict()})
        self.tables[self.current_level].append(dict())
    
    def pop_level(self):
        if self.current_level != -1: self.current_level -= 1
    
    def top_current_table(self):
        if self.current_level >= 0:
            return self.tables[self.current_level][self.levels[self.current_level]]
        else:
            return self.global_space
        
    def get_current_tables(self):
        level = self.current_level
        tables = list()
        while level >= 0:
            tables.append(self.tables[level][self.levels[level]])
            level -= 1
        tables.append(self.global_space)
        return tables
    
    def create_symbol(self, identifier):
        '''create_symbol(identifier):
            symbol = c_types.Identifier'''
        current_table = self.top_current_table()
        if current_table.has_key(identifier.name):
            raise Exception, 'identifier "%s" was already in table' % identifier.name
        current_table.update({identifier.name:identifier})
    
    def find_symbol(self, name):
        '''find_symbol(name):
            name = c_types.Identifier.name whatever was in the name field of the id you are 
                   looking for
           returns c_types.Identifier or None if the symbol was not found'''
        current_tables = self.get_current_tables()
        for table in current_tables:
            if table.has_key(name): return table[name]
        raise Exception, "Symbol '%s' not in the symbol table -> %s" % (name, str(current_tables))
    
    def in_table(self, name):
        try:
            self.find_symbol(name)
            return True
        except:
            return False
    
    def __str__(self):
        return str(self.global_space) + ', ' + str(self.tables)

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