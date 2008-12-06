# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex
from ply.lex import TOKEN
from tokens import tokens, Tokens, literals, reserved

D = r'[0-9]'
L = r'[a-zA-Z_]'
H = r'[a-fA-F0-9]'
E = r'[Ee][+-]?{D}+'
FS = r'(f|F|l|L)'
IS = r'(u|U|l|L)*'
class C_Lexer(object):
    # List of token names.   This is always required
    tokens = tokens
    literals = literals
    
    identifier = '(' + L + ')((' + L + ')|(' + D + '))*'
    @TOKEN(identifier)
    def t_IDENTIFIER(self, token):
        print 'hello', token
        token.type = reserved.get(token.value,'IDENTIFIER')
        return token
    
    const_char = "'(\\.|[^\\'])+'"
    @TOKEN(const_char)
    def t_CONST_CHAR(self, token):
        token.type = 'CONSTANT'
        token.value = token.value[1]
        return token
    
    # Regular expression rules for simple tokens
    #t_PLUS    = r'\+'
    #t_MINUS   = r'-'
    #t_TIMES   = r'\*'
    #t_DIVIDE  = r'/'
    #t_LPAREN  = r'\('
    #t_RPAREN  = r'\)'

    # A regular expression rule with some action code
    # Note addition of self parameter since we're in a class
    #def t_NUMBER(self,t):
        #r'\d+'
        #try:
             #t.value = int(t.value)    
        #except ValueError:
             #print "Line %d: Number %s is too large!" % (t.lineno,t.value)
             #t.value = 0
        #return t

    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self,t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(object=self, **kwargs)
    
    # Test it output
    def test(self,data):
        self.lexer.input(data)
        while 1:
             tok = lexer.token()
             if not tok: break
             print tok

# Build the lexer and try it out
m = C_Lexer()
m.build()           # Build the lexer
lexer = m.lexer

if __name__ == '__main__':
    # Test it out
    data = '''
    int hello;
    hello = 0;
    char c;
    c = 'x';
    '''
    
    #3 + 4 * 10
    #+ -20 *2
    
    # Give the lexer some input
    lexer.input(data)
    
    # Tokenize
    while 1:
        tok = lexer.token()
        if not tok: break      # No more input
        print tok, tok.value