import ply.lex as lex

class Lexer(object):
    def __init__(self, tokens):
        self.lexer = lex.lex(object=tokens)

    def build(self, data):
        self.lexer.input(data)
        for tok in self.lexer:
            print(tok)