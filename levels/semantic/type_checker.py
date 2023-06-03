from utils.symbol_table import *
import utils.ast as ast
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
        # print(node.expr2)
        # print(expr2_type)
        for_block_symbol_table = self.find_symbol_table(f"for_block_{node.lineno}", table) # symbol table for "for" block

        # setattr(node, "type", expr2_type)

        iden_symbol = "int"

        if iden_symbol != expr1_type['type']:
                self.semantic_messages.add_message({"message": f"Two sides of '=' must be 'int'! expr1 is of type: '{iden_symbol}' and expr2 is of type: '{expr1_type['type']}'", "lineno":node.expr1.lineno})
        elif iden_symbol != expr2_type['values_type']:
                self.semantic_messages.add_message({"message": f"expr2 is not vector of int", "lineno":node.expr2.lineno})

        self.visit(node.stmt, for_block_symbol_table)



    def visit_Stmt6(self, node, table):
        #print(f"visiting: stmt6")
        expr = self.visit(node.expr, table)
        # print(node.expr)
        # print(expr)
        #finding function name
        # print("expr : ", expr)
        function_name = []
        while not "_function_body_block_table" in table.name and table:
            table = table.parent
            #print("checked", table.name)
        #found the function name
        # print(table)
        if table:
            function_name = table.name.split("_function_body_block_table")[0]
            function_symbol = table.get(function_name)
            # print(config.global_symbol_table)
            function_type = function_symbol.type.split(" ")
            if "vector" in function_type:
                if expr["type"] != function_type[0]:
                    self.semantic_messages.add_message({"message": f"Returning wrong type for function '{function_name}'. must return: '{function_type[0]}<{function_type[1]}>', you're returning: '{expr['type']}'", "lineno":node.expr.lineno})
                elif expr["values_type"] != function_type[1]:
                    self.semantic_messages.add_message({"message": f"Returning wrong type for function '{function_name}'. must return: '{function_type[0]}<{function_type[1]}>', you're returning: '{expr['type']}<{expr['values_type']}>'", "lineno":node.expr.lineno})

            elif expr["type"] != function_type[0]:
                    self.semantic_messages.add_message({"message": f"Returning wrong type for function '{function_name}'. must return: '{function_type[0]}', you're returning: '{expr['type']}'", "lineno":node.expr.lineno})
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
        # print(table)
        name = node.iden.iden_value
        if isinstance(node.type, LexToken):
            type = "null"
        else:
            type = node.type.type_value
        if type != "vector":
            if isinstance(node.vector_type_choice, ast.Empty):
                if not table.put(VariableSymbol(name, type)):
                        self.semantic_messages.add_message({"message": f"'{name}' already defined", "lineno":node.iden.lineno})
        
                expr_type = self.visit(node.defvar_choice, table)
                # print(expr_type)
                if expr_type != "empty_rule":
                    if type != expr_type:
                        self.semantic_messages.add_message({"message": f"Two sides of '=' must be of same type! identifier is of type: '{type}' and experssions is of type: '{expr_type}'", "lineno":node.defvar_choice.lineno})
            else:
                self.semantic_messages.add_message({"message": "The type definition must be one of these: null, int, string, vector<int>, vector<string>", "lineno":node.vector_type_choice.lineno})

        else:
            if not isinstance(node.vector_type_choice, ast.Empty):
                if not isinstance(node.vector_type_choice.type, LexToken):
                    vector_type = node.vector_type_choice.type.type_value
                    expr = self.visit(node.defvar_choice, table)
                    if expr != "empty_rule":
                        if expr["type"] == "vector":
                            # print("AAAAAAAAAAAAAAA")
                            if expr["arguments"] == "not_same":
                                self.semantic_messages.add_message({"message": f"All vector values must be of type: {vector_type} But the types are different here : {expr['arguments']}", "lineno":node.vector_type_choice.lineno})
                                return
                            
                            if expr["arguments"] == "empty":
                                if not table.put(VectorSymbol(name, vector_type)):
                                    self.semantic_messages.add_message({"message": f"'{name}' already defined", "lineno":node.iden.lineno})
                                return
                            
                            if expr["arguments"] == "items_is_null":
                                self.semantic_messages.add_message({"message": f"vector values must be one of 'int', 'string'", "lineno":node.iden.lineno})
                                return

                            if vector_type != expr["arguments"][0]:
                                self.semantic_messages.add_message({"message": f"All vector values must be of type: '{vector_type}' But the types are different here : {expr['arguments']}", "lineno":node.vector_type_choice.lineno})
                                return
                            # print("AAAAAAAA")
                            if not table.put(VectorSymbol(name, vector_type, len(expr["arguments"]))):
                                self.semantic_messages.add_message({"message": f"'{name}' already defined", "lineno":node.iden.lineno})
                            # print(table)
                    else:
                        if not table.put(VectorSymbol(name, vector_type)):
                                self.semantic_messages.add_message({"message": f"'{name}' already defined", "lineno":node.iden.lineno})
                        # self.semantic_messages.add_message({"message": f"Two sides of '=' must be of same type! identifier is of type: 'vector<{vector_type}>' and experssions is of type: '{expr['arguments'][0]}'", "lineno":node.iden.lineno})
                        # return
            else:
                self.semantic_messages.add_message({"message": "The type definition must be one of these: null, int, string, vector<int>, vector<string>", "lineno":node.vector_type_choice.lineno})


    def visit_DefvarChoice2(self, node, table):
        return self.visit(node.expr, table)
            
    
    def visit_Expr1(self, node, table):
        # calling an vector
        #print(f"visiting: expr2")
        vector_iden = self.visit(node.expr1, table)
        # print("vector_iden : ", vector_iden)
        # print("node_expr : ", node.expr1)
        vector_index = self.visit(node.expr2, table)
        # print(node.expr2)
        if vector_iden["type"] == "vector" and vector_index["type"] == "int":
            return {"type": vector_iden["values_type"], "values_type": vector_iden["values_type"]}
        else:
            #print(vector_iden, vector_index)
            self.semantic_messages.add_message({"message": f"Identifier type must be 'vector'!", "lineno": node.expr1.lineno})
            
            if vector_index["type"] != "int":
                self.semantic_messages.add_message({"message": f'{node.expr2.lineno}: index of the vector must be of type \'int\'!', "lineno": node.expr2.lineno})
            
            # elif not 0 < vector_index["num_value"] < vector_iden.size:
            #     self.semantic_messages.add_message({"message": f"Index out of range, vector size is {vector_iden.size}", "lineno": node.expr2.lineno})

            return {"type": "null", "values_type": "null"}


    def visit_Expr2(self, node, table):
        # creating an vector

        arguments = self.get_arguments(node, table)
        seen = set()
        duplicates = set(x for x in arguments if x in seen or seen.add(x))
        
        if len(duplicates) > 1:
            return {"type": "vector", "arguments": "not_same"}
        elif len(duplicates) == 0:
            return {"type": "vector", "arguments": "empty"}
        elif arguments[0] == "null":
            return {"type": "vector", "arguments": "items_is_null", "values_type": arguments[0]}
        elif arguments[0] == "int" or arguments[0] == "string":
            return {"type": "vector", "arguments": arguments, "values_type": arguments[0]}


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
        print(f"first: {first_operand} node: {node.expr1}")
        second_operand = self.visit(node.expr2, table)
        # print(f"second: {second_operand} node: {node.expr2}")

        operator = node.oper
        #print(f'first operand type is {first_operand} and second is {second_operand} , operand: {operator}')


        #check if it's like id = expr
        first_operand_is_iden = isinstance(node.expr1, ast.Expr6)

        #dynamic type error handling! null type can be converted to Int or vector!
        #if operator is "=", assignment and first operand is a iden of type "null" you can assign anything to it
        if operator == "=" and first_operand["type"] == "null" and second_operand["type"] !="null" and first_operand_is_iden:
            first_operand_name = node.expr1.iden.iden_value
            first_operand_symbol = table.get(first_operand_name)
            first_operand_symbol.type = second_operand["type"]
            first_operand = second_operand
            return second_operand

        if first_operand["type"] != second_operand["type"]:
            self.semantic_messages.add_message({"message": f"Two sides of '{operator}' must be of same type! expr1 is of type: '{first_operand['type']}' and expr2 is of type: '{second_operand['type']}'", "lineno":node.expr1.lineno})
            return {"type": "null", "values_type": "null"}
        #print(f'first operand type is {first_operand} and second is {second_operand}')
        # table.get
        if first_operand["type"] == "vector" and "arguments" in second_operand:
            vector_symbol = table.get(node.expr1.iden.iden_value)
            vector_symbol.size = len(second_operand['arguments'])
        return first_operand
    


    def visit_Expr5(self, node, table):
        #print(f"visiting: expr5")
        #operator
        operand = self.visit(node.expr, table)
        # print(operand)
        operator = node.oper
        if operand['type'] == "int" :
            return operand
        elif operand['type'] == "null" and operator == "!":
            return {"type": "int", "values_type": "int"}
        else:
            self.semantic_messages.add_message({"message": f"The operand of the '{operator}' must be of type 'int'", "lineno":node.expr.lineno})
            return {"type": "null", "values_type": "null"}


    def visit_Expr6(self, node, table):
        #print(f"visiting: expr7")
        #search in table for the iden of this var, if not found, returns None
        iden_type = self.visit(node.iden, table)
        # print(f"iden_type: {iden_type}")
        if not iden_type:
            self.semantic_messages.add_message({"message": f"Variable '{node.iden.iden_value}' is not defined", "lineno":node.iden.lineno})
            
            # for error handling we should create that var
            # new_declared_symbol_for_error_handling = VariableSymbol(node.iden.iden_value, "null")
            # table.put(new_declared_symbol_for_error_handling)
            return {"type": "null", "values_type": "null"}
        
        return iden_type


    def visit_Expr7(self, node, table):
        #function call
        #print(f"visiting: expr1")
        function_iden = node.iden.iden_value
        # if function_iden == "find":
        #     print("heree")
        function_symbol = table.get(function_iden)
        # print(function_iden)
        # print(function_symbol)
        # print(table)
        # print()
        #check if function exists with this id
        # if not found, it's type automatically(in get function) is set to None
        if isinstance(function_symbol, FunctionSymbol):
            # get parameters
            parameters = self.get_parameters(function_symbol)
            # print(function_symbol)
            # print(parameters)
            # get arguments
            arguments = self.get_arguments(node, table)
            
            #print(f"{node.clist.lineno}: function: {function_iden}, arguments: {arguments}, parameters: {parameters}")
            # check number of arguments with number of parameters 
            if len(parameters) != len(arguments):
                # handle semantic error
                    self.semantic_messages.add_message({"message": f"Function '{function_iden}' expected {len(parameters)} arguments but got {len(arguments)} instead", "lineno": node.clist.lineno})
                    if "vector" in function_symbol.type:
                        return {"type": "vector", "values_type": function_symbol.type.split(" ")[1]}
                    else:    
                        return {"type": function_symbol.type, "values_type": function_symbol.type}

            # check arguments types with parameters types
            for i in range(len(function_symbol.parameters)):
                par_type = parameters[i]
                arg_type = arguments[i]
                if par_type != arg_type:
                    # handle semantic error
                    self.semantic_messages.add_message({"message": f"{i+1}th argument of function '{function_iden}' type must be '{par_type}'", "lineno":node.clist.lineno})
                    if "vector" in function_symbol.type:
                        return {"type": "vector", "values_type": function_symbol.type.split(" ")[1]}
                    else:    
                        return {"type": function_symbol.type, "values_type": function_symbol.type}

            # if number of arguments and their types where correct, return function iden's type
            if "vector" in function_symbol.type:
                return {"type": "vector", "values_type": function_symbol.type.split(" ")[1]}
            else:    
                return {"type": function_symbol.type, "values_type": function_symbol.type}

        

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
                return {"type": result.type, "values_type": result.type}


    def visit_Expr8(self, node, table):
        #print(f"visiting: expr8")pr
        return self.visit(node.num, table)


    def visit_Expr9(self, node, table):
        #print(f"visiting: expr6")
        return self.visit(node.str, table)

    # No need to traverse flist, It is done in function definition in preprocess


    def visit_Clist1(self, node, table):
        #print(f"visiting: clist1")
        return {"type": "null", "values_type": "null"}


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
        pass

    
    def visit_Iden(self, node, table):
        #print(f"visiting: iden")
        name = node.iden_value
        symbol = table.get(name)
        # print("symbol : ", symbol)
        if not symbol:
            # self.semantic_messages.add_message({"message": f"'{name}' is not declared", "lineno":node.lineno,  'is_warning': True})
            # new_declared_variable_for_error_handling = FunctionSymbol(name, "null", [])
            # table.put(new_declared_variable_for_error_handling)
            # return "null"
            return None
        if symbol.__class__.__name__ == "VectorSymbol":
            return {"type": "vector", "values_type": symbol.type, "size": symbol.size}
        elif symbol.__class__.__name__ == "VariableSymbol":
            return {"type": symbol.type, "values_type": symbol.type}
    

    def visit_Str(self, node, table):
        #print(f"visiting: str")
        return {"type": "string", "values_type": "string"}
    
    
    def visit_Num(self, node, table):
        #print(f"visiting: num")
        return {"type": "int", "values_type": "int", "num_value": node.num_value}


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
                # if "vector" in parameter["type"]:
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
        if not isinstance(clist, ast.Empty):
            if clist.expr:
                res = self.visit(clist, table)
                if not isinstance(res, str) and res:
                    res = res["type"]
                arguments.append(res)
                while hasattr(clist, "clist"):
                    clist = clist.clist
                    if (not isinstance(clist, ast.Empty)):
                        res = self.visit(clist, table)
                        if not isinstance(res, str):
                            res = res["type"]
                        arguments.append(res)
        return arguments