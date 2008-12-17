'''Class that represent the AST'''

class TerminalSymbol(object):
    '''Represents a terminal symbol on the AST'''
    
    def __init__(self, symbol):
        self.symbol = symbol
    
    def __str__(self): 
        return str(self.symbol)

class NonTerminalSymbol(object):
    '''Represents a non-terminal symbol on the AST'''
    
    def __init__(self, symbol):
        self.symbol = symbol
    
    def __str__(self):
        return str(self.symbol)

class Value(object):
    '''Represents the value passed in by lextoken.value on the AST'''
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)

class Attributes(object):
    
    def __init__(self):
        pass

class Node(object):
    '''Represents a vertice on the AST'''
    
    def __init__(self, production=None, symbol=''):
        if not production:
            self.children = []
        else:
            self.children = production[1:]
        
        if production: token_stack = production.lexer.lexmodule.token_stack[:]
        
        for index,child in enumerate(self.children):
            if child.__class__ != Node:
                n = Node(symbol=TerminalSymbol(child))
                for token in token_stack:
                    if token and token.value == child:
                        if len(token.type) < 2: break
                        n = Node(symbol=TerminalSymbol(token.type))
                        n2 = Node(symbol=Value(child))
                        n2.graph_color = "#88ff88"
                        n.children.append(n2)
                        break
                self.children[index] = n
                self.children[index].graph_color = "#8888ff"
        if production: self.symbol = NonTerminalSymbol(symbol)
        else: self.symbol = symbol
        self.type = None
        self.identifier = None
    
    def traverse(self, node, i=0):
        s = ' '*i + str(node) + '\n'
        if 'children' not in dir(node): return s
        for child in node.children:
            s += self.traverse(child, i+1)
        return s
    
    def print_out(self):
        return str(self.traverse(self))
    
    def __repr__(self): return str(self)
    
    def __str__(self):
        s = str(self.symbol)
        if self.type: s += ', ' + str(self.type)
        if self.identifier: s += ', ' + str(self.identifier)
        return '"' + s + '"'