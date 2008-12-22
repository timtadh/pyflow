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
    '''Empty base class for three address statement types'''
    
class BinaryAssignmentType(StatementType):
    '''r = o1 bin_op o2'''
    result = 'The c_types.Identifier where the result of the operation goes'
    operator = 'An opertor from BinaryOperators'
    operand_1 = 'A constant or c_types.Identifier'
    operand_2 = 'A constant or c_types.Identifier'

class UnaryAssignmentType(StatementType):
    '''r = unary_op o'''
    result = 'The c_types.Identifier where the result of the operation goes'
    operator = 'An opertor from BinaryOperators'
    operand = 'A constant or c_types.Identifier'

class CopyType(StatementType):
    '''r = o'''
    result = 'The c_types.Identifier where the result of the operation goes'
    operand = 'A constant or c_types.Identifier'

class IndexedCopyType(StatementType):
    '''r = o[i]'''
    result = 'The c_types.Identifier where the result of the operation goes'
    operand = 'A c_types.Identifier the type must be c_types.VectorType'
    index = 'The index of the array beign accessed'

class UnconditionalJumpType(StatementType):
    '''goto label'''
    label = 'The label where the jump is going to'

class ConditionalJump(StatementType):
    '''if x: goto label'''
    operand = '''A constant or c_types.Identifier, note this will evaluate for false if all zero 
                 true otherwise'''
    label = 'Target of the jump if operand evaluates to true'

class RelationalExpressionConditionalJump(StatementType):
    '''if x rel_op y: goto label'''
    operator = 'An opertor from BinaryOperators restrict yourself to the realtional'
    operand_1 = 'A constant or c_types.Identifier'
    operand_2 = 'A constant or c_types.Identifier'
    label = 'Target of the jump if operand evaluates to true'

class ParameterType(StatementType):
    '''param x'''
    parameter = 'A constant or c_types.Identifier'

class ProcedureCallType(StatementType):
    '''param x1
       param x2
       ...
       param xn
       call procedure, n'''
    parameter_list = 'A list of parameters to be passed into the parameter'
    procedure = 'The procedure being called'