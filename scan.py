'''Defines the lexer for the compiler. Equivalent to lex.l'''
import ply.lex as lex
from ply.lex import TOKEN
from tokens import tokens, Tokens, literals, reserved
import c_types

D = r'[0-9]'
L = r'[a-zA-Z_]'
H = r'[a-fA-F0-9]'
E = r'[Ee][+-]?(' + D + ')+'
FS = r'(f|F|l|L)'
IS = r'(u|U|l|L)'

class C_Lexer(object):
    '''The lexer object. Defines tokens, literals, and reserved words.
    Usage:
        c_lexer = C_Lexer(symbol_table, typedef_table)
        lexer = c_lexer.build()
        lexer.input('your input string') 
        t = lexer.token() #gets the next token'''
    
    # List of token names.   This is always required
    tokens = tokens
    literals = literals
    
    def __init__(self, symbol_table, typedef_table):
        self.symbol_table = symbol_table
        self.typedef_table = typedef_table
        self.token_stack = []
        self.next_token = None
    
    comment = r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'
    @TOKEN(comment)
    def t_COMMENT(self, token):
        #print token.lexer.lineno, len(token.value.split('\n')), token.value.split('\n')
        lines = len(token.value.split('\n')) - 1
        if lines < 0: lines = 0
        token.lexer.lineno += lines
    
    identifier = '(' + L + ')((' + L + ')|(' + D + '))*'
    @TOKEN(identifier)
    def t_IDENTIFIER(self, token):
        #if not reserved.has_key(token.value):
            #if not self.symbol_table.find_symbol(token.value):
                #self.symbol_table.create_symbol(c_types.Identifier(token.value))
        token.type = reserved.get(token.value,'IDENTIFIER')
        return token
    
    const_char = "'(\\.|[^\\'])+'"
    @TOKEN(const_char)
    def t_CONST_CHAR(self, token):
        token.type = 'CONSTANT'
        token.value = c_types.Constant(token.value[1:-1], self.typedef_table.find_type('char'))
        return token
    
    const_hex = '0[xX](' + H + ')+(' + IS + ')?'
    @TOKEN(const_hex)
    def t_CONST_HEX(self, token):
        token.type = 'CONSTANT'
        token.value = c_types.Constant(int(token.value, 16), self.typedef_table.find_type('int'))
        return token
    
    const_float1 = '(' + D + ')+' + '(' + E + ')' + '(' + FS + ')?'#{D}+{E}{FS}?
    @TOKEN(const_float1)
    def t_CONST_FLOAT1(self, token):
        token.type = 'CONSTANT'
        token.value = c_types.Constant(float(token.value), self.typedef_table.find_type('float'))
        return token
    
    const_float2 = '(' + D + ')*\.(' + D + ')+(' + E + ')?' + '(' + FS + ')?'#{D}*"."{D}+({E})?{FS}?
    @TOKEN(const_float2)
    def t_CONST_FLOAT2(self, token):
        token.type = 'CONSTANT'
        token.value = c_types.Constant(float(token.value), self.typedef_table.find_type('float'))
        return token
    
    const_float3 = '(' + D + ')+\.(' + D + ')*(' + E + ')?' + '(' + FS + ')?'#{D}+"."{D}*({E})?{FS}?
    @TOKEN(const_float3)
    def t_CONST_FLOAT3(self, token):
        token.type = 'CONSTANT'
        token.value = c_types.Constant(float(token.value), self.typedef_table.find_type('float'))
        return token
    
    const_dec_oct = '(' + D + ')+(' + IS + ')?'
    @TOKEN(const_dec_oct)
    def t_CONST_DEC_OCT(self, token):
        token.type = 'CONSTANT'
        if len(token.value) > 1 and token.value[0] == '0':
            token.value = c_types.Constant(int(token.value, 8), self.typedef_table.find_type('int'))
        else:
            token.value = c_types.Constant(int(token.value, 10),self.typedef_table.find_type('int'))
        return token
        
    string_literal = r'\"(\\.|[^\\"])*\"'
    @TOKEN(string_literal)
    def t_STRING_LITERAL(self, token):
        token.type = 'STRING_LITERAL'
        token.value = token.value[1:-1]
        return token;
    
    #0[xX]{H}+{IS}?
    
    # Regular expression rules for simple tokens
    t_RIGHT_ASSIGN = r'>>='
    t_LEFT_ASSIGN = r'<<='
    t_ADD_ASSIGN = r'\+='
    t_SUB_ASSIGN = r'\-='
    t_MUL_ASSIGN = r'\*='
    t_DIV_ASSIGN = r'\/='
    t_MOD_ASSIGN = r'\%='
    t_AND_ASSIGN = r'\&='
    t_XOR_ASSIGN = r'\^='
    t_OR_ASSIGN = r'\|='
    t_RIGHT_OP = r'>>'
    t_LEFT_OP = r'<<'
    t_INC_OP = r'\+\+'
    t_DEC_OP = r'\-\-'
    t_PTR_OP = r'\->'
    t_AND_OP = r'\&\&'
    t_OR_OP = r'\|\|'
    t_LE_OP = r'\<='
    t_GE_OP = r'\>='
    t_EQ_OP = r'=='
    t_NE_OP = r'\!='

    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t\v\f'

    # Error handling rule
    def t_error(self,t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)

    def build(self,**kwargs):
        '''Build the lexer'''
        self.lexer = lex.lex(object=self, **kwargs)
        def h(self, f, *args, **kwargs):
            def token(*args, **kwargs):
                '''A decorator on the original token function'''
                t = f()
                self.token_stack.append(self.next_token)
                self.next_token = t
                return t
            return token
        self.lexer.token = h(self, self.lexer.token)

    def test(self,data):
        '''Test function'''
        self.lexer.input(data)
        while 1:
             tok = lexer.token()
             if not tok: break
             print tok

# Build the lexer and try it out
#m = C_Lexer()
#m.build()           # Build the lexer
#lexer = m.lexer

if __name__ == '__main__':
    # Test it out
    f = open('test.c', 'r')
    data = f.read()
    f.close()
    
    #3 + 4 * 10
    #+ -20 *2
    
    # Give the lexer some input
    lexer.input(data)
    
    # Tokenize
    while 1:
        tok = lexer.token()
        if not tok: break      # No more input
        print tok, tok.value