from os import error
from utils.symbol_table import *
import utils.AST as AST

class NodeVisitor(object):
    
    def visit(self, node, table=None):
        # print(node)
        method = 'visit_' + node.__class__.__name__

        # print(method)
        visitor = getattr(self, method, self.generic_visit)
        # visitor = getattr(self, method)
        # print(visitor)

        return visitor(node, table)


    def generic_visit(self, node, table):        # Called if no explicit visitor function exists for a node.
        node = node["ast"]
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)
