from utils.symbol_table import *
import utils.ast as ast
from utils.node_visitor import NodeVisitor
from ply.lex import LexToken
import config


class PreProcess(NodeVisitor):

    def __init__(self, semantic_messages):
        # Creating and pushing built-in function symbols to the global symbol table
        self.create_and_push_builtin_funcs(config.global_symbol_table)
        self.semantic_messages = semantic_messages

    def visit_Prog2(self, node, table):
        # Visiting the function and program nodes of Prog2
        self.visit(node.func, config.global_symbol_table)
        self.visit(node.prog, config.global_symbol_table)

    def visit_Func(self, node, table):
        # Getting the parameters of the function
        parameters = self.get_parameters(node)
        function_name = node.iden.iden_value
        name = node.iden.iden_value

        # Creating a FunctionSymbol object based on the function type
        if node.type.type_value == "vector":
            function_symbol = FunctionSymbol(
                name, node.type.type_value + " " + node.type.vector_type_value, parameters)
        else:
            function_symbol = FunctionSymbol(
                name, node.type.type_value, parameters)

        # Checking if the function symbol can be added to the symbol table
        if not table.put(function_symbol):
            # If there is a function or variable with the same identifier
            self.semantic_messages.add_message(
                {"message": f"Identifier '{name}' already exists", "lineno": node.flist.lineno})
            return

        # Creating a new symbol table for the function body block
        function_body_table = SymbolTable(
            table, function_name+"_function_body_block_table")

        # Adding the function parameters to the function body symbol table
        for par in parameters:
            name = par["iden_value"]
            if not function_body_table.is_exist(name):
                if "vector" in par["type"]:
                    vector_type = par["type"].split(" ")[1]
                    function_body_table.put(VectorSymbol(name, vector_type))
                else:
                    type = par["type"]
                    function_body_table.put(VariableSymbol(name, type))
            else:
                self.semantic_messages.add_message(
                    {"message": f"'{name}' already defined", "lineno": node.flist.lineno})

        # Visiting the function choice node with the function body symbol table
        self.visit(node.func_choice, function_body_table)

    def visit_FuncChoice1(self, node, table):
        # Visiting the body node of FuncChoice1
        self.visit(node.body, table)

    def visit_FuncChoice2(self, node, table):
        pass

    def visit_Body2(self, node, table):
        # Visiting the statement and body nodes of Body2
        self.visit(node.stmt, table)
        self.visit(node.body, table)

    def visit_Stmt1(self, node, table):
        pass

    def visit_Stmt2(self, node, table):
        pass

    def visit_Stmt3(self, node, table):
        # Creating a new symbol table for the "if" block
        if_block_symbol_table = SymbolTable(
            table, f"if_block_{node.lineno}")
        
        # Visiting the statement and else choice nodes of Stmt3
        self.visit(node.stmt, if_block_symbol_table)
        self.visit(node.else_choice, table)

    def visit_ElseChoice2(self, node, table):
        # Creating a new symbol table for the "else" block
        else_block_symbol_table = SymbolTable(
            table, f"else_block_{node.lineno}")

        # Visiting the statement node of ElseChoice2
        self.visit(node.stmt, else_block_symbol_table)

    def visit_Stmt4(self, node, table):
        # Creating a new symbol table for the "while" block of a while loop
        while_block_symbol_table = SymbolTable(
            table, f"while_block_{node.lineno}")

        # Visiting the statement node of Stmt4
        self.visit(node.stmt, while_block_symbol_table)

    def visit_Stmt5(self, node, table):
        # Creating a new symbol table for the "for" block
        for_block_symbol_table = SymbolTable(
            table, f"for_block_{node.lineno}")

        # Adding the loop variable to the for block symbol table
        name = node.iden.iden_value
        type = "int"
        iden = VariableSymbol(name, type)
        for_block_symbol_table.put(iden)

        # Visiting the statement node of Stmt5
        self.visit(node.stmt, for_block_symbol_table)

    def visit_Stmt6(self, node, table):
        pass

    def visit_Stmt7(self, node, table):
        # Creating a new symbol table for the "body" block
        body_block_symbol_table = SymbolTable(
            table, f"body_block_{node.lineno}")

        # Visiting the body node of Stmt7
        self.visit(node.body, body_block_symbol_table)

    def visit_Stmt8(self, node, table):
        # Visiting the function node of Stmt8
        self.visit(node.func, table)

    def visit_Empty(self, node, table):
        pass

    def create_and_push_builtin_funcs(self, table):
        # Creating and pushing built-in function symbols to the given symbol table
        
        scan_function_symbol = FunctionSymbol(name="scan",
                                              type="int",
                                              parameters=[])
        table.put(scan_function_symbol)

        print_funcition_symbol = FunctionSymbol(name="print",
                                                type="int",
                                                parameters=[{"iden": "n", "type": ["int", "str"]}])
        table.put(print_funcition_symbol)

        lsit_funcition_symbol = FunctionSymbol(name="list",
                                               type="vector int",
                                               parameters=[{"iden": "x", "type": ["int"]}])
        table.put(lsit_funcition_symbol)

        length_funcition_symbol = FunctionSymbol(name="length",
                                                 type="int",
                                                 parameters=[{"iden": "V", "type": ["vector int", "vector str"]}])
        table.put(length_funcition_symbol)

        exit_funcition_symbol = FunctionSymbol(name="exit",
                                               type="int",
                                               parameters=[{"iden": "n", "type": ["int"]}])
        table.put(exit_funcition_symbol)

    def get_parameters(self, node):
        # Getting the parameters of a function

        parameters = []
        flist = node.flist

        # Checking if there are any parameters
        if isinstance(flist, LexToken):
            return parameters

        # Traversing through the parameter list and adding each parameter to the list
        if not isinstance(flist, ast.Empty):
            if flist.iden:
                type = flist.type.type_value
                if type == "vector":
                    type += " " + flist.type.vector_type_value
                parameters.append(
                    {"iden_value": flist.iden.iden_value, "type": type})
            while hasattr(flist, "flist"):
                flist = flist.flist
                if (not isinstance(flist, ast.Empty)):
                    type = flist.type.type_value
                    if type == "vector":
                        type += " " + flist.type.vector_type_value
                    parameters.append(
                        {"iden_value": flist.iden.iden_value, "type": type})

        # Reversing the list to maintain the correct order
        parameters.reverse()
        return parameters
