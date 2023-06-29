from ply.lex import LexToken
from utils.symbol_table import *
import utils.ast as ast

class NodeVisitor(object):
    
    def visit(self, node, table=None):
        method = 'visit_' + node.__class__.__name__

        visitor = getattr(self, method, self.no_need_to_visit)

        return visitor(node, table)

    def no_need_to_visit(self, node, table):
        pass
