from utils.symbol_table import *
import utils.ast as ast
from utils.node_visitor import NodeVisitor
from ply.lex import LexToken
import config


class TypeChecker(NodeVisitor):
    # This class is a subclass of NodeVisitor and is used for type checking.

    def __init__(self, semantic_messages):
        # Constructor that initializes the TypeChecker object.
        # It takes in a parameter 'semantic_messages' which stores the messages related to semantic errors.
        self.semantic_messages = semantic_messages

    def visit_Prog1(self, node, table):
        
        pass
        # The visit_Prog1 method is called when visiting a Prog1 node.
        # It does nothing and is left empty.

    def visit_Prog2(self, node, table):
        # The visit_Prog2 method is called when visiting a Prog2 node.
        # It visits the 'func' and 'prog' nodes using the global symbol table as the argument.
        self.visit(node.func, config.global_symbol_table)
        self.visit(node.prog, config.global_symbol_table)

    def visit_Func(self, node, table):
        # The visit_Func method is called when visiting a Func node.
        
        # Retrieves the function symbol from the symbol table using the identifier value.
        function_symbol = table.get(node.iden.iden_value)
        
        # Determines the function name based on the retrieved function symbol.
        function_name = function_symbol.name
        
        # Finds the symbol table for the function body block using the function name and the parent symbol table.
        function_body_block = self.find_symbol_table(
            f"{function_name}_function_body_block_table", table)
        
        # Visits the 'func_choice' node using the function body block symbol table as the argument.
        self.visit(node.func_choice, function_body_block)
    
    def visit_FuncChoice1(self, node, table):
        # The visit_FuncChoice1 method is called when visiting a FuncChoice1 node.
        # It visits the 'body' node using the given symbol table as the argument.
        self.visit(node.body, table)

    def visit_FuncChoice2(self, node, table):
        pass
        # The visit_FuncChoice2 method is called when visiting a FuncChoice2 node.
        # It does nothing and is left empty.

    def visit_Body1(self, node, table):
        # The visit_Body1 method is called when visiting a Body1 node.
        # It visits the 'stmt' node using the given symbol table as the argument.
        self.visit(node.stmt, table)

    def visit_Body2(self, node, table):
        # The visit_Body2 method is called when visiting a Body2 node.
        # It visits the 'stmt' and 'body' nodes using the given symbol table as the argument.
        self.visit(node.stmt, table)
        self.visit(node.body, table)


    def visit_Stmt1(self, node, table):
        # The visit_Stmt1 method is called when visiting a Stmt1 node.
        # It visits the 'expr' node using the given symbol table as the argument.
        self.visit(node.expr, table)
    
    def visit_Stmt2(self, node, table):
        # The visit_Stmt2 method is called when visiting a Stmt2 node.
        # It visits the 'defvar' node using the given symbol table as the argument.
        self.visit(node.defvar, table)
    
    def visit_Stmt3(self, node, table):
        # The visit_Stmt3 method is called when visiting a Stmt3 node.
        
        # Visits the 'expr' node using the given symbol table as the argument.
        self.visit(node.expr, table)
        
        # Finds the symbol table for the if block and visits the 'stmt' and 'else_choice' nodes using the if block symbol table as the argument.
        if_block_symbol_table = self.find_symbol_table(
            f"if_block_{node.lineno}", table)
        self.visit(node.stmt, if_block_symbol_table)
        self.visit(node.else_choice, table)
    
    def visit_ElseChoice2(self, node, table):
        # The visit_ElseChoice2 method is called when visiting an ElseChoice2 node.
        
        # Finds the symbol table for the else block and visits the 'stmt' node using the else block symbol table as the argument.
        else_block_symbol_table = self.find_symbol_table(
            f"else_block_{node.lineno}", table)
        self.visit(node.stmt, else_block_symbol_table)
    
    def visit_Stmt4(self, node, table):
        # The visit_Stmt4 method is called when visiting a Stmt4 node.
        
        # Visits the 'expr' node using the given symbol table as the argument.
        self.visit(node.expr, table)
        
        # Finds the symbol table for the while block and visits the 'stmt' node using the while block symbol table as the argument.
        while_block_symbol_table = self.find_symbol_table(
            f"while_block_{node.lineno}", table)
        self.visit(node.stmt, while_block_symbol_table)
    
    
    def visit_Stmt5(self, node, table):
        # The visit_Stmt5 method is called when visiting a Stmt5 node.
        # It visits the 'expr1' and 'expr2' nodes using the given symbol table as the argument.
        expr1_type = self.visit(node.expr1, table)
        expr2_type = self.visit(node.expr2, table)
    
        # It finds the symbol table for the for block and sets the identifier symbol to "int".
        for_block_symbol_table = self.find_symbol_table(
            f"for_block_{node.lineno}", table)
        iden_symbol = "int"
    
        # It checks if the types of expr1 and expr2 match the iden_symbol
        # and adds the appropriate semantic message if they don't match.
        if iden_symbol != expr1_type['type']:
            self.semantic_messages.add_message(
                {"message": f"Two sides of '=' must be 'int'! {expr1_type['id_value']} is '{iden_symbol}' and {expr2_type['id_value']} is '{expr2_type['type']}'", "lineno": node.expr1.lineno})
        elif iden_symbol != expr2_type['type']:
            self.semantic_messages.add_message(
                {"message": f"Type {expr2_type['id_value']} must be int", "lineno": node.expr2.lineno})
    
        # It then visits the 'stmt' node using the for block symbol table as the argument.
        self.visit(node.stmt, for_block_symbol_table)
    

    def visit_Stmt6(self, node, table):
        # Visits the 'expr' node using the given symbol table as the argument.
        expr = self.visit(node.expr, table)
        
        # Finding function name
        function_name = []
        while not "_function_body_block_table" in table.name and table:
            table = table.parent
        
        # Found the function name
        if table:
            function_name = table.name.split("_function_body_block_table")[0]
            function_symbol = table.get(function_name)
            
            # Extracting function type
            function_type = function_symbol.type.split(" ")
            
            if "vector" in function_type:
                # Checking if the returned type matches the expected type for a vector function
                if expr["type"] != function_type[0]:
                    self.semantic_messages.add_message(
                        {"message": f"Returning wrong type for function '{function_name}'. must return : '{function_type[0]}<{function_type[1]}>', you're returning : '{expr['type']}'", "lineno": node.expr.lineno})
                elif expr["values_type"] != function_type[1]:
                    self.semantic_messages.add_message(
                        {"message": f"Returning wrong type for function '{function_name}'. must return : '{function_type[0]}<{function_type[1]}>', you're returning : '{expr['type']}<{expr['values_type']}>'", "lineno": node.expr.lineno})
            else:
                # Checking if the returned type matches the expected type for a normal function
                if expr["type"] != function_type[0]:
                    self.semantic_messages.add_message(
                        {"message": f"Returning wrong type for function '{function_name}'. must return : '{function_type[0]}', you're returning : '{expr['type']}'", "lineno": node.expr.lineno})
        else:
            # Didn't find the corresponding function to this return
            self.semantic_messages.add_message(
                {"message": f"Shouldn't have put return here!", "lineno": node.expr.lineno})
    
    def visit_Stmt7(self, node, table):
        # Finds the symbol table for the body block and visits the 'body' node using the body block symbol table as the argument.
        body_block_symbol_table = self.find_symbol_table(
            f"body_block_{node.lineno}", table)
        self.visit(node.body, body_block_symbol_table)
    
    def visit_Stmt8(self, node, table):
        # Visits the 'func' node using the given symbol table as the argument.
        self.visit(node.func, table)
    

    def visit_Defvar(self, node, table):
        # Extracts the name and type of the variable from the Defvar node.
        name = node.iden.iden_value
        type = node.type.type_value
        
        # Checks if the variable name already exists in the symbol table.
        if not table.is_exist(name):
            
            # Handles the case when the type is "vector".
            if type == "vector":
                
                # Visits the DefvarChoice node to get the expression for the vector variable.
                expr = self.visit(node.defvar_choice, table)
                vector_type = node.type.vector_type_value
                
                # Checks if the expression is an empty rule.
                if expr == "empty_rule":
                    
                    # Adds a VectorSymbol with the name and vector type to the symbol table.
                    table.put(VectorSymbol(name, vector_type))
                else:
                    # Handles the case when the expression is a vector.
                    if expr["type"] == "vector":
                        error = False
    
                        if expr["arguments"] == "not_same":
                            # Adds a semantic message indicating that all vector values must have the same type.
                            self.semantic_messages.add_message({"message": f"All vector values must be {vector_type}, But the types are different here : {expr['arguments']}", "lineno": node.vector_type_choice.lineno})
                            error = True
                        if expr["arguments"] == "empty":
                            # Adds a semantic message indicating that the vector must have at least one element.
                            self.semantic_messages.add_message({"message": f"The vector must have at least one element", "lineno": node.iden.lineno})
                            error = True
                        if expr["arguments"] == "items_is_null":
                            # Adds a semantic message indicating that vector values must be either 'int' or 'str'.
                            self.semantic_messages.add_message({"message": f"vector values must be one of 'int', 'str'", "lineno": node.iden.lineno})
                            error = True
                        if vector_type != expr["arguments"][0]:
                            # Adds a semantic message indicating that all vector values must have the same type.
                            self.semantic_messages.add_message({"message": f"All vector values must be '{vector_type}', But the types are different here : {expr['arguments']}", "lineno": node.vector_type_choice.lineno})
                            error = True
    
                        if not error:
                            # Adds a VectorSymbol with the name, vector type, and length of the vector to the symbol table.
                            table.put(VectorSymbol(name, vector_type, len(expr["arguments"])))
                        else:
                            # Adds a VariableSymbol with the name and value "null" to the symbol table.
                            table.put(VariableSymbol(name, "null"))
                    else:
                        # Adds a semantic message indicating that both sides of '=' must be of the same type.
                        self.semantic_messages.add_message({"message": f"Two sides of '=' must be of same type! identifier is 'vector<{vector_type}>' and expression is '{expr['type']}'", "lineno": node.defvar_choice.lineno})
    
            else:
                # Adds a VariableSymbol with the name and type to the symbol table.
                table.put(VariableSymbol(name, type))
                
                # Visits the DefvarChoice node with the symbol table.
                expr = self.visit(node.defvar_choice, table)
                
                # Checks if the expression is not an empty rule.
                if expr != "empty_rule":
                    # Checks if the type of the variable is different from the type of the expression.
                    self.semantic_messages.add_message({"message": f"Two sides of '=' must be of same type! identifier is '{type}' and expression is '{expr['type']}'", "lineno": node.defvar_choice.lineno})
        else:
            # Adds a semantic message indicating that the variable name is already defined.
            self.semantic_messages.add_message({"message": f"'{name}' already defined", "lineno": node.iden.lineno})
    
    def visit_DefvarChoice2(self, node, table):
        # Visits the expression node with the symbol table.
        return self.visit(node.expr, table)
    

    def visit_Expr1(self, node, table):
        # Visits the expression nodes to get the vector identifier and index.
        vector_iden = self.visit(node.expr1, table)
        vector_index = self.visit(node.expr2, table)
        
        # Checks if the type of the vector identifier is "vector" and the type of the index is "int".
        if vector_iden["type"] == "vector" and vector_index["type"] == "int":
            if vector_index["type"] == "int":
                # Returns a dictionary containing the vector identifier, type, and values type.
                return {"id_value" : vector_iden["id_value"],"type": vector_iden["values_type"], "values_type": vector_iden["values_type"]}
            else:
                # Adds a semantic message indicating that the index of the vector must be 'int'.
                self.semantic_messages.add_message({"message": f'{node.expr2.lineno}: index of the vector must be \'int\'!', "lineno": node.expr2.lineno})
                return {"id_value": vector_iden["id_value"], "type": "null", "values_type": "null"}
    
        else:
            # Adds a semantic message indicating that the identifier type must be 'vector'.
            self.semantic_messages.add_message({"message": f"Identifier type must be 'vector'!", "lineno": node.expr1.lineno})
            return {"id_value" : vector_iden["id_value"], "type": "null", "values_type": "null"}
    
    def visit_Expr2(self, node, table):
        # Gets the arguments and identifier value from the node.
        arguments, id_value = self.get_arguments(node, table)
        
        # Finds duplicate arguments.
        seen = set()
        duplicates = set(x for x in arguments if x in seen or seen.add(x))
    
        if len(duplicates) > 1:
            # Returns a dictionary indicating that the arguments are not all the same.
            return {"id_value": id_value, "type": "vector", "arguments": "not_same"}
        elif len(duplicates) == 0:
            # Returns a dictionary indicating that the vector has no elements.
            return {"id_value": id_value, "type": "vector", "arguments": "empty"}
        elif arguments[0] == "null":
            # Returns a dictionary indicating that the items of the vector are null.
            return {"id_value": id_value, "type": "vector", "arguments": "items_is_null", "values_type": arguments[0]}
        elif arguments[0] == "int" or arguments[0] == "str":
            # Returns a dictionary containing the identifier value, type, arguments, and values type.
            return {"id_value": id_value, "type": "vector", "arguments": arguments, "values_type": arguments[0]}
    

    # This function visits an Expr3 node in an abstract syntax tree.
    def visit_Expr3(self, node, table):
        # Visit the first expression of the Expr3 node and store the result in condition_expr.
        condition_expr = self.visit(node.expr1, table)
        
        # Visit the second expression of the Expr3 node and store the result in true_block_expr.
        true_block_expr = self.visit(node.expr2, table)
        
        # Visit the third expression of the Expr3 node and store the result in false_block_expr.
        false_block_expr = self.visit(node.expr3, table)
        
        # Check if the type of the condition expression is "null".
        if condition_expr["type"] == "null":
            # If the condition expression is null, the condition would be false,
            # so return the false block expression.
            return false_block_expr
        
        # If the condition expression is not null, the condition is true,
        # so return the true block expression.
        return true_block_expr
    

    # This function visits an Expr4 node in an abstract syntax tree.
    def visit_Expr4(self, node, table):
        # Visit the first operand expression of the Expr4 node and store the result in first_operand.
        first_operand = self.visit(node.expr1, table)
        
        # Visit the second operand expression of the Expr4 node and store the result in second_operand.
        second_operand = self.visit(node.expr2, table)
        
        # Get the operator from the Expr4 node.
        operator = node.oper
        
        # Create a string representing the id value with the operator between the first and second operands.
        id_value = f"{first_operand['id_value']} {operator} {second_operand['id_value']}"
        
        # Check if the types of the first and second operands are not equal.
        if first_operand["type"] != second_operand["type"]:
            # If they are not equal, set the expected type as the type of the second operand.
            expected = second_operand["type"]
            
            # If the second operand is a vector, update the expected type to include the values_type.
            if second_operand["type"] == "vector":
                expected = f"{second_operand['type']}<{second_operand['values_type']}>"
            
            # Add a semantic message to indicate that the two sides of the operator must be of the same type.
            # Include information about the mismatched types and their corresponding values.
            self.semantic_messages.add_message({"message": f"Two sides of '{operator}' must be of same type! '{first_operand['id_value']}' is '{first_operand['type']}' and '{second_operand['id_value']}' is '{expected}'", "lineno": node.expr1.lineno})
            
            # Set the id_value to null and return a dictionary with id_value, type, and values_type as null.
            id_value = f"{first_operand['id_value']} {operator} {second_operand['id_value']}"
            return {"id_value": id_value, "type": "null", "values_type": "null"}
        
        # If the types of the first and second operands are equal, continue with the code execution.
        # table.get
        if first_operand["type"] == "vector" and "arguments" in second_operand:
            # If the first operand is a vector and the second operand has arguments (indicating indexing), update the size of the vector symbol in the table.
            vector_symbol = table.get(node.expr1.iden.iden_value)
            vector_symbol.size = len(second_operand['arguments'])
        
        # Return the value of the first operand.
        return first_operand
    

    # This function visits an Expr5 node in an abstract syntax tree.
    def visit_Expr5(self, node, table):
        # Visit the expression node of the Expr5 node and store the result in operand.
        operand = self.visit(node.expr, table)
        
        # Get the operator from the Expr5 node.
        operator = node.oper
        
        # Check if the type of the operand is "int".
        if operand['type'] == "int":
            # If it is, return the operand as it is.
            return operand
        
        # Check if the type of the operand is "null" and the operator is "!". 
        elif operand['type'] == "null" and operator == "!":
            # If it is, create a new dictionary with id_value set to the operand's "operand" value, type set to "int", and values_type set to "int".
            return {"id_value": operand["operand"], "type": "int", "values_type": "int"}
        
        else:
            # If none of the above conditions are met, add a semantic message indicating that the operand of the operator must be 'int'.
            self.semantic_messages.add_message({"message": f"The operand of the '{operator}' must be 'int'", "lineno": node.expr.lineno})
            
            # Create a new dictionary with id_value set to the operand's "operand" value, type set to "null", and values_type set to "null".
            return {"id_value": operand["operand"], "type": "null", "values_type": "null"}
    
    # This function visits an Expr6 node in an abstract syntax tree.
    def visit_Expr6(self, node, table):
        # Visit the iden node of the Expr6 node and get the type information from the visitation.
        iden_type = self.visit(node.iden, table)
        
        # Check if the "type" value in the iden_type dictionary is empty.
        if not iden_type["type"]:
            # If it is empty, add a semantic message indicating that the variable is not defined and set the id_value, type, and values_type to null.
            self.semantic_messages.add_message({"message": f"Variable '{node.iden.iden_value}' is not defined", "lineno": node.iden.lineno})
            
            # Create a new VariableSymbol with the iden value and type as "null" for error handling purposes.
            new_declared_symbol_for_error_handling = VariableSymbol(node.iden.iden_value, "null")
            table.put(new_declared_symbol_for_error_handling)
            
            # Return a dictionary with the id_value, type, and values_type set to null.
            return {"id_value": iden_type["id_value"], "type": "null", "values_type": "null"}
    
        # If the "type" value in the iden_type dictionary is not empty, return the iden_type as it is.
        return iden_type
    

    def visit_Expr7(self, node, table):
        # Retrieve the identifier value of the function
        function_iden = node.iden.iden_value
        
        # Look up the function symbol in the table
        function_symbol = table.get(function_iden)
        
        # Check if the function symbol is an instance of FunctionSymbol
        if isinstance(function_symbol, FunctionSymbol):
            # Retrieve the function's parameters and arguments
            parameters = self.get_parameters(function_symbol)
            arguments = self.get_arguments(node, table)[0]
            
            # Check if the number of parameters and arguments match
            if len(parameters) != len(arguments):
                self.semantic_messages.add_message(
                    {"message": f"Function '{function_iden}' expected {len(parameters)} arguments but got {len(arguments)} instead",
                    "lineno": node.clist.lineno})
                if "vector" in function_symbol.type:
                    return {"id_value": function_iden, "type": "vector", "values_type": function_symbol.type.split(" ")[1]}
                else:
                    return {"id_value": function_iden, "type": function_symbol.type, "values_type": function_symbol.type}
            
            # Compare each parameter type with the corresponding argument type
            for i in range(len(function_symbol.parameters)):
                par_type = parameters[i]
                arg_type = arguments[i]
                expected = ""
                if isinstance(par_type, list):
                    inconsistent = 0
                    for par in par_type:
                        if "vector" in par:
                            if arg_type != par:
                                inconsistent += 1
                                expected += f"'vector<{par.split(' ')[1]}>' or "
                        else:
                            if arg_type != par:
                                inconsistent += 1
                                expected += par
                    if inconsistent == len(par_type):
                        self.semantic_messages.add_message(
                            {"message": f"{i+1}th argument of function '{function_iden}' type must be {expected[:-4]}",
                            "lineno": node.clist.lineno})
                else:
                    if arg_type != par_type:
                        if "vector" in par_type:
                            expected += f"'vector<{par_type.split(' ')[1]}>'"
                        else:
                            expected += par_type
                        self.semantic_messages.add_message(
                            {"message": f"{i+1}th argument of function '{function_iden}' type must be {expected}",
                            "lineno": node.clist.lineno})
            
            # Return the function identifier and type information
            if "vector" in function_symbol.type:
                return {"id_value": function_iden, "type": "vector", "values_type": function_symbol.type.split(" ")[1]}
            else:
                return {"id_value": function_iden, "type": function_symbol.type, "values_type": function_symbol.type}
        
        else:
            # Handle the case where the function symbol is not a FunctionSymbol
            result = table.get(function_iden, check_parent=False)
            if not result:
                # Add an error message for undefined function
                self.semantic_messages.add_message(
                    {"message": f"Function: '{function_iden}' not defined", "lineno": node.iden.lineno})
                new_declared_func_for_error_handling = FunctionSymbol(
                    function_iden, "null", [])
                table.put(new_declared_func_for_error_handling)
            else:
                # Add an error message for symbol not being a function
                self.semantic_messages.add_message(
                    {"message": f"'{function_iden}' is not a function", "lineno": node.iden.lineno})
                return {"id_value": function_iden, "type": result.type, "values_type": result.type}


    # This method visits the Expr8 node and returns the result of visiting its num child node.
    def visit_Expr8(self, node, table):
        return self.visit(node.num, table)

    # This method visits the Expr9 node and returns the result of visiting its str child node.
    def visit_Expr9(self, node, table):
        return self.visit(node.str, table)

    # This comment states that there is no need to traverse flist, as it is already done in the function definition in preprocess.
    def visit_Clist1(self, node, table):
        pass

    # This method visits the Clist2 node and returns the result of visiting its expr child node.
    def visit_Clist2(self, node, table):
        return self.visit(node.expr, table)

    # This method visits the Clist3 node, first visits its clist child node, and then returns the result of visiting its expr child node.
    def visit_Clist3(self, node, table):
        self.visit(node.clist, table)
        return self.visit(node.expr, table)


    # Function to visit an identifier node
    def visit_Iden(self, node, table):
        # Get the name of the identifier
        name = node.iden_value
        
        # Retrieve the symbol from the symbol table using the name
        symbol = table.get(name)
        
        # If the symbol does not exist in the table, return a dictionary with the identifier value and None for the type
        if not symbol:
            return {"id_value": name, "type": None}
            
        # Check the class name of the symbol object
        if symbol.__class__.__name__ == "VectorSymbol":
            # If the symbol is of type VectorSymbol, return a dictionary with the identifier value, type as "vector",
            # values_type as the symbol's type, and size as the symbol's size
            return {"id_value": name, "type": "vector", "values_type": symbol.type, "size": symbol.size}
        elif symbol.__class__.__name__ == "VariableSymbol":
            # If the symbol is of type VariableSymbol, return a dictionary with the identifier value, type as the symbol's type,
            # and values_type as the symbol's type
            return {"id_value": name, "type": symbol.type, "values_type": symbol.type}
   

    # Function to visit a string node
    def visit_Str(self, node, table):
        # Return a dictionary with the string value of the node as the identifier value,
        # type as "str", and values_type as "str"
        return {"id_value": node.str_value,"type": "str", "values_type": "str"}
    
    # Function to visit a number node
    def visit_Num(self, node, table):
        # Return a dictionary with the number value of the node as the identifier value,
        # type as "int", and values_type as "int"
        return {"id_value": node.num_value, "type": "int", "values_type": "int"}
    
    # Function to visit an empty node
    def visit_Empty(self, node, table):
        # Return the string "empty_rule"
        return "empty_rule"
    
    # Function to find a symbol table based on its name within a parent scope
    def find_symbol_table(self, name, parent):
        # Iterate through the children of the parent scope
        for i in range(len(parent.children)):
            # Check if the name of the current child matches the desired name
            if parent.children[i].name == name:
                # Return the matching child symbol table
                return parent.children[i]
    
    # Function to get parameters from a function symbol
    def get_parameters(self, function_symbol):
        parameters = []
        # Iterate through the parameters of the given function symbol
        for parameter in function_symbol.parameters:
            try:
                # Try to access the "type" key in the parameter dictionary and append it as a list to the parameters list
                parameter = [parameter["type"].type_value]
            except:
                # If the "type" key does not exist or there is an exception, assign the parameter directly to itself
                parameter = parameter["type"]
            # Append the parameter to the parameters list
            parameters.append(parameter)
        # Reverse the order of the parameters list and return it
        parameters.reverse()
        return parameters
    

    # Function to get arguments from a node
    def get_arguments(self, node, table):
        # Initialize an empty list for arguments
        arguments = [[], []]

        # Get the clist from the node
        clist = node.clist

        # If clist is a LexToken, return the empty arguments list
        if isinstance(clist, LexToken):
            return arguments

        # Check if clist is not an Empty ast node
        if not isinstance(clist, ast.Empty):
            # Check if clist has an expr
            if clist.expr:
                # Visit the clist and get the result
                result = self.visit(clist, table)

                # Check if the result is not a string and is truthy
                if not isinstance(result, str) and result:
                    # Get the type of the argument
                    arg_type = result["type"]

                    # Check if the type is "vector" and append the values_type to arg_type
                    if result["type"] == "vector":
                        arg_type += f" {result['values_type']}"

                    # Append the type and id_value of the argument to arguments
                    arguments[0].append(arg_type)
                    arguments[1].append(result["id_value"])

                # Loop until clist does not have a clist attribute
                while hasattr(clist, "clist"):
                    clist = clist.clist

                    # Check if clist is not an Empty ast node
                    if (not isinstance(clist, ast.Empty)):
                        # Visit the clist and get the result
                        result = self.visit(clist, table)

                        # Check if the result is not a string
                        if not isinstance(result, str):
                            # Get the type of the argument
                            arg_type = result["type"]

                            # Check if the type is "vector" and append the values_type to arg_type
                            if result["type"] == "vector":
                                arg_type += f" {result['values_type']}"

                            # Append the type and id_value of the argument to arguments
                            arguments[0].append(arg_type)
                            arguments[1].append(result["id_value"])

        # Return the arguments list
        return arguments

