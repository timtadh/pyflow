'''Semantic representation of three address code'''

class Operators(object):
    '''Empty base class for three address code operators'''
    
class BinaryOperators(object):
    '''Binaray operators for three address code'''
    assignment = '='
    adition = '+'
    subtraction = '-'
    multiplication = '*'
    division = '/'
    modulus = '%'
    exponentiate = '**'
    binary_and = '&'
    inclusive_or = '|'
    exclusive_or = '^'
    shift_right = '>>'
    shift_left = '<<'
    lt = '<'
    le = '<='
    gt = '>'
    ge = '>='
    eq = '=='
    nq = '!='

class UnaryOperators(object):
    '''Unary operators for three address code'''
    negate = '-'
    posit = '+'
    address = '&'
    value = '*'
    compliment = '~'

class StatementType(object):
    '''Base class for three address statement types'''
    fields = []
    
    @staticmethod
    def format(statement):
        assert statement.type == StatementType
        return ''
    
class BinaryAssignmentType(StatementType):
    '''r = o1 bin_op o2'''
    result = 'The c_types.Identifier where the result of the operation goes'
    operator = 'An opertor from BinaryOperators'
    operand_1 = 'A constant or c_types.Identifier'
    operand_2 = 'A constant or c_types.Identifier'
    fields = ['operand_1', 'operand_2', 'operator', 'result']
    
    @staticmethod
    def format(statement):
        assert statement.type == BinaryAssignmentType
        s = str(statement.result) + ' = '
        s += str(statement.operand_1) + ' '
        s += str(statement.operator) + ' '
        s += str(statement.operand_2)
        return s

class UnaryAssignmentType(StatementType):
    '''r = unary_op o'''
    result = 'The c_types.Identifier where the result of the operation goes'
    operator = 'An opertor from BinaryOperators'
    operand = 'A constant or c_types.Identifier'
    fields = ['operand', 'operator', 'result']
    
    @staticmethod
    def format(statement):
        assert statement.type == UnaryAssignmentType
        s = str(statement.result) + ' = '
        s += str(statement.operator) + ' '
        s += str(statement.operand)
        return s

class CopyType(StatementType):
    '''r = o'''
    result = 'The c_types.Identifier where the result of the operation goes'
    operand = 'A constant or c_types.Identifier'
    fields = ['operand', 'result']
    
    @staticmethod
    def format(statement):
        assert statement.type == CopyType
        s = str(statement.result) + ' = '
        s += str(statement.operand)
        return s

class IndexedCopyType(StatementType):
    '''r = o[i]'''
    result = 'The c_types.Identifier where the result of the operation goes'
    operand = 'A c_types.Identifier the type must be c_types.VectorType'
    index = 'The index of the array beign accessed'
    fields = ['index', 'operand', 'result']
    
    @staticmethod
    def format(statement):
        assert statement.type == IndexedCopyType
        s = str(statement.result) + ' = '
        s += str(statement.operand) + '['
        s += str(statement.index) + ']'
        return s

class UnconditionalJumpType(StatementType):
    '''goto label'''
    label = 'The label where the jump is going to'
    fields = ['label']
    
    @staticmethod
    def format(statement):
        assert statement.type == UnconditionalJumpType
        s = 'goto ' + str(statement.label)
        return s

class ConditionalJump(StatementType):
    '''if x: goto label'''
    operand = '''A constant or c_types.Identifier, note this will evaluate for false if all zero 
                 true otherwise'''
    label = 'Target of the jump if operand evaluates to true'
    fields = ['label', 'operand']
    
    @staticmethod
    def format(statement):
        assert statement.type == ConditionalJump
        s = 'if ' + str(statement.operand) + ': '
        s += 'goto ' + str(statement.label)
        return s

class RelationalExpressionConditionalJump(StatementType):
    '''if x rel_op y: goto label'''
    operator = 'An opertor from BinaryOperators restrict yourself to the realtional'
    operand_1 = 'A constant or c_types.Identifier'
    operand_2 = 'A constant or c_types.Identifier'
    label = 'Target of the jump if operand evaluates to true'
    fields = ['label', 'operand_1', 'operand_2', 'operator']
    
    @staticmethod
    def format(statement):
        assert statement.type == RelationalExpressionConditionalJump
        s = 'if ' + str(statement.operand_1) + ' '
        s += str(statement.operator) + ' '
        s += str(statement.operand_2) + ': '
        s += 'goto ' + str(statement.label)
        return s

class ParameterType(StatementType):
    '''param x'''
    parameter = 'A constant or c_types.Identifier'
    fields = ['parameter']
    
    @staticmethod
    def format(statement):
        assert statement.type == ParameterType
        s = 'param ' + str(statement.parameter)
        return s

class ProcedureCallType(StatementType):
    '''param x1
       param x2
       ...
       param xn
       call procedure, n'''
    parameter_list = 'A list of parameters to be passed into the parameter'
    procedure = 'The procedure being called'
    fields = ['parameter', 'procdure']
    
    @staticmethod
    def format(statement):
        assert statement.type == ProcedureCallType
        s = '\n'.join([ParameterType.format(parameter) for parameter in statement.parameter_list])
        s += '\n' + 'call ' + str(statement.procedure) + ', ' + str(len(statement.parameter_list))
        return s

class Statement(object):
    '''Represents a three adress code statement'''
    
    def __init__(self, statement_type, **kwargs):
        self.type = statement_type
        keys = kwargs.keys()
        keys.sort()
        assert keys == self.type.fields
        for key in keys:
            self.__setattr__(key, kwargs[key])
    
    def get(self, attr):
        return self.__getattribute__(attr)
    
    def __str__(self):
        return self.type.format(self)