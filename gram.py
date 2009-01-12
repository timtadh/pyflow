'''Defines the grammar and parser for the compiler. Equivalent of yacc.y'''
import ply.yacc as yacc
import sys
import c_types, ircode, irgenerator
from scan import C_Lexer
from ast import *

class C_Parser(object):
    
    def __init__(self, symbol_table, typedef_table):
        self.start = 'code'
        self.c_lexer = C_Lexer(symbol_table, typedef_table)
        self.c_lexer.build()
        self.lexer = self.c_lexer.lexer
        self.tokens = self.c_lexer.tokens
        self.literals = self.c_lexer.literals
        self.symbol_table = symbol_table
        self.typedef_table = typedef_table
        self.irgen = irgenerator.IRGenerator(self.symbol_table, self.typedef_table)

    def p_primary_expr(self, p):
        '''primary_expr : identifier
                        | CONSTANT
                        | STRING_LITERAL
                        | '(' expr ')' '''
        p[0] = Node(p, 'primary_expr')
        p[0].attrs.code = []
        if p[1].__class__ == Node and p[1].symbol.symbol == 'identifier':
            p[0].attrs.identifier = self.symbol_table.find_symbol(p[1].attrs.identifier)
        if p[1].__class__ == c_types.Constant:
            temp, statements = self.irgen.load_constant(p[1])
            p[0].attrs.code += statements
            p[0].attrs.identifier = temp
    
    def p_postfix_expr(self, p):
        '''postfix_expr : primary_expr
                        | postfix_expr '[' expr ']'
                        | postfix_expr '(' ')'
                        | postfix_expr '(' argument_expr_list ')'
                        | postfix_expr '.' identifier
                        | postfix_expr PTR_OP identifier
                        | postfix_expr INC_OP
                        | postfix_expr DEC_OP'''                    #NOT FINISHED
        p[0] = Node(p, 'postfix_expr')
        p[0].attrs.code = []
        p[0].attrs.identifier = None
        if p[1].__class__ == Node and p[1].symbol.symbol == 'primary_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.identifier = p[1].attrs.identifier
    
    def p_argument_expr_list(self, p):
        '''argument_expr_list : assignment_expr
                            | argument_expr_list ',' assignment_expr'''
        p[0] = Node(p, 'argument_expr_list')
    
    def p_unary_expr(self, p):
        '''unary_expr : postfix_expr
                    | INC_OP unary_expr
                    | DEC_OP unary_expr
                    | unary_operator cast_expr
                    | SIZEOF unary_expr
                    | SIZEOF '(' type_name ')' '''                   #NOT FINISHED
        p[0] = Node(p, 'unary_expr')
        p[0].attrs.code = []
        p[0].attrs.identifier = None
        if p[1].__class__ == Node and p[1].symbol.symbol == 'postfix_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.identifier = p[1].attrs.identifier
        elif p[1].__class__ == Node and p[1].symbol.symbol == 'unary_operator':
            p[0].attrs.code += p[2].attrs.code
            temp, statements = self.irgen.unary_operation(p[1].attrs.operator, p[2].attrs.identifier)
            p[0].attrs.code += statements
            p[0].attrs.identifier = temp
    
    def p_unary_operator(self, p):
        '''unary_operator : '&'
                        | '*'
                        | '+'
                        | '-'
                        | '~'
                        | '!' '''
        p[0] = Node(p, 'unary_operator')
        p[0].attrs.operator = p[1]
        
    
    def p_cast_expr(self, p):
        '''cast_expr  : unary_expr
                    | '(' type_name ')' cast_expr'''                #NOT FINISHED
        p[0] = Node(p, 'cast_expr')
        p[0].attrs.code = []
        p[0].attrs.identifier = None
        if p[1].__class__ == Node and p[1].symbol.symbol == 'unary_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.identifier = p[1].attrs.identifier
        
    
    def p_multiplicative_expr(self, p):
        '''multiplicative_expr : cast_expr
                            | multiplicative_expr '*' cast_expr
                            | multiplicative_expr '/' cast_expr
                            | multiplicative_expr '%' cast_expr'''
        p[0] = Node(p, 'multiplicative_expr')
        p[0].attrs.code = []
        p[0].attrs.identifier = None
        if p[1].__class__ == Node and p[1].symbol.symbol == 'cast_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.identifier = p[1].attrs.identifier
        elif p[1].__class__ == Node and p[1].symbol.symbol == 'multiplicative_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.code += p[3].attrs.code
            temp, statements = self.irgen.binary_operation(p[2], p[1].attrs.identifier, 
                                                                              p[3].attrs.identifier)
            p[0].attrs.code += statements
            print temp
            p[0].attrs.identifier = temp
    
    def p_additive_expr(self, p):
        '''additive_expr : multiplicative_expr
                        | additive_expr '+' multiplicative_expr
                        | additive_expr '-' multiplicative_expr'''
        p[0] = Node(p, 'additive_expr')
        p[0].attrs.code = []
        p[0].attrs.identifier = None
        if p[1].__class__ == Node and p[1].symbol.symbol == 'multiplicative_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.identifier = p[1].attrs.identifier
        elif p[1].__class__ == Node and p[1].symbol.symbol == 'additive_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.code += p[3].attrs.code
            temp, statements = self.irgen.binary_operation(p[2], p[1].attrs.identifier, 
                                                                              p[3].attrs.identifier)
            p[0].attrs.code += statements
            print temp
            p[0].attrs.identifier = temp
    
    def p_shift_expr(self, p):
        '''shift_expr : additive_expr
                    | shift_expr LEFT_OP additive_expr
                    | shift_expr RIGHT_OP additive_expr'''
        p[0] = Node(p, 'shift_expr')
        p[0].attrs.code = []
        p[0].attrs.identifier = None
        if p[1].__class__ == Node and p[1].symbol.symbol == 'additive_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.identifier = p[1].attrs.identifier
        elif p[1].__class__ == Node and p[1].symbol.symbol == 'shift_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.code += p[3].attrs.code
            temp, statements = self.irgen.binary_operation(p[2], p[1].attrs.identifier, 
                                                                              p[3].attrs.identifier)
            p[0].attrs.code += statements
            print temp
            p[0].attrs.identifier = temp
    
    def p_relational_expr(self, p):
        '''relational_expr : shift_expr
                        | relational_expr '<' shift_expr
                        | relational_expr '>' shift_expr
                        | relational_expr LE_OP shift_expr
                        | relational_expr GE_OP shift_expr'''
        p[0] = Node(p, 'relational_expr')
        p[0].attrs.code = []
        p[0].attrs.identifier = None
        if p[1].__class__ == Node and p[1].symbol.symbol == 'shift_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.identifier = p[1].attrs.identifier
        elif p[1].__class__ == Node and p[1].symbol.symbol == 'relational_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.code += p[3].attrs.code
            temp, statements = self.irgen.binary_operation(p[2], p[1].attrs.identifier, 
                                                                              p[3].attrs.identifier)
            p[0].attrs.code += statements
            print temp
            p[0].attrs.identifier = temp
    
    def p_equality_expr(self, p):
        '''equality_expr : relational_expr
                        | equality_expr EQ_OP relational_expr
                        | equality_expr NE_OP relational_expr'''
        p[0] = Node(p, 'equality_expr')
        p[0].attrs.code = []
        p[0].attrs.identifier = None
        if p[1].__class__ == Node and p[1].symbol.symbol == 'relational_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.identifier = p[1].attrs.identifier
        elif p[1].__class__ == Node and p[1].symbol.symbol == 'equality_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.code += p[3].attrs.code
            temp, statements = self.irgen.binary_operation(p[2], p[1].attrs.identifier, 
                                                                              p[3].attrs.identifier)
            p[0].attrs.code += statements
            print temp
            p[0].attrs.identifier = temp
    
    def p_and_expr(self, p):
        '''and_expr  : equality_expr
                    | and_expr '&' equality_expr'''
        p[0] = Node(p, 'and_expr')
        p[0].attrs.code = []
        p[0].attrs.identifier = None
        if p[1].__class__ == Node and p[1].symbol.symbol == 'equality_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.identifier = p[1].attrs.identifier
        elif p[1].__class__ == Node and p[1].symbol.symbol == 'and_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.code += p[3].attrs.code
            temp, statements = self.irgen.binary_operation(p[2], p[1].attrs.identifier, 
                                                                              p[3].attrs.identifier)
            p[0].attrs.code += statements
            print temp
            p[0].attrs.identifier = temp
    
    def p_exclusive_or_expr(self, p):
        '''exclusive_or_expr : and_expr
                            | exclusive_or_expr '^' and_expr'''
        p[0] = Node(p, 'exclusive_or_expr')
        p[0].attrs.code = []
        p[0].attrs.identifier = None
        if p[1].__class__ == Node and p[1].symbol.symbol == 'and_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.identifier = p[1].attrs.identifier
        elif p[1].__class__ == Node and p[1].symbol.symbol == 'exclusive_or_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.code += p[3].attrs.code
            temp, statements = self.irgen.binary_operation(p[2], p[1].attrs.identifier, 
                                                                              p[3].attrs.identifier)
            p[0].attrs.code += statements
            print temp
            p[0].attrs.identifier = temp
    
    def p_inclusive_or_expr(self, p):
        '''inclusive_or_expr : exclusive_or_expr
                            | inclusive_or_expr '|' exclusive_or_expr'''
        p[0] = Node(p, 'inclusive_or_expr')
        p[0].attrs.code = []
        p[0].attrs.identifier = None
        if p[1].__class__ == Node and p[1].symbol.symbol == 'exclusive_or_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.identifier = p[1].attrs.identifier
        elif p[1].__class__ == Node and p[1].symbol.symbol == 'inclusive_or_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.code += p[3].attrs.code
            temp, statements = self.irgen.binary_operation(p[2], p[1].attrs.identifier, 
                                                                              p[3].attrs.identifier)
            p[0].attrs.code += statements
            print temp
            p[0].attrs.identifier = temp
    
    def p_logical_and_expr(self, p):
        '''logical_and_expr : inclusive_or_expr
                            | logical_and_expr AND_OP inclusive_or_expr'''
        p[0] = Node(p, 'logical_and_expr')
        p[0].attrs.code = []
        p[0].attrs.identifier = None
        if p[1].__class__ == Node and p[1].symbol.symbol == 'inclusive_or_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.identifier = p[1].attrs.identifier
        elif p[1].__class__ == Node and p[1].symbol.symbol == 'logical_and_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.code += p[3].attrs.code
            temp, statements = self.irgen.binary_operation(p[2], p[1].attrs.identifier, 
                                                                              p[3].attrs.identifier)
            p[0].attrs.code += statements
            print temp
            p[0].attrs.identifier = temp
    
    def p_logical_or_expr(self, p):
        '''logical_or_expr : logical_and_expr
                        | logical_or_expr OR_OP logical_and_expr'''
        p[0] = Node(p, 'logical_or_expr')
        p[0].attrs.code = []
        p[0].attrs.identifier = None
        if p[1].__class__ == Node and p[1].symbol.symbol == 'logical_and_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.identifier = p[1].attrs.identifier
        elif p[1].__class__ == Node and p[1].symbol.symbol == 'logical_or_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.code += p[3].attrs.code
            temp, statements = self.irgen.binary_operation(p[2], p[1].attrs.identifier, 
                                                                              p[3].attrs.identifier)
            p[0].attrs.code += statements
            print temp
            p[0].attrs.identifier = temp
    
    def p_conditional_expr(self, p):
        '''conditional_expr : logical_or_expr
                            | logical_or_expr '?' logical_or_expr ':' conditional_expr'''          #NOT FINISHED
        p[0] = Node(p, 'conditional_expr')
        p[0].attrs.code = []
        p[0].attrs.identifier = None
        if p[1].__class__ == Node and p[1].symbol.symbol == 'logical_or_expr' and len(p) == 2:
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.identifier = p[1].attrs.identifier
    
    def p_assignment_expr(self, p):
        '''assignment_expr : conditional_expr
                        | unary_expr assignment_operator assignment_expr'''
        p[0] = Node(p, 'assignment_expr')
        p[0].attrs.code = []
        p[0].attrs.identifier = None
        if p[1].__class__ == Node and p[1].symbol.symbol == 'conditional_expr':
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.identifier = p[1].attrs.identifier
        else:
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.code += p[3].attrs.code
            if p[2].attrs.operator == '=':
                temp, statements = self.irgen.copy(p[3].attrs.identifier, p[1].attrs.identifier)
                p[0].attrs.code += statements
                p[0].attrs.identifier = temp
            else:
                temp, statements = self.irgen.binary_operation(p[2].attrs.operator[0], p[1].attrs.identifier, 
                                                                              p[3].attrs.identifier)
                p[0].attrs.code += statements
                temp, statements = self.irgen.copy(temp, p[1].attrs.identifier)
                p[0].attrs.code += statements
                p[0].attrs.identifier = temp
    
    def p_assignment_operator(self, p):
        '''assignment_operator : '='
                            | MUL_ASSIGN
                            | DIV_ASSIGN
                            | MOD_ASSIGN
                            | ADD_ASSIGN
                            | SUB_ASSIGN
                            | LEFT_ASSIGN
                            | RIGHT_ASSIGN
                            | AND_ASSIGN
                            | XOR_ASSIGN
                            | OR_ASSIGN'''
        p[0] = Node(p, 'assignment_operator')
        p[0].attrs.operator = p[1]
    
    def p_expr(self, p):
        '''expr : assignment_expr
                | expr ',' assignment_expr'''
        p[0] = Node(p, 'expr')
        p[0].attrs.code = []
        p[0].attrs.identifier = None
        if p[1].__class__ == Node and p[1].symbol.symbol == 'assignment_expr':
            p[0].attrs.code += p[1].attrs.code
        else:
            p[0].attrs.code += p[1].attrs.code
            p[0].attrs.code += p[3].attrs.code
            
    
    def p_constant_expr(self, p):
        '''constant_expr : conditional_expr'''
        p[0] = Node(p, 'constant_expr')
    
    def p_declaration(self, p):
        '''declaration : declaration_specifiers ';'
                    | declaration_specifiers init_declarator_list ';'  '''
        p[0] = Node(p, 'declaration')
    
    def p_declaration_specifiers(self, p):
        '''declaration_specifiers : storage_class_specifier
                                | storage_class_specifier declaration_specifiers
                                | type_specifier
                                | type_specifier declaration_specifiers'''
        if p[1].symbol.symbol == 'type_specifier':
            if len(p) == 3: 
                type_name = p[1].attrs.type.type_name + ' ' + p[2].attrs.type.type_name
            else:
                type_name = p[1].attrs.type.type_name
        else: type_name = None
        p[0] = Node(p, 'declaration_specifiers')
        p[0].attrs.type = self.typedef_table.find_type(type_name)
    
    def p_init_declarator_list(self, p):
        '''init_declarator_list : init_declarator
                                | init_declarator_list ',' init_declarator'''
        p[0] = Node(p, 'init_declarator_list')
        p[0].attrs.type = p[-1].attrs.type
    
    def p_init_declarator(self, p):
        '''init_declarator : declarator
                           | declarator '=' initializer'''
        p[0] = Node(p, 'init_declarator')
        i = -1
        while p[i].__class__ != Node: i -= 1
        type = p[i].attrs.type
        #print p[i]
        if len(p) == 4: value = p[3].attrs.value
        else: value = None
        identifier = p[1].attrs.identifier
        identifier.type = type
        identifier.value = value
        p[0].attrs.identifier = identifier
    
    def p_storage_class_specifier(self, p):
        '''storage_class_specifier : TYPEDEF
                                | EXTERN
                                | STATIC
                                | AUTO
                                | REGISTER'''
        p[0] = Node(p, 'storage_class_specifier')
    
    def p_type_specifier(self, p):
        '''type_specifier : CHAR
                          | SHORT
                          | INT
                          | LONG
                          | SIGNED
                          | UNSIGNED
                          | FLOAT
                          | DOUBLE
                          | CONST
                          | VOLATILE
                          | VOID
                          | struct_or_union_specifier
                          | enum_specifier
                          | TYPE_NAME'''
        type = self.typedef_table.find_type(p[1])
        if type: p[1] = type
        p[0] = Node(p, 'type_specifier')
        p[0].attrs.type = type
        for child in p[0].children: child.attrs.type = type
    
    def p_struct_or_union_specifier(self, p):
        '''struct_or_union_specifier : struct_or_union identifier '{' struct_declaration_list '}'
                                    | struct_or_union '{' struct_declaration_list '}'
                                    | struct_or_union identifier'''
        p[0] = Node(p, 'struct_or_union_specifier')
    
    def p_struct_or_union(self, p):
        '''struct_or_union : STRUCT
                        | UNION'''
        p[0] = Node(p, 'struct_or_union')
    
    def p_struct_declaration_list(self, p):
        '''struct_declaration_list : struct_declaration
                                | struct_declaration_list struct_declaration'''
        p[0] = Node(p, 'struct_declaration_list')
    
    def p_struct_declaration(self, p):
        '''struct_declaration : type_specifier_list struct_declarator_list ';'  '''
        p[0] = Node(p, 'struct_declaration')
    
    def p_struct_declarator_list(self, p):
        '''struct_declarator_list : struct_declarator
                                | struct_declarator_list ',' struct_declarator'''
        p[0] = Node(p, 'struct_declarator_list')
    
    def p_struct_declarator(self, p):
        '''struct_declarator : declarator
                            | ':' constant_expr
                            | declarator ':' constant_expr'''
        p[0] = Node(p, 'struct_declarator')
    
    def p_enum_specifier(self, p):
        '''enum_specifier : ENUM '{' enumerator_list '}'
                        | ENUM identifier '{' enumerator_list '}'
                        | ENUM identifier'''
        p[0] = Node(p, 'enum_specifier')
    
    def p_enumerator_list(self, p):
        '''enumerator_list : enumerator
                        | enumerator_list ',' enumerator''' 
        p[0] = Node(p, 'enumerator_list')
    
    def p_enumerator(self, p):
        '''enumerator : identifier
                    | identifier '=' constant_expr'''
        p[0] = Node(p, 'enumerator')
    
    def p_declarator(self, p):
        '''declarator : declarator2
                    | pointer declarator2'''
        p[0] = Node(p, 'declarator')
        if len(p) == 2: p[0].attrs.identifier = p[1].attrs.identifier
        else:
            type = p[2].attrs.identifier.type
            pointer = c_types.PointerType(self.typedef_table.find_type('int'), type)
            p[0].attrs.identifier = p[2].attrs.identifier
            p[0].attrs.identifier.type = pointer
    
    def p_declarator2(self, p):
        '''declarator2 : identifier
                    | '(' declarator ')'
                    | declarator2 '[' ']'
                    | declarator2 '[' constant_expr ']'
                    | declarator2 '(' ')'
                    | declarator2 '(' parameter_type_list ')'
                    | declarator2 '(' parameter_identifier_list ')'  '''
        if p[1].__class__ == Node:
            if p[1].symbol.symbol == 'identifier':
                identifier = c_types.Identifier(p[1].attrs.identifier)
                self.symbol_table.create_symbol(identifier)
            else:
                identifier = p[1].attrs.identifier
        else:
            identifier = p[2].attrs.identifier
        p[0] = Node(p, 'declarator2')
        p[0].attrs.identifier = identifier
    
    def p_pointer(self, p):
        '''pointer : '*'
                | '*' type_specifier_list
                | '*' pointer
                | '*' type_specifier_list pointer'''  
        p[0] = Node(p, 'pointer')  
    
    def p_type_specifier_list(self, p):
        '''type_specifier_list : type_specifier
                            | type_specifier_list type_specifier'''
        p[0] = Node(p, 'type_specifier_list')
    
    def p_parameter_identifier_list(self, p):
        '''parameter_identifier_list : identifier_list
                                    | identifier_list ',' ELIPSIS'''
        p[0] = Node(p, 'parameter_identifier_list')
    
    def p_identifier_list(self, p):
        '''identifier_list : identifier
                        | identifier_list ',' identifier'''
        p[0] = Node(p, 'identifier_list')
    
    def p_parameter_type_list(self, p):
        '''parameter_type_list : parameter_list
                            | parameter_list ',' ELIPSIS'''
        p[0] = Node(p, 'parameter_type_list')
    
    def p_parameter_list(self, p):
        '''parameter_list : parameter_declaration
                        | parameter_list ',' parameter_declaration'''
        p[0] = Node(p, 'parameter_list')
    
    def p_parameter_declaration(self, p):
        '''parameter_declaration : type_specifier_list declarator
                                | type_name'''
        p[0] = Node(p, 'parameter_declaration')
    
    def p_type_name(self, p):
        '''type_name : type_specifier_list
                    | type_specifier_list abstract_declarator'''
        p[0] = Node(p, 'type_name')
    
    def p_abstract_declarator(self, p):
        '''abstract_declarator : pointer
                            | abstract_declarator2
                            | pointer abstract_declarator2'''
        p[0] = Node(p, 'abstract_declarator')
    
    def p_abstract_declarator2(self, p):
        '''abstract_declarator2 : '(' abstract_declarator ')'
                                | '[' ']'
                                | '[' constant_expr ']'
                                | abstract_declarator2 '[' ']'
                                | abstract_declarator2 '[' constant_expr ']'
                                | '(' ')'
                                | '(' parameter_type_list ')'
                                | abstract_declarator2 '(' ')'
                                | abstract_declarator2 '(' parameter_type_list ')' '''
        p[0] = Node(p, 'abstract_declarator2')
    
    def p_initializer(self, p):
        '''initializer : assignment_expr
                    | '{' initializer_list '}'
                    | '{' initializer_list ',' '}' '''
        p[0] = Node(p, 'initializer')
    
    def p_initializer_list(self, p):
        '''initializer_list : initializer
                            | initializer_list ',' initializer'''
        p[0] = Node(p, 'initializer_list')
    
    def p_statement(self, p):
        '''statement : labeled_statement
                    | compound_statement
                    | expression_statement
                    | selection_statement
                    | iteration_statement
                    | jump_statement'''
        p[0] = Node(p, 'statement')
    
    def p_labeled_statement(self, p):
        '''labeled_statement : identifier ':' statement
                            | CASE constant_expr ':' statement
                            | DEFAULT ':' statement'''
        p[0] = Node(p, 'labeled_statement')
    
    def p_left_bracket(self, p):
        '''left_bracket : '{' '''
        p[0] = Node(p, 'left_bracket')
        #print self.symbol_table
        self.symbol_table.push_level()
        
    def p_right_bracket(self, p):
        '''right_bracket : '}' '''
        p[0] = Node(p, 'right_bracket')
        self.symbol_table.pop_level()
    
    def p_compound_statement(self, p):
        '''compound_statement : left_bracket right_bracket
                            | left_bracket statement_list right_bracket
                            | left_bracket declaration_list right_bracket
                            | left_bracket declaration_list statement_list right_bracket'''
        p[0] = Node(p, 'compound_statement')
    
    def p_declaration_list(self, p):
        '''declaration_list : declaration
                            | declaration_list declaration'''
        p[0] = Node(p, 'declaration_list')
    
    def p_statement_list(self, p):
        '''statement_list : statement
                          | statement_list statement'''
        p[0] = Node(p, 'statement_list')
    
    def p_expr_statement(self, p):
        '''expression_statement : ';'
                                | expr ';' '''
        p[0] = Node(p, 'expression_statement')
        p[0].attrs.code = []
        if p[1].__class__ == Node and p[1].symbol.symbol == 'expr':
            p[0].attrs.code += p[1].attrs.code
    
    def p_selection_statement(self, p):
        '''selection_statement : IF '(' expr ')' statement
                               | IF '(' expr ')' statement ELSE statement
                               | SWITCH '(' expr ')' statement'''
        p[0] = Node(p, 'selection_statement')
    
    def p_iteration_statement(self, p):
        '''iteration_statement : WHILE '(' expr ')' statement
                               | DO statement WHILE '(' expr ')' ';'
                               | FOR '(' ';' ';' ')' statement
                               | FOR '(' ';' ';' expr ')' statement
                               | FOR '(' ';' expr ';' ')' statement
                               | FOR '(' ';' expr ';' expr ')' statement
                               | FOR '(' expr ';' ';' ')' statement
                               | FOR '(' expr ';' ';' expr ')' statement
                               | FOR '(' expr ';' expr ';' ')' statement
                               | FOR '(' expr ';' expr ';' expr ')' statement'''
        p[0] = Node(p, 'iteration_statement')
    
    def p_jump_statement(self, p):
        '''jump_statement : GOTO identifier ';'
                          | CONTINUE ';'
                          | BREAK ';'
                          | RETURN ';'
                          | RETURN expr ';' '''
        p[0] = Node(p, 'jump_statement')
    
    def p_code(self, p):
        '''code : file'''
        p[0] = Node(p, 'code')
    
    def p_file(self, p):
        '''file : external_definition
                | file external_definition '''
        p[0] = Node(p, 'file')
    
    def p_external_definition(self, p):
        '''external_definition : function_definition
                               | declaration'''
        p[0] = Node(p, 'external_definition')
    
    def p_function_definition(self, p):
        '''function_definition : declarator function_body
                               | declaration_specifiers declarator function_body'''
        if p[1].__class__ == Node and p[1].symbol.symbol == 'declaration_specifiers':
            return_type = p[1].attrs.type
            identifier = p[2].attrs.identifier
        else:
            return_type = self.typedef_table.find_type('int')
            identifier = p[1].attrs.identifier
        identifier.type = c_types.FunctionType(identifier.name, return_type)
        p[0] = Node(p, 'function_definition')
        p[0].attrs.identifier = identifier
    
    def p_function_body(self, p):
        '''function_body : compound_statement
                         | declaration_list compound_statement
        '''
        p[0] = Node(p, 'function_body')
    
    def p_identifier(self, p):
        '''identifier : IDENTIFIER'''
        p[0] = Node(p, 'identifier')
        p[0].attrs.identifier = p[1]
    
    def p_error(self, p):
        sys.stderr.write('ERROR' + str(p))
    
    def build(self, **kwargs):
         self.parser = yacc.yacc(module=self, **kwargs)
    
    def parse(self, text):
        return self.parser.parse(input=text, lexer=self.lexer, debug=0)


if __name__ == "__main__":
    c_parser = C_Parser()
    c_parser.build()
    f = open('test3.c', 'r')
    data = f.read()
    f.close()
    print c_parser.parse(data).print_out()