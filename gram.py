import ply.yacc as yacc
import sys
from scan import C_Lexer

class Node(object):
    
    def __init__(self, children=[], symbol=''):
        self.children = children
        for index,child in enumerate(self.children):
            if child.__class__ != Node:
                self.children[index] = Node(symbol='"'+str(child)+'"')
                self.children[index].graph_color = "#0000aa"
        self.symbol = symbol
    
    def traverse(self, node, i=0):
        s = ' '*i + str(node) + '\n'
        if 'children' not in dir(node): return s
        for child in node.children:
            s += self.traverse(child, i+1)
        return s
    
    def print_out(self):
        return str(self.traverse(self))
    
    def __str__(self):
        return str(self.symbol)

class C_Parser(object):
    
    def __init__(self):
        self.start = 'code'
        self.c_lexer = C_Lexer()
        self.c_lexer.build()
        self.lexer = self.c_lexer.lexer
        self.tokens = self.c_lexer.tokens
        self.literals = self.c_lexer.literals

    def p_primary_expr(self, p):
        '''primary_expr : identifier
                        | CONSTANT
                        | STRING_LITERAL
                        | '(' expr ')' '''
        p[0] = Node(p[1:], 'primary_expr')
    
    def p_postfix_expr(self, p):
        '''postfix_expr : primary_expr
                        | postfix_expr '[' expr ']'
                        | postfix_expr '(' ')'
                        | postfix_expr '(' argument_expr_list ')'
                        | postfix_expr '.' identifier
                        | postfix_expr PTR_OP identifier
                        | postfix_expr INC_OP
                        | postfix_expr DEC_OP'''
        p[0] = Node(p[1:], 'postfix_expr')
    
    def p_argument_expr_list(self, p):
        '''argument_expr_list : assignment_expr
                            | argument_expr_list ',' assignment_expr'''
        p[0] = Node(p[1:], 'argument_expr_list')
    
    def p_unary_expr(self, p):
        '''unary_expr : postfix_expr
                    | INC_OP unary_expr
                    | DEC_OP unary_expr
                    | unary_operator cast_expr
                    | SIZEOF unary_expr
                    | SIZEOF '(' type_name ')' '''
        p[0] = Node(p[1:], 'unary_expr')
    
    def p_unary_operator(self, p):
        '''unary_operator : '&'
                        | '*'
                        | '+'
                        | '-'
                        | '~'
                        | '!' '''
        p[0] = Node(p[1:], 'unary_operator')
    
    def p_cast_expr(self, p):
        '''cast_expr  : unary_expr
                    | '(' type_name ')' cast_expr'''
        p[0] = Node(p[1:], 'cast_expr')
    
    def p_multiplicative_expr(self, p):
        '''multiplicative_expr : cast_expr
                            | multiplicative_expr '*' cast_expr
                            | multiplicative_expr '/' cast_expr
                            | multiplicative_expr '%' cast_expr'''
        p[0] = Node(p[1:], 'multiplicative_expr')
    
    def p_additive_expr(self, p):
        '''additive_expr : multiplicative_expr
                        | additive_expr '+' multiplicative_expr
                        | additive_expr '-' multiplicative_expr'''
        p[0] = Node(p[1:], 'additive_expr')
    
    def p_shift_expr(self, p):
        '''shift_expr : additive_expr
                    | shift_expr LEFT_OP additive_expr
                    | shift_expr RIGHT_OP additive_expr'''
        p[0] = Node(p[1:], 'shift_expr')
    
    def p_relational_expr(self, p):
        '''relational_expr : shift_expr
                        | relational_expr '<' shift_expr
                        | relational_expr '>' shift_expr
                        | relational_expr LE_OP shift_expr
                        | relational_expr GE_OP shift_expr'''
        p[0] = Node(p[1:], 'relational_expr')
    
    def p_equality_expr(self, p):
        '''equality_expr : relational_expr
                        | equality_expr EQ_OP relational_expr
                        | equality_expr NE_OP relational_expr'''
        p[0] = Node(p[1:], 'equality_expr')
    
    def p_and_expr(self, p):
        '''and_expr  : equality_expr
                    | and_expr '&' equality_expr'''
        p[0] = Node(p[1:], 'and_expr')
    
    def p_exclusive_or_expr(self, p):
        '''exclusive_or_expr : and_expr
                            | exclusive_or_expr '^' and_expr'''
        p[0] = Node(p[1:], 'exclusive_or_expr')
    
    def p_inclusive_or_expr(self, p):
        '''inclusive_or_expr : exclusive_or_expr
                            | inclusive_or_expr '|' exclusive_or_expr'''
        p[0] = Node(p[1:], 'inclusive_or_expr')
    
    def p_logical_and_expr(self, p):
        '''logical_and_expr : inclusive_or_expr
                            | logical_and_expr AND_OP inclusive_or_expr'''
        p[0] = Node(p[1:], 'logical_and_expr')
    
    def p_logical_or_expr(self, p):
        '''logical_or_expr : logical_and_expr
                        | logical_or_expr OR_OP logical_and_expr'''
        p[0] = Node(p[1:], 'logical_or_expr')
    
    def p_conditional_expr(self, p):
        '''conditional_expr : logical_or_expr
                            | logical_or_expr '?' logical_or_expr ':' conditional_expr'''
        p[0] = Node(p[1:], 'conditional_expr')
    
    def p_assignment_expr(self, p):
        '''assignment_expr : conditional_expr
                        | unary_expr assignment_operator assignment_expr'''
        p[0] = Node(p[1:], 'assignment_expr')
    
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
        p[0] = Node(p[1:], 'assignment_operator')
    
    def p_expr(self, p):
        '''expr : assignment_expr
                | expr ',' assignment_expr'''
        p[0] = Node(p[1:], 'expr')
    
    def p_constant_expr(self, p):
        '''constant_expr : conditional_expr'''
        p[0] = Node(p[1:], 'constant_expr')
    
    def p_declaration(self, p):
        '''declaration : declaration_specifiers ';'
                    | declaration_specifiers init_declarator_list ';'  '''
        p[0] = Node(p[1:], 'declaration')
    
    def p_declaration_specifiers(self, p):
        '''declaration_specifiers : storage_class_specifier
                                | storage_class_specifier declaration_specifiers
                                | type_specifier
                                | type_specifier declaration_specifiers'''
        p[0] = Node(p[1:], 'declaration_specifiers')
    
    def p_init_declarator_list(self, p):
        '''init_declarator_list : init_declarator
                                | init_declarator_list ',' init_declarator'''
        p[0] = Node(p[1:], 'init_declarator_list')
    
    def p_init_declarator(self, p):
        '''init_declarator : declarator
                        | declarator '=' initializer'''
        p[0] = Node(p[1:], 'init_declarator')
    
    def p_storage_class_specifier(self, p):
        '''storage_class_specifier : TYPEDEF
                                | EXTERN
                                | STATIC
                                | AUTO
                                | REGISTER'''
        p[0] = Node(p[1:], 'storage_class_specifier')
    
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
        p[0] = Node(p[1:], 'type_specifier')
    
    def p_struct_or_union_specifier(self, p):
        '''struct_or_union_specifier : struct_or_union identifier '{' struct_declaration_list '}'
                                    | struct_or_union '{' struct_declaration_list '}'
                                    | struct_or_union identifier'''
        p[0] = Node(p[1:], 'struct_or_union_specifier')
    
    def p_struct_or_union(self, p):
        '''struct_or_union : STRUCT
                        | UNION'''
        p[0] = Node(p[1:], 'struct_or_union')
    
    def p_struct_declaration_list(self, p):
        '''struct_declaration_list : struct_declaration
                                | struct_declaration_list struct_declaration'''
        p[0] = Node(p[1:], 'struct_declaration_list')
    
    def p_struct_declaration(self, p):
        '''struct_declaration : type_specifier_list struct_declarator_list ';'  '''
        p[0] = Node(p[1:], 'struct_declaration')
    
    def p_struct_declarator_list(self, p):
        '''struct_declarator_list : struct_declarator
                                | struct_declarator_list ',' struct_declarator'''
        p[0] = Node(p[1:], 'struct_declarator_list')
    
    def p_struct_declarator(self, p):
        '''struct_declarator : declarator
                            | ':' constant_expr
                            | declarator ':' constant_expr'''
        p[0] = Node(p[1:], 'struct_declarator')
    
    def p_enum_specifier(self, p):
        '''enum_specifier : ENUM '{' enumerator_list '}'
                        | ENUM identifier '{' enumerator_list '}'
                        | ENUM identifier'''
        p[0] = Node(p[1:], 'enum_specifier')
    
    def p_enumerator_list(self, p):
        '''enumerator_list : enumerator
                        | enumerator_list ',' enumerator''' 
        p[0] = Node(p[1:], 'enumerator_list')
    
    def p_enumerator(self, p):
        '''enumerator : identifier
                    | identifier '=' constant_expr'''
        p[0] = Node(p[1:], 'enumerator')
    
    def p_declarator(self, p):
        '''declarator : declarator2
                    | pointer declarator2'''
        p[0] = Node(p[1:], 'declarator')
    
    def p_declarator2(self, p):
        '''declarator2 : identifier
                    | '(' declarator ')'
                    | declarator2 '[' ']'
                    | declarator2 '[' constant_expr ']'
                    | declarator2 '(' ')'
                    | declarator2 '(' parameter_type_list ')'
                    | declarator2 '(' parameter_identifier_list ')'  '''
        p[0] = Node(p[1:], 'declarator2')
    
    def p_pointer(self, p):
        '''pointer : '*'
                | '*' type_specifier_list
                | '*' pointer
                | '*' type_specifier_list pointer'''  
        p[0] = Node(p[1:], 'pointer')  
    
    def p_type_specifier_list(self, p):
        '''type_specifier_list : type_specifier
                            | type_specifier_list type_specifier'''
        p[0] = Node(p[1:], 'type_specifier_list')
    
    def p_parameter_identifier_list(self, p):
        '''parameter_identifier_list : identifier_list
                                    | identifier_list ',' ELIPSIS'''
        p[0] = Node(p[1:], 'parameter_identifier_list')
    
    def p_identifier_list(self, p):
        '''identifier_list : identifier
                        | identifier_list ',' identifier'''
        p[0] = Node(p[1:], 'identifier_list')
    
    def p_parameter_type_list(self, p):
        '''parameter_type_list : parameter_list
                            | parameter_list ',' ELIPSIS'''
        p[0] = Node(p[1:], 'parameter_type_list')
    
    def p_parameter_list(self, p):
        '''parameter_list : parameter_declaration
                        | parameter_list ',' parameter_declaration'''
        p[0] = Node(p[1:], 'parameter_list')
    
    def p_parameter_declaration(self, p):
        '''parameter_declaration : type_specifier_list declarator
                                | type_name'''
        p[0] = Node(p[1:], 'parameter_declaration')
    
    def p_type_name(self, p):
        '''type_name : type_specifier_list
                    | type_specifier_list abstract_declarator'''
        p[0] = Node(p[1:], 'type_name')
    
    def p_abstract_declarator(self, p):
        '''abstract_declarator : pointer
                            | abstract_declarator2
                            | pointer abstract_declarator2'''
        p[0] = Node(p[1:], 'abstract_declarator')
    
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
        p[0] = Node(p[1:], 'abstract_declarator2')
    
    def p_initializer(self, p):
        '''initializer : assignment_expr
                    | '{' initializer_list '}'
                    | '{' initializer_list ',' '}' '''
        p[0] = Node(p[1:], 'initializer')
    
    def p_initializer_list(self, p):
        '''initializer_list : initializer
                            | initializer_list ',' initializer'''
        p[0] = Node(p[1:], 'initializer_list')
    
    def p_statement(self, p):
        '''statement : labeled_statement
                    | compound_statement
                    | expression_statement
                    | selection_statement
                    | iteration_statement
                    | jump_statement'''
        p[0] = Node(p[1:], 'statement')
    
    def p_labeled_statement(self, p):
        '''labeled_statement : identifier ':' statement
                            | CASE constant_expr ':' statement
                            | DEFAULT ':' statement'''
        p[0] = Node(p[1:], 'labeled_statement')
    
    def p_left_bracket(self, p):
        '''left_bracket : '{' '''
        p[0] = Node(p[1:], 'left_bracket')
        
    def p_right_bracket(self, p):
        '''right_bracket : '}' '''
        p[0] = Node(p[1:], 'right_bracket')
    
    def p_compound_statement(self, p):
        '''compound_statement : left_bracket right_bracket
                            | left_bracket statement_list right_bracket
                            | left_bracket declaration_list right_bracket
                            | left_bracket declaration_list statement_list right_bracket'''
        p[0] = Node(p[1:], 'compound_statement')
    
    def p_declaration_list(self, p):
        '''declaration_list : declaration
                            | declaration_list declaration'''
        p[0] = Node(p[1:], 'declaration_list')
    
    def p_statement_list(self, p):
        '''statement_list : statement
                          | statement_list statement'''
        p[0] = Node(p[1:], 'statement_list')
    
    def p_expr_statement(self, p):
        '''expression_statement : ';'
                                | expr ';' '''
        p[0] = Node(p[1:], 'expression_statement')
    
    def p_selection_statement(self, p):
        '''selection_statement : IF '(' expr ')' statement
                               | IF '(' expr ')' statement ELSE statement
                               | SWITCH '(' expr ')' statement'''
        p[0] = Node(p[1:], 'selection_statement')
    
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
        p[0] = Node(p[1:], 'iteration_statement')
    
    def p_jump_statement(self, p):
        '''jump_statement : GOTO identifier ';'
                        | CONTINUE ';'
                        | BREAK ';'
                        | RETURN ';'
                        | RETURN expr ';' '''
        p[0] = Node(p[1:], 'jump_statement')
    
    def p_code(self, p):
        '''code : file'''
        p[0] = Node(p[1:], 'code')
    
    def p_file(self, p):
        '''file : external_definition
                | file external_definition '''
        p[0] = Node(p[1:], 'file')
    
    def p_external_definition(self, p):
        '''external_definition : function_definition
                               | declaration'''
        p[0] = Node(p[1:], 'external_definition')
    
    def p_function_definition(self, p):
        '''function_definition : declarator function_body
                               | declaration_specifiers declarator function_body'''
        p[0] = Node(p[1:], 'function_definition')
    
    def p_function_body(self, p):
        '''function_body : compound_statement
                         | declaration_list compound_statement
        '''
        p[0] = Node(p[1:], 'function_body')
    
    def p_identifier(self, p):
        '''identifier : IDENTIFIER'''
        p[0] = Node(p[1:], 'identifier')
    
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