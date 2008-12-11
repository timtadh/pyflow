import ply.yacc as yacc
from lex import C_Lexer

def p_primary_expr(p):
    '''primary_expr : identifier
                    | CONSTANT
                    | STRING_LITERAL
                    | '(' expr ')' '''
    pass

def p_postfix_expr(p):
    '''postfix_expr : primary_expr
                    | postfix_expr '[' expr ']'
                    | postfix_expr '(' ')'
                    | postfix_expr '(' argument_expr_list ')'
                    | postfix_expr '.' identifier
                    | postfix_expr PTR_OP identifier
                    | postfix_expr INC_OP
                    | postfix_expr DEC_OP'''
    pass

def p_argument_expr_list(p):
    '''argument_expr_list : assignment_expr
                          | argument_expr_list ',' assignment_expr'''
    pass

def p_unary_expr(p):
    '''unary_expr : postfix_expr
                  | INC_OP unary_expr
                  | DEC_OP unary_expr
                  | unary_operator cast_expr
                  | SIZEOF unary_expr
                  | SIZEOF '(' type_name ')' '''
    pass

def p_unary_operator(p):
    '''unary_operator : '&'
                      | '*'
                      | '+'
                      | '-'
                      | '~'
                      | '!' '''
    pass

def p_cast_expr(p):
    '''cast_expr  : unary_expr
                  | '(' type_name ')' cast_expr'''
    pass

def p_multiplicative_expr(p):
    '''multiplicative_expr : cast_expr
                           | multiplicative_expr '*' cast_expr
                           | multiplicative_expr '/' cast_expr
                           | multiplicative_expr '%' cast_expr'''
    pass

def p_additive_expr(p):
    '''additive_expr : multiplicative_expr
                     | additive_expr '+' multiplicative_expr
                     | additive_expr '-' multiplicative_expr'''
    pass

def p_shift_expr(p):
    '''shift_expr : additive_expr
                  | shift_expr LEFT_OP additive_expr
                  | shift_expr RIGHT_OP additive_expr'''
    pass

def p_relational_expr(p):
    '''relational_expr : shift_expr
                       | relational_expr '<' shift_expr
                       | relational_expr '>' shift_expr
                       | relational_expr LE_OP shift_expr
                       | relational_expr GE_OP shift_expr'''
    pass

def p_equality_expr(p):
    '''equality_expr : relational_expr
                     | equality_expr EQ_OP relational_expr
                     | equality_expr NE_OP relational_expr'''
    pass

def p_and_expr(p):
    '''and_expr  : equality_expr
                 | and_expr '&' equality_expr'''
    pass

def p_exclusive_or_expr(p):
    '''exclusive_or_expr : and_expr
                         | exclusive_or_expr '^' and_expr'''
    pass

def p_inclusive_or_expr(p):
    '''inclusive_or_expr : exclusive_or_expr
                         | inclusive_or_expr '|' exclusive_or_expr'''
    pass

def p_logical_and_expr(p):
    '''logical_and_expr : inclusive_or_expr
                        | logical_and_expr AND_OP inclusive_or_expr'''
    pass

def p_logical_or_expr(p):
    '''logical_or_expr : logical_and_expr
                       | logical_or_expr OR_OP logical_and_expr'''
    pass

def p_conditional_expr(p):
    '''conditional_expr : logical_or_expr
                        | logical_or_expr '?' logical_or_expr ':' conditional_expr'''
    pass

def p_assignment_expr(p):
    '''assignment_expr : conditional_expr
                       | unary_expr assignment_operator assignment_expr'''
    pass

def p_assignment_operator(p):
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
    pass

def p_expr(p):
    '''expr : assignment_expr
            | expr ',' assignment_expr'''
    pass

def p_constant_expr(p):
    '''constant_expr : conditional_expr'''
    pass

def p_declaration(p):
    '''declaration : declaration_specifiers ''
                   | declaration_specifiers init_declarator_list ''  '''
    pass

def p_declaration_specifiers(p):
    '''declaration_specifiers : storage_class_specifier
                              | storage_class_specifier declaration_specifiers
                              | type_specifier
                              | type_specifier declaration_specifiers'''
    pass

def p_init_declarator_list(p):
    '''init_declarator_list : init_declarator
                            | init_declarator_list ',' init_declarator'''
    pass

def p_init_declarator(p):
    '''init_declarator : declarator
                       | declarator '=' initializer'''
    pass

def p_storage_class_specifier(p):
    '''storage_class_specifier : TYPEDEF
                               | EXTERN
                               | STATIC
                               | AUTO
                               | REGISTER'''
    pass

def p_type_specifier(p):
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
    pass

def p_struct_or_union_specifier(p):
    '''struct_or_union_specifier : struct_or_union identifier '{' struct_declaration_list '}'
                                 | struct_or_union '{' struct_declaration_list '}'
                                 | struct_or_union identifier'''
    pass

def p_struct_or_union(p):
    '''struct_or_union : STRUCT
                    | UNION'''
    pass

def p_struct_declaration_list(p):
    '''struct_declaration_list : struct_declaration
                            | struct_declaration_list struct_declaration'''
    pass

def p_struct_declaration(p):
    '''struct_declaration : type_specifier_list struct_declarator_list ''  '''
    pass

def p_struct_declarator_list(p):
    '''struct_declarator_list : struct_declarator
                              | struct_declarator_list ',' struct_declarator'''
    pass

def p_struct_declarator(p):
    '''struct_declarator : declarator
                         | ':' constant_expr
                         | declarator ':' constant_expr'''
    pass

def p_enum_specifier(p):
    '''enum_specifier : ENUM '{' enumerator_list '}'
                      | ENUM identifier '{' enumerator_list '}'
                      | ENUM identifier'''
    pass

def p_enumerator_list(p):
    '''enumerator_list : enumerator
                       | enumerator_list ',' enumerator''' 
    pass

def p_enumerator(p):
    '''enumerator : identifier
                  | identifier '=' constant_expr'''
    pass

def p_declarator(p):
    '''declarator : declarator2
                | pointer declarator2'''
    pass

def p_declarator2(p):
    '''declarator2 : identifier
                   | '(' declarator ')'
                   | declarator2 '[' ']'
                   | declarator2 '[' constant_expr ']'
                   | declarator2 '(' ')'
                   | declarator2 '(' parameter_type_list ')'
                   | declarator2 '(' parameter_identifier_list ')'  '''
    pass

def p_pointer(p):
    '''pointer : '*'
               | '*' type_specifier_list
               | '*' pointer
               | '*' type_specifier_list pointer'''  
    pass  

def p_type_specifier_list(p):
    '''type_specifier_list : type_specifier
                           | type_specifier_list type_specifier'''
    pass

def p_parameter_identifier_list(p):
    '''parameter_identifier_list : identifier_list
                                 | identifier_list ',' ELIPSIS'''
    pass

def p_identifier_list(p):
    '''identifier_list : identifier
                       | identifier_list ',' identifier'''
    pass

def p_parameter_type_list(p):
    '''parameter_type_list : parameter_list
                           | parameter_list ',' ELIPSIS'''
    pass

def p_parameter_list(p):
    '''parameter_list : parameter_declaration
                      | parameter_list ',' parameter_declaration'''
    pass

def p_parameter_declaration(p):
    '''parameter_declaration : type_specifier_list declarator
                             | type_name'''
    pass

def p_type_name(p):
    '''type_name : type_specifier_list
                 | type_specifier_list abstract_declarator'''
    pass

def p_abstract_declarator(p):
    '''abstract_declarator : pointer
                           | abstract_declarator2
                           | pointer abstract_declarator2'''
    pass

def p_abstract_declarator2(p):
    '''abstract_declarator2 : '(' abstract_declarator ')'
                            | '[' ']'
                            | '[' constant_expr ']'
                            | abstract_declarator2 '[' ']'
                            | abstract_declarator2 '[' constant_expr ']'
                            | '(' ')'
                            | '(' parameter_type_list ')'
                            | abstract_declarator2 '(' ')'
                            | abstract_declarator2 '(' parameter_type_list ')' '''
    pass

def p_initializer(p):
    '''initializer : assignment_expr
                   | '{' initializer_list '}'
                   | '{' initializer_list ',' '}' '''
    pass

def p_initializer_list(p):
    '''initializer_list : initializer
                        | initializer_list ',' initializer'''
    pass

def p_statement(p):
    '''statement : labeled_statement
                 | compound_statement
                 | expression_statement
                 | selection_statement
                 | iteration_statement
                 | jump_statement'''
    pass

def p_labeled_statement(p):
    '''labeled_statement : identifier ':' statement
                         | CASE constant_expr ':' statement
                         | DEFAULT ':' statement'''
    pass

def p_brackets(p):
    '''left_bracket : '{'
       right_bracket : '}' '''
    pass

def p_compound_statement(p):
    '''compound_statement : left_bracket right_bracket
                          | left_bracket statement_list right_bracket
                          | left_bracket declaration_list right_bracket
                          | left_bracket declaration_list statement_list right_bracket'''
    pass

def p_declaration_list(p):
    '''declaration_list : declaration
                        | declaration_list declaration'''
    pass

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    pass

def p_expr_statement(p):
    '''expression_statement : ';'
                            | expr ';' '''
    pass

def p_selection_statement(p):
    '''selection_statement : IF '(' expr ')' statement
                           | IF '(' expr ')' statement ELSE statement
                           | SWITCH '(' expr ')' statement'''
    pass

def p_iteration_statement(p):
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
    pass

def p_jump_statement(p):
    '''jump_statement : GOTO identifier ';'
                      | CONTINUE ';'
                      | BREAK ';'
                      | RETURN ';'
                      | RETURN expr ';' '''
    pass

def p_code(p):
    '''code : file'''
    pass

def p_file(p):
    '''file : external_definition
            | file external_definition '''
    pass

def p_external_definition(p):
    '''external_definition : function_definition
                           | declaration'''
    pass

def p_function_definition(p):
    '''function_definition : declarator function_body
                           | declaration_specifiers declarator function_body'''
    pass

def p_function_body(p):
    '''function_body : compound_statement
                     | declaration_list compound_statement
    '''
    pass

def p_identifier(p):
    '''identifier : IDENTIFIER'''
    print p
    p[0] = p[1]

def p_error(p):
    print p

c_lexer = C_Lexer()
c_lexer.build()
lexer = c_lexer.lexer
tokens = c_lexer.tokens
literals = c_lexer.literals

start = 'code'
parser = yacc.yacc()
parser.parse('int i = 0;', lexer=lexer)