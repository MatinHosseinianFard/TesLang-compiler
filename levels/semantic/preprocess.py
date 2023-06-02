from utils.symbol_table import *
import utils.AST as AST
from utils.node_visitor import NodeVisitor
from ply.lex import LexToken
import config


class PreProcess(NodeVisitor):

    def __init__(self, semantic_messages):
        self.create_and_push_builtin_funcs(config.global_symbol_table)
        self.semantic_messages = semantic_messages
    
    def visit_Prog1(self, node, table):
        #print(f"visiting: prog1")
        pass

    def visit_Prog2(self, node, table):
        #print(f"visiting: prog2")
        self.visit(node.func, config.global_symbol_table)
        self.visit(node.prog, config.global_symbol_table)


    def visit_Func(self, node, table):
        #print(f"visiting: func")

        parameters = self.get_parameters(node)
        # print(node.iden)
        function_name= node.iden.iden_value


        name = node.iden.iden_value

        function_symbol = FunctionSymbol(name, node.type.type_value, parameters)
        if not table.put(function_symbol):
            # if there is a function or var with the same identifier
            self.semantic_messages.add_message({"message":f"Identifier '{name}' already exists", "lineno":node.flist.lineno})
            return
        function_body_table = SymbolTable(table, function_name+"_function_body_block_table")
        for par in parameters:
            name = par["iden"].iden_value
            type = par["type"].type_value
            #print(f"funcion {function_name}'s arg: name: '{name}', type: {type}'" )
            if not function_body_table.put(VariableSymbol(name, type)):
                self.semantic_messages.add_message({"message": f"'{name}' already defined", "lineno": node.flist.lineno})
        self.visit(node.func_choice, function_body_table)
        
    def visit_FuncChoice1(self, node, table):
        self.visit(node.body, table)
        
    def visit_FuncChoice2(self, node, table):
        pass

    def visit_Body1(self, node, table):
        #print(f"visiting: body1")
        pass            


    def visit_Body2(self, node, table):
        #print(f"visiting: body2")
        self.visit(node.stmt, table)
        self.visit(node.body, table)


    def visit_Stmt1(self, node, table):
        #print(f"visiting: stmt1")
        pass            

    def visit_Stmt2(self, node, table):
        #print(f"visiting: stmt2")
        self.visit(node.defvar, table)


    def visit_Stmt3(self, node, table):
        #print(f"visiting: stmt3")
        if_block_symbol_table = SymbolTable(table, f"if_block_{node.lineno}") # symbol table for "if" block
        self.visit(node.stmt, if_block_symbol_table)
        self.visit(node.else_choice, table)


    # def visit_ElseChoice1(self, node, table):
    #     #print(f"visiting: stmt4")
    #     pass


    def visit_ElseChoice2(self, node, table):
        #print(f"visiting: stmt4")
        else_block_symbol_table = SymbolTable(table, f"else_block_{node.lineno}") # symbol table for "else" block
        self.visit(node.stmt, else_block_symbol_table)


    def visit_Stmt4(self, node, table):
        #print(f"visiting: stmt4")
        while_block_symbol_table = SymbolTable(table, f"while_block_{node.lineno}") # symbol table for "while" block of a while
        self.visit(node.stmt, while_block_symbol_table)


    def visit_Stmt5(self, node, table):
        #print(f"visiting: stmt5")
        for_block_symbol_table = SymbolTable(table, f"for_block_{node.lineno}") # symbol table for "for" block
        name = node.iden.iden_value
        type = "int"
        iden = VariableSymbol(name, type)
        for_block_symbol_table.put(iden)
        self.visit(node.stmt, for_block_symbol_table)


    def visit_Stmt6(self, node, table):
        #print(f"visiting: stmt6")
        pass

    def visit_Stmt7(self, node, table):
        #print(f"visiting: stmt7")
        body_block_symbol_table = SymbolTable(table, f"body_block_{node.lineno}") # symbol table for "body" block
        self.visit(node.body, body_block_symbol_table)


    def visit_Stmt7(self, node, table):
        #print(f"visiting: stmt7")
        body_block_symbol_table = SymbolTable(table, f"body_block_{node.lineno}") # symbol table for "body" block
        self.visit(node.body, body_block_symbol_table)

    
    def visit_Stmt8(self, node, table):
        #print(f"visiting: stmt7")
        self.visit(node.func, table)

    
    def visit_Defvar(self, node, table):
        # name = node.iden.iden_value["name"]
        # type = node.type.type_value["name"]
        # iden = VariableSymbol(name, type)
        # table.put(iden)
        pass

    
    def visit_DefvarChoice2(self, node, table):
        pass
            
    def visit_Type(self, node, table):
        #print(f"visiting: type")
        pass
    
    def visit_Str(self, node, table):
        #print(f"visiting: str")
        pass

    def visit_Iden(self, node, table):
        #print(f"visiting: iden")
        pass

    def visit_Empty(self, node, table):
        #print(f"visiting: empty")
        pass



    def create_and_push_builtin_funcs(self, table):
        scan_function_symbol = FunctionSymbol("scan", "int", [] )
        table.put(scan_function_symbol)

        print_funcition_symbol = FunctionSymbol("print", "int", [{"iden": "n", "type": "int"}] )
        table.put(print_funcition_symbol)

        lsit_funcition_symbol = FunctionSymbol("list", "vector", [{"iden": "x", "type": "int"}] )
        table.put(lsit_funcition_symbol)

        getList_funcition_symbol = FunctionSymbol("getList", "vector", [{"iden": "A", "type": "vector"}] )
        table.put(getList_funcition_symbol)

        printList_funcition_symbol = FunctionSymbol("printList", "vector", [{"iden": "A", "type": "vector"}] )
        table.put(printList_funcition_symbol)

        length_funcition_symbol = FunctionSymbol("length", "int", [{"iden": "A", "type": "vector"}] )
        table.put(length_funcition_symbol)

        exit_funcition_symbol = FunctionSymbol("exit", "int", [{"iden": "n", "type": "int"}] )
        table.put(exit_funcition_symbol)


    def get_parameters(self, node):
        parameters = []
        flist = node.flist
        if isinstance(flist, LexToken):
            return parameters
        # print(flist)
        if not isinstance(flist, AST.Empty):
            if flist.iden:
                parameters.append({"iden": flist.iden, "type": flist.type})
            while hasattr(flist, "flist"):
                flist = flist.flist
                if (not isinstance(flist, AST.Empty)):
                    parameters.append({"iden": flist.iden, "type": flist.type})
        parameters.reverse()
        return parameters