
    def t_SEMICOLON(self, token):
        '\;'
        token.type = token.value
        print token.type
        return token
    
    def t_RIGHT_BRACKET(self, token):
        '\}'
        token.type = token.value
        return token
    
    def t_LEFT_BRACKET(self, token):
        '\{'
        token.type = token.value
        return token
    
    def t_COMMA(self, token):
        '\,'
        token.type = token.value
        return token
    
    def t_COLON(self, token):
        '\:'
        token.type = token.value
        return token
    
    def t_EQUAL_SIGN(self, token):
        '\='
        token.type = token.value
        return token
    
    def t_RIGHT_PAREN(self, token):
        '\)'
        token.type = token.value
        return token
    
    def t_LEFT_PAREN(self, token):
        '\('
        token.type = token.value
        return token
    
    def t_RIGHT_SQUARE_BRACKET(self, token):
        '\]'
        token.type = token.value
        return token
    
    def t_LEFT_SQUARE_BRACKET(self, token):
        '\['
        token.type = token.value
        return token
    
    def t_DOT(self, token):
        '\.'
        token.type = token.value
        return token
    
    def t_AMPERSTAND(self, token):
        '\&'
        token.type = token.value
        return token
    
    def t_EXCLAMATION_POINT(self, token):
        '\!'
        token.type = token.value
        return token
    
    def t_TILDA(self, token):
        '\~'
        token.type = token.value
        return token
    
    def t_MINUS_SIGN(self, token):
        '\-'
        token.type = token.value
        return token
    
    def t_PLUS_SIGN(self, token):
        '\+'
        token.type = token.value
        return token
    
    def t_STAR(self, token):
        '\*'
        token.type = token.value
        return token
    
    def t_FORWARD_SLASH(self, token):
        '\/'
        token.type = token.value
        return token
    
    def t_PERCENT_SIGN(self, token):
        '\%'
        token.type = token.value
        return token
    
    def t_LT(self, token):
        '\<'
        token.type = token.value
        return token
    
    def t_GT(self, token):
        '\>'
        token.type = token.value
        return token
    
    def t_CARET(self, token):
        '\^'
        token.type = token.value
        return token
    
    def t_VBAR(self, token):
        '\|'
        token.type = token.value
        return token
    
    def t_QUESTION_MARK(self, token):
        '\?'
        token.type = token.value
        return token
    