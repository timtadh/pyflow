'''Starting point for the c compiler'''
import gram, c_types, tables

def construct_basic_types(typedef_table):
    typedef_table.create_type(c_types.ScalarType('void', 0))
    typedef_table.create_type(c_types.ScalarType('char', 1))
    typedef_table.create_type(c_types.ScalarType('short', 2))
    typedef_table.create_type(c_types.ScalarType('short int', 2))
    typedef_table.create_type(c_types.ScalarType('int', 4))
    typedef_table.create_type(c_types.ScalarType('long', 4))
    typedef_table.create_type(c_types.ScalarType('float', 4))
    #typedef_table.create_type(c_types.PointerType('pointer', 4))
    typedef_table.create_type(c_types.ScalarType('double', 8))
    typedef_table.create_type(c_types.ScalarType('long long', 8))

def construct_parser():
    symbol_table = tables.SymbolTable()
    typedef_table = tables.TypedefTable()
    construct_basic_types(typedef_table)
    c_parser = gram.C_Parser(symbol_table, typedef_table)
    c_parser.build()
    return c_parser
