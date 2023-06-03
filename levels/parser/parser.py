import ply.yacc as yacc

class Parser(object):
    def __init__(self, grammar):
        self.parser = yacc.yacc(debug=True, module= grammar)

    def build(self, data):
        self.parser.parse(data, debug=True)