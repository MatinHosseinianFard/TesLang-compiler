from utils.symbol_table import *
import utils.AST as AST
from utils.node_visitor import NodeVisitor
from ply.lex import LexToken
import config


class TypeChecker(NodeVisitor):

    def __init__(self, semantic_messages):
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
        function_symbol = table.get(node.iden.iden_value)
        function_name = function_symbol.name
        function_body_block = self.find_symbol_table(f"{function_name}_function_body_block_table", table)

        self.visit(node.func_choice, function_body_block)

        
    def visit_FuncChoice1(self, node, table):
        self.visit(node.body, table)
        
    
    def visit_FuncChoice2(self, node, table):
        pass

    
    def visit_Body1(self, node, table):
        #print(f"visiting: body1")
        self.visit(node.stmt, table)
            


    def visit_Body2(self, node, table):
        #print(f"visiting: body2")
        self.visit(node.stmt, table)
        self.visit(node.body, table)


    def visit_Stmt1(self, node, table):
        #print(f"visiting: stmt1")
        self.visit(node.expr, table)
            

    def visit_Stmt2(self, node, table):
        #print(f"visiting: stmt2")
        self.visit(node.defvar, table)


    def visit_Stmt3(self, node, table):
        #print(f"visiting: stmt3")
        self.visit(node.expr, table)
        if_block_symbol_table = self.find_symbol_table(f"if_block_{node.lineno}", table) # symbol table for "if" block
        self.visit(node.stmt, if_block_symbol_table)
        self.visit(node.else_choice, table)


    # def visit_ElseChoice1(self, node, table):
    #     #print(f"visiting: stmt4")
    #     pass
    

    def visit_ElseChoice2(self, node, table):
        #print(f"visiting: stmt4")
        else_block_symbol_table = self.find_symbol_table(f"else_block_{node.lineno}", table) # symbol table for "else" block
        self.visit(node.stmt, else_block_symbol_table)


    def visit_Stmt4(self, node, table):
        #print(f"visiting: stmt4")
        self.visit(node.expr, table)
        while_block_symbol_table = self.find_symbol_table(f"while_block_{node.lineno}", table) # symbol table for "while" block of a while
        self.visit(node.stmt, while_block_symbol_table)


    def visit_Stmt5(self, node, table):
        #print(f"visiting: stmt5")
        expr1_type = self.visit(node.expr1, table)
        expr2_type = self.visit(node.expr2, table)
        for_block_symbol_table = self.find_symbol_table(f"for_block_{node.lineno}", table) # symbol table for "for" block

        # setattr(node, "type", expr2_type)

        iden_symbol = "int"
        
        if iden_symbol != expr1_type:
                self.semantic_messages.add_message({"message": f"Two sides of '=' must be of same type! expr1 is of type: '{iden_symbol}' and expr2 is of type: '{expr1_type}'", "lineno":node.expr1.lineno})
        elif iden_symbol != expr2_type:
                self.semantic_messages.add_message({"message": f"expr2 is not vector if int", "lineno":node.expr2.lineno})

        self.visit(node.stmt, for_block_symbol_table)



    def visit_Stmt6(self, node, table):
        #print(f"visiting: stmt6")
        expr_type = self.visit(node.expr, table)
        #finding function name
        function_name = []
        while not "_function_body_block_table" in table.name and table:
            table = table.parent
            #print("checked", table.name)
        #found the function name
        if table:
            function_name = table.name.split("_function_body_block_table")[0]
            function_symbol = config.global_symbol_table.get(function_name)
            function_type = function_symbol.type
            if expr_type != function_type:
                self.semantic_messages.add_message({"message": f"Returning wrong type for function '{function_name}'. must return: '{function_type}', you're returning: '{expr_type}'", "lineno":node.expr.lineno})
        # did'nt found the corresponding function to this return
        else:
            self.semantic_messages.add_message({"message": f"Shouldn'n have put return here!","lineno": node.expr.lineno})
            


    def visit_Stmt7(self, node, table):
        #print(f"visiting: stmt7")
        body_block_symbol_table = self.find_symbol_table(f"body_block_{node.lineno}", table) # symbol table for "body" block
        self.visit(node.body, body_block_symbol_table)
    
    
    def visit_Stmt8(self, node, table):
        #print(f"visiting: stmt7")
        self.visit(node.func, table)

    
    def visit_Defvar(self, node, table):
        #print(f"visiting: defvar")
        name = node.iden.iden_value
        if isinstance(node.type, LexToken):
            type = "int"
        else:
            type = node.type.type_value

        if not table.put(VariableSymbol(name, type)):
                self.semantic_messages.add_message({"message": f"'{name}' already defined", "lineno":node.iden.lineno})
        
        self.visit(node.iden, table)
        self.visit(node.type, table)
        expr_type = self.visit(node.defvar_choice, table)
        # print(expr_type)
        if expr_type != "empty_rule":
            if type != expr_type:
                self.semantic_messages.add_message({"message": f"Two sides of '=' must be of same type! identifier is of type: '{type}' and experssions is of type: '{expr_type}'", "lineno":node.defvar_choice.lineno})

    

    def visit_DefvarChoice2(self, node, table):
        return self.visit(node.expr, table)
            
    
    def visit_Expr1(self, node, table):
        # calling an vector
        #print(f"visiting: expr2")
        type_of_vector_iden = self.visit(node.expr1, table)

        type_of_vector_index = self.visit(node.expr2, table)
        if type_of_vector_iden == "vector" and type_of_vector_index == "int":
            return "int"

        else:
            #print(type_of_vector_iden, type_of_vector_index)
            self.semantic_messages.add_message({"message": f"Id of the vector must of type 'vector'!", "lineno": node.expr1.lineno})
            if type_of_vector_index != "int":
                self.semantic_messages.add_message({"message": f'{node.expr2.lineno}: index of the vector must be of type \'int\'!', "lineno": node.expr2.lineno})
            return "null"


    def visit_Expr2(self, node, table):
        # calling an vector
        #print(f"visiting: expr2")
        # arguments = self.get_arguments(node, table)
        # if len(set(arguments)) == 1:
        return self.visit(node.clist, table)


    def visit_Expr3(self, node, table):
        #print(f"visiting: expr3")
        condition_expr = self.visit(node.expr1, table)
        true_block_expr = self.visit(node.expr2, table)
        false_block_expr = self.visit(node.expr3, table)
        if condition_expr == "null":
            # Therefore condition would be false
            return false_block_expr
        return true_block_expr
    

    def visit_Expr4(self, node, table):
        #print(f"visiting: expr4")
        first_operand = self.visit(node.expr1, table)
        # print(f"first: {first_operand} node: {node.expr1}")
        second_operand = self.visit(node.expr2, table)
        operator = node.oper
        #print(f'first operand type is {first_operand} and second is {second_operand} , operand: {operator}')


        #check if it's like id = expr
        first_operand_is_iden = isinstance(node.expr1, AST.Expr6)

        #dynamic type error handling! null type can be converted to Int or vector!
        #if operator is "=", assignment and first operand is a iden of type "null" you can assign anything to it
        if operator == "=" and first_operand == "null" and second_operand !="null" and first_operand_is_iden:
            first_operand_name = node.expr.iden.iden_value
            first_operand_symbol = table.get(first_operand_name)
            first_operand_symbol.type = second_operand
            first_operand = second_operand
            return second_operand

        if first_operand != second_operand:
            self.semantic_messages.add_message({"message": f"Two sides of '{operator}' must be of same type! expr1 is of type: '{first_operand}' and expr2 is of type: '{second_operand}'", "lineno":node.expr1.lineno})
            return "null"
        #print(f'first operand type is {first_operand} and second is {second_operand}')
        return first_operand
    


    def visit_Expr5(self, node, table):
        #print(f"visiting: expr5")
        #operator
        operand = self.visit(node.expr, table)
        operator = node.oper
        if operand == "int" :
            return operand
        elif operand == "null" and operator == "!":
            return "int"
        else:
            self.semantic_messages.add_message({"message": f"The operand of the '{operator}' must be of type 'int'", "lineno":node.expr.lineno})
            return "null"


    def visit_Expr6(self, node, table):
        #print(f"visiting: expr7")
        #search in table for the iden of this var, if not found, returns None
        iden_type = self.visit(node.iden, table)
        # print(f"iden_type: {iden_type}")
        if not iden_type:
            # for error handling we should create that var
            new_declared_symbol_for_error_handling = VariableSymbol(node.iden.iden_value,"null")
            table.put(new_declared_symbol_for_error_handling)
            return "null"
        
        return iden_type


    def visit_Expr7(self, node, table):
        #function call
        #print(f"visiting: expr1")
        function_iden = node.iden.iden_value
        function_symbol = table.get(function_iden)
        #check if function exists with this id
        # if not found, it's type automatically(in get function) is set to None
        if isinstance(function_symbol, FunctionSymbol):
            # get parameters
            parameters = self.get_parameters(function_symbol)

            # get arguments
            arguments = self.get_arguments(node, table)

            
            #print(f"{node.clist.lineno}: function: {function_iden}, arguments: {arguments}, parameters: {parameters}")
            # check number of arguments with number of parameters 
            if len(parameters) != len(arguments):
                # handle semantic error
                    self.semantic_messages.add_message({"message": f"Function '{function_iden}' expected {len(parameters)} arguments but got {len(arguments)} instead", "lineno": node.clist.lineno})
                    return function_symbol.type

            # check arguments types with parameters types
            for i in range(len(function_symbol.parameters)):
                par_type = parameters[i]
                arg_type = arguments[i]
                if par_type != arg_type:
                    # handle semantic error
                    self.semantic_messages.add_message({"message": f"{i+1}th argument of function '{function_iden}' type must be '{par_type}'", "lineno":node.clist.lineno})
                    return function_symbol.type
            # if number of arguments and their types where correct, return function iden's type
            return function_symbol.type
        

        #function is not declared but it can be called becasue of error handling, it returns "null"        
        else:
            #print("function not found", function_iden)
            # tries to create a symbol with function_name and type null
            # returns False if there is an id with that function_name

            result = table.get(function_iden, check_parent=False)
            #if there is not a var with the same name in the same scope then it would make a function that returns "null" in the same scope
            if not result:
                self.semantic_messages.add_message({"message": f"Function: '{function_iden}' not defined", "lineno": node.iden.lineno})
                new_declared_func_for_error_handling = FunctionSymbol(function_iden, "null",[])
                table.put(new_declared_func_for_error_handling)

            #if there is a var in the same scope with this name, return it's type
            else:
                self.semantic_messages.add_message({"message": f"'{function_iden}' is not a function", "lineno": node.iden.lineno})
                return result.type


    def visit_Expr8(self, node, table):
        #print(f"visiting: expr8")pr
        return self.visit(node.num, table)


    def visit_Expr9(self, node, table):
        #print(f"visiting: expr6")
        return self.visit(node.str, table)

    # No need to traverse flist, It is done in function definition in preprocess


    def visit_Clist1(self, node, table):
        #print(f"visiting: clist1")
        return "null"


    def visit_Clist2(self, node, table):
        #print(f"visiting: clist2")
        return self.visit(node.expr, table)
        

    def visit_Clist3(self, node, table):
        #print(f"visiting: clist3")
        self.visit(node.clist, table)
        return self.visit(node.expr, table)


    def visit_Type(self, node, table):
        #print(f"visiting: type")
        type = node.type_value
        return type


    def visit_Num(self, node, table):
        #print(f"visiting: num")
        return "int" 


    def visit_Iden(self, node, table):
        #print(f"visiting: iden")
        name = node.iden_value
        symbol = table.get(name)
        if not symbol:
            # self.semantic_messages.add_message({"message": f"'{name}' is not declared", "lineno":node.lineno,  'is_warning': True})
            # new_declared_variable_for_error_handling = FunctionSymbol(name, "null", [])
            # table.put(new_declared_variable_for_error_handling)
            # return "null"
            return None
        return symbol.type

    def visit_Empty(self, node, table):
        #print(f"visiting: empty")
        return "empty_rule"




    def find_symbol_table(self, name, parent):
        # print(parent)
        for i in range(len(parent.children)):
            if parent.children[i].name == name:
                return parent.children[i]


    def get_parameters(self, function_symbol):
        parameters = []
        for parameter in function_symbol.parameters:
            try:
                parameter = parameter["type"].type_value
            except:
                parameter =  parameter["type"] # this is for builtin functions
            parameters.append(parameter)
        parameters.reverse()
        return parameters


    def get_arguments(self, node, table):
        #get arguments
        arguments = []
        clist = node.clist
        if isinstance(clist, LexToken):
            return arguments
        if not isinstance(clist, AST.Empty):
            if clist.expr:
                res = self.visit(clist, table)
                if not isinstance(res, str) and res:
                    res = res.type_value
                arguments.append(res)
                while hasattr(clist, "clist"):
                    clist = clist.clist
                    if (not isinstance(clist, AST.Empty)):
                        res = self.visit(clist, table)
                        if not isinstance(res, str):
                            res = res.type_value
                        arguments.append(res)
        return arguments