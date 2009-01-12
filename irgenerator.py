'''Classes and functions to support the generation an intermediate representation'''
import c_types, ircode

class IRGenerator(object):
    
    def __init__(self, symbol_table, typedef_table):
        self.symbol_table = symbol_table
        self.typedef_table = typedef_table
        self.tempcount = 0
    
    def next_temporary(self, type=None):
        name = 't%d' % self.tempcount
        self.tempcount += 1
        while self.symbol_table.in_table(name): 
            name = 't%d' % self.tempcount
            self.tempcount += 1
        identifier = c_types.Identifier(name, type=type)
        self.symbol_table.create_symbol(identifier)
        return identifier
    
    def load_constant(self, const):
        temp = self.next_temporary(const.type)
        temp.value = const.value
        statements = [ircode.Statement(ircode.CopyType, result=temp, operand=const)]
        return temp, statements
    
    def unary_operation(self, operator, operand):
        if operand: temp = self.next_temporary(operand.type)
        else: temp = self.next_temporary()
        statements = [ircode.Statement(ircode.UnaryAssignmentType, result=temp, operator=operator,
                                                                   operand=operand)]
        return temp, statements
    
    def binary_operation(self, operator, operand_1, operand_2):
        print operator, operand_1, operand_2
        assert operand_1.type == operand_2.type
        temp = self.next_temporary(operand_1.type)
        statements = [ircode.Statement(ircode.BinaryAssignmentType, result=temp, operator=operator,
                                                          operand_1=operand_1, operand_2=operand_2)]
        return temp, statements
    
    def copy(self, source, target):
        assert source.type == target.type
        statements = [ircode.Statement(ircode.CopyType, result=target, operand=source)]
        return target, statements
