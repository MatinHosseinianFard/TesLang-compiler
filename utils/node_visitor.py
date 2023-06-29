from ply.lex import LexToken
from utils.symbol_table import *
import utils.ast as ast

# Class definition for NodeVisitor
class NodeVisitor(object):
    
    # Method to visit a node
    def visit(self, node, table=None):
        # Generate the method name based on the class name of the node
        method = 'visit_' + node.__class__.__name__

        # Get the appropriate visitor method based on the generated method name
        visitor = getattr(self, method, self.no_need_to_visit)

        # Invoke the visitor method with the node and table as arguments
        return visitor(node, table)

    # Method to handle cases where visiting a node is not needed
    def no_need_to_visit(self, node, table):
        # No operation, simply pass
        pass

