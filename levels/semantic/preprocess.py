from utils.symbol_table import *
import utils.ast as ast
from utils.node_visitor import NodeVisitor
from ply.lex import LexToken
import config


class PreProcess(NodeVisitor):

    def __init__(self, semantic_messages):
        self.create_and_push_builtin_funcs(config.global_symbol_table)
        self.semantic_messages = semantic_messages

    def visit_Prog2(self, node, table):
        self.visit(node.func, config.global_symbol_table)
        self.visit(node.prog, config.global_symbol_table)

    def visit_Func(self, node, table):
        parameters = self.get_parameters(node)
        function_name = node.iden.iden_value
        name = node.iden.iden_value

        if node.type.type_value == "vector":
            function_symbol = FunctionSymbol(
                name, node.type.type_value + " " + node.type.vector_type_value, parameters)
        else:
            function_symbol = FunctionSymbol(
                name, node.type.type_value, parameters)

        if not table.put(function_symbol):
            # if there is a function or var with the same identifier
            self.semantic_messages.add_message(
                {"message": f"Identifier '{name}' already exists", "lineno": node.flist.lineno})
            return

        function_body_table = SymbolTable(
            table, function_name+"_function_body_block_table")
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

        self.visit(node.func_choice, function_body_table)

    def visit_FuncChoice1(self, node, table):
        self.visit(node.body, table)

    def visit_FuncChoice2(self, node, table):
        pass

    def visit_Body2(self, node, table):
        self.visit(node.stmt, table)
        self.visit(node.body, table)

    # def visit_Stmt1(self, node, table):
    #     pass

    def visit_Stmt2(self, node, table):
        self.visit(node.defvar, table)

    def visit_Stmt3(self, node, table):
        if_block_symbol_table = SymbolTable(
            table, f"if_block_{node.lineno}")  # symbol table for "if" block
        self.visit(node.stmt, if_block_symbol_table)
        self.visit(node.else_choice, table)

    def visit_ElseChoice2(self, node, table):
        else_block_symbol_table = SymbolTable(
            table, f"else_block_{node.lineno}")  # symbol table for "else" block
        self.visit(node.stmt, else_block_symbol_table)

    def visit_Stmt4(self, node, table):
        # symbol table for "while" block of a while
        while_block_symbol_table = SymbolTable(
            table, f"while_block_{node.lineno}")
        self.visit(node.stmt, while_block_symbol_table)

    def visit_Stmt5(self, node, table):
        for_block_symbol_table = SymbolTable(
            table, f"for_block_{node.lineno}")  # symbol table for "for" block
        name = node.iden.iden_value
        type = "int"
        iden = VariableSymbol(name, type)
        for_block_symbol_table.put(iden)
        self.visit(node.stmt, for_block_symbol_table)

    # def visit_Stmt6(self, node, table):
    #     pass

    def visit_Stmt7(self, node, table):
        body_block_symbol_table = SymbolTable(
            table, f"body_block_{node.lineno}")  # symbol table for "body" block
        self.visit(node.body, body_block_symbol_table)

    def visit_Stmt8(self, node, table):
        self.visit(node.func, table)

    # def visit_Defvar(self, node, table):
    #     pass

    # def visit_DefvarChoice2(self, node, table):
    #     pass

    # def visit_Expr1(self, node, table):
    #     pass

    # def visit_Expr2(self, node, table):
    #     pass

    # def visit_Expr3(self, node, table):
    #     pass

    # def visit_Expr4(self, node, table):
    #     pass

    # def visit_Expr5(self, node, table):
    #     pass

    # def visit_Expr6(self, node, table):
    #     pass

    # def visit_Expr7(self, node, table):
    #     pass

    # def visit_Expr8(self, node, table):
    #     pass

    # def visit_Expr9(self, node, table):
    #     pass

    # def visit_Clist1(self, node, table):
    #     pass

    # def visit_Clist2(self, node, table):
    #     pass

    # def visit_Clist3(self, node, table):
    #     pass
    
    # def visit_Type(self, node, table):
    #     pass

    # def visit_Iden(self, node, table):
    #     pass

    # def visit_Str(self, node, table):
    #     pass

    # def visit_Num(self, node, table):
    #     pass

    # def visit_Empty(self, node, table):
    #     pass

    def create_and_push_builtin_funcs(self, table):
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
        parameters = []
        flist = node.flist
        if isinstance(flist, LexToken):
            return parameters
        if not isinstance(flist, ast.Empty):
            if flist.iden:
                type = flist.type.type_value
                if type == "vector":
                    type += " " + flist.type.vector_type_value
                parameters.append({"iden_value": flist.iden.iden_value, "type": type})
            while hasattr(flist, "flist"):
                flist = flist.flist
                if (not isinstance(flist, ast.Empty)):
                    type = flist.type.type_value
                    if type == "vector":
                        type += " " + flist.type.vector_type_value
                    parameters.append({"iden_value": flist.iden.iden_value, "type": type})

        parameters.reverse()
        return parameters