'''Semantic representation of three address code'''

class Operators(object):
    '''Empty base class for three address code operators'''
    
class BinaryOperators(object):
    '''Binaray operators for three address code'''
    assignment = '='
    addition = '+'
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
    inc = '++'
    dec = '--'
    not_op = '!'

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
        s = str(statement.result) + ' ' + BinaryOperators.assignment + ' '
        s += str(statement.operator)
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
        s = str(statement.result) + ' ' + BinaryOperators.assignment + ' '
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
        s = str(statement.result) + ' ' + BinaryOperators.assignment + ' '
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

class ConditionalJumpType(StatementType):
    '''if x: goto label'''
    operand = '''A constant or c_types.Identifier, note this will evaluate for false if all zero 
                 true otherwise'''
    label = 'Target of the jump if operand evaluates to true'
    fields = ['label', 'operand']
    
    @staticmethod
    def format(statement):
        assert statement.type == ConditionalJumpType
        s = 'if ' + str(statement.operand) + ': '
        s += 'goto ' + str(statement.label)
        return s

class RelationalExpressionConditionalJumpType(StatementType):
    '''if x rel_op y: goto label'''
    operator = 'An opertor from BinaryOperators restrict yourself to the realtional'
    operand_1 = 'A constant or c_types.Identifier'
    operand_2 = 'A constant or c_types.Identifier'
    label = 'Target of the jump if operand evaluates to true'
    fields = ['label', 'operand_1', 'operand_2', 'operator']
    
    @staticmethod
    def format(statement):
        assert statement.type == RelationalExpressionConditionalJumpType
        s = 'if ' + str(statement.operand_1) + ' '
        s += str(statement.operator) + ' '
        s += str(statement.operand_2) + ': '
        s += 'goto ' + str(statement.label)
        return s

class InParameterType(StatementType):
    '''param x'''
    param = 'A constant or c_types.Identifier'
    fields = ['param']
    
    @staticmethod
    def format(statement):
        assert statement.type == InParameterType
        s = 'inparam ' + str(statement.param)
        return s

class OutParameterType(StatementType):
    '''param x'''
    param = 'A constant or c_types.Identifier'
    fields = ['param']
    
    @staticmethod
    def format(statement):
        assert statement.type == OutParameterType
        s = 'outparam ' + str(statement.param)
        return s

class ProcedureCallType(StatementType):
    '''inparam x1
       inparam x2
       ...
       inparam xn
       outparam y1
       outparam y2
       ...
       outparam ym
       call procedure, n, m'''
    inparams = 'A list of parameters to be passed into the parameter'
    outparams = 'A list of parameters to be returned by the parameter'
    procedure = 'The procedure being called usually a c_types.Identifier'
    fields = ['inparams', 'outparams', 'procedure']
    
    @staticmethod
    def format(statement):
        assert statement.type == ProcedureCallType
        s = '\n'.join([InParameterType.format(param) for param in statement.inparams]) + '\n'
        s += '\n'.join([OutParameterType.format(param) for param in statement.outparams]) + '\n'
        s += 'call ' + str(statement.procedure) + ', ' + str(len(statement.inparams))
        s += ', ' + str(len(statement.outparams))
        return s

class ProcedureDefinitionType(StatementType):
    '''procedure f, in, out
       inparam x1
       inparam x2
       ...
       inparam xn
       statement 1
       statement 2
       ...
       statement n
       outparam y1
       outparam y2
       ...
       outparam ym
       endprocedure'''
    identifier = 'The procedure being called usually a c_types.Identifier'
    inparams = 'A list of parameters to be passed into the parameter'
    outparams = 'A list of parameters to be returned by the parameter'
    statements = 'A list of statements that define the body of the procedure'
    fields = ['identifier', 'inparams', 'outparams', 'statements']
    
    @staticmethod
    def format(statement):
        assert statement.type == ProcedureDefinitionType
        s = 'procedure ' + str(statement.identifier)
        s += ', ' + str(len(statement.inparams)) + ', ' + str(len(statement.outparams)) + '\n'
        s += '\n'.join([InParameterType.format(param) for param in statement.inparams]) + '\n'
        s += '\n'.join([str(x) for x in statement.statements]) + '\n'
        s += '\n'.join([OutParameterType.format(param) for param in statement.outparams]) + '\n'
        s += 'endprocedure'
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

if __name__ == '__main__':
    import c_types
    c_types.debug = 0
    x = c_types.Identifier('x')
    y = c_types.Identifier('y')
    z = c_types.Identifier('z')
    f = c_types.Identifier('f')
    bin_op = BinaryOperators.addition
    unary_op = UnaryOperators.negate
    rel_op = BinaryOperators.lt
    s = Statement(BinaryAssignmentType, result=z, operator=bin_op, operand_1=x, operand_2=y)
    assert str(s) == 'z = x + y'
    s = Statement(UnaryAssignmentType, result=z, operator=unary_op, operand=x)
    assert str(s) == 'z = -x'
    s = Statement(CopyType, result=z, operand=x)
    assert str(s) == 'z = x'
    s = Statement(IndexedCopyType, result=z, operand=x, index=y)
    assert str(s) == 'z = x[y]'
    s = Statement(UnconditionalJumpType, label='label1')
    assert str(s) == 'goto label1'
    s = Statement(ConditionalJumpType, operand=x, label='label1')
    assert str(s) == 'if x: goto label1'
    s = Statement(RelationalExpressionConditionalJumpType, operand_1=x, operand_2=y, 
                                                           operator=rel_op, label='label1')
    assert str(s) == 'if x < y: goto label1'
    s = Statement(InParameterType, param=x)
    assert str(s) == 'inparam x'
    s = Statement(OutParameterType, param=x)
    assert str(s) == 'outparam x'
    s = Statement(ProcedureCallType, 
                  inparams=[Statement(InParameterType, param=x), 
                            Statement(InParameterType, param=y)],
                  outparams=[Statement(OutParameterType, param=z)],
                  procedure=f)
    assert str(s) == 'inparam x\ninparam y\noutparam z\ncall f, 2, 1'
    s = Statement(ProcedureDefinitionType, 
                  inparams=[Statement(InParameterType, param=x), 
                            Statement(InParameterType, param=y)],
                  outparams=[Statement(OutParameterType, param=z)],
                  identifier=f,
                  statements=[
                              Statement(BinaryAssignmentType, result=z, operator=bin_op, 
                                                                        operand_1=x, operand_2=y),
                              Statement(UnaryAssignmentType, result=z, operator=unary_op, 
                                                                                    operand=x),
                              Statement(CopyType, result=z, operand=x)
                             ])
    assert str(s) == 'procedure f, 2, 1\ninparam x\ninparam y\nz = x + y\n' + \
                     'z = -x\nz = x\noutparam z\nendprocedure'