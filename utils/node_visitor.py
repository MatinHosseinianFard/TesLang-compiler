from ply.lex import LexToken
from utils.symbol_table import *
import utils.ast as ast

class NodeVisitor(object):
    
    def visit(self, node, table=None):
        # print(node)
        method = 'visit_' + node.__class__.__name__

        # print(method)
        # visitor = getattr(self, method, self.generic_visit)
        visitor = getattr(self, method, self.no_need_to_visit)
        # print(visitor)

        return visitor(node, table)

    def no_need_to_visit(self, node, table):
        pass
    # def generic_visit(self, node, table):
    #     if isinstance(node, LexToken):
    #         return        # Called if no explicit visitor function exists for a node.
    #     node = node["ast"]
    #     if isinstance(node, list):
    #         for elem in node:
    #             self.visit(elem)
    #     else:
    #         for child in node.children:
    #             if isinstance(child, list):
    #                 for item in child:
    #                     if isinstance(item, ast.Node):
    #                         self.visit(item)
    #             elif isinstance(child, ast.Node):
    #                 self.visit(child)
