from utils.symbol_table import *
import utils.ast as AST
from utils.node_visitor import NodeVisitor
import config


class IRGenerator(NodeVisitor):

    def __init__(self):
        self.reginster_index = 0
        self.label_index = 0
        self.memory_allocated_registers = []
        self.create_and_push_builtin_funcs()
        config.max_register_index_used_in_code = 0

    def visit_Prog1(self, node, table):
        code = ""
        return code

    def visit_Prog2(self, node, table):
        func_code = self.visit(node.func, config.global_symbol_table)
        prog_code = self.visit(node.prog, config.global_symbol_table)
        func_name = node.func.iden.iden_value

        # The following if-else statement ensures that the "main" function always comes after all other functions.
        if func_name == "main":
            code = prog_code + "\n" + func_code
        else:
            code = func_code + "\n" + prog_code

        # Add used built-in functions
        self.builtin_funcs.reverse()

        # Iterate over the built-in functions list in reverse order
        for i in range(len(self.builtin_funcs)):

            # Check if the function was used but not yet included in the code
            if self.builtin_funcs[i]["used"] and not self.builtin_funcs[i]["included"]:
                code = f'''{self.builtin_funcs[i]["code"]}
    {code}'''

                # Mark the function as included to avoid duplication
                self.builtin_funcs[i]["included"] = True

        # Set the generated code as the new value of the iR_code variable in the config module
        config.iR_code = code
        return code

    def visit_Func(self, node, table):
        function_iden = node.iden.iden_value
        function_symbol = table.get(function_iden)
        function_iden = function_symbol.name

        # Find the symbol table for the function body block
        function_body_block = self.find_symbol_table(
            f"{function_iden}_function_body_block_table", table)

        # Get the parameters of the function
        parameters = self.get_parameters(node)

        # Reset the register index for variable symbol registration
        self.reginster_index = 0
        parameters_initiation_code = ""

        # Iterate over the parameters and initiate variable symbol registers
        for param in parameters:
            self.initiate_var_symbol_register(
                param["iden"].iden_value, function_body_block)

        # Visit the function choice (body) to generate code for it
        func_body_code = self.visit(node.func_choice, function_body_block)

        # Generate the overall code for the function
        code = f'''proc {function_iden}
    {func_body_code}'''

        return code

    def visit_FuncChoice1(self, node, table):
        # Visit the body of the function and generate code for it
        body_code = self.visit(node.body, table)
        return body_code

    def visit_FuncChoice2(self, node, table):
        # Visit the expression of the function and generate code for it
        body_code = self.visit(node.expr, table)
        return body_code

    def visit_Body1(self, node, table):
        # Initialize an empty string for the code
        code = ""
        return code

    def visit_Body2(self, node, table):
        # Visit the statement and body of the function
        stmt_code = self.visit(node.stmt, table)
        body_code = self.visit(node.body, table)

        if not stmt_code:
            # If there is no statement code, assign the body code to the code variable
            code = body_code
        else:
            # If there is a statement code, concatenate the statement code and body code with a line break in between
            code = f'''{stmt_code}{body_code}'''
        return code

    def visit_Stmt1(self, node, table):
        # Visit the expression of the statement and retrieve the result
        res = self.visit(node.expr, table)

        if res:
            # If the result is not empty (evaluates to True)
            # extract the code from the result dictionary
            expr_code = res["code"]
            code = expr_code
        else:
            # If the result is empty, assign an empty string to code
            code = ""

        return code

    def visit_Stmt2(self, node, table):
        # Visit the definition of a variable in the statement and generate code for it
        code = self.visit(node.defvar, table)
        return code

    def visit_Stmt3(self, node, table):
        # Visit the expression of the statement and retrieve the result
        res = self.visit(node.expr, table)
        expr_code = res["code"]
        expr_returned_reg = res["reg"]

        # Find the symbol table for the "if" block
        if_block_symbol_table = self.find_symbol_table(
            f"if_block_{node.lineno}", table)

        # Visit the statement inside the "if" block using the symbol table
        stmt_code = self.visit(node.stmt, if_block_symbol_table)

        label = ""
        label2 = ""
        else_choice_code = ""

        if not isinstance(node.else_choice, AST.Empty):
            # If there is an else choice, visit it and generate code
            else_choice_code = self.visit(node.else_choice, table)

            # Create labels for branching
            label = self.create_label()
            label2 = self.create_label()

            # Create the code block including conditions, jumps, and labels
            code = f'''{expr_code}
                        \tjz {expr_returned_reg}, {label}
                        {stmt_code}
                        \tjmp {label2}
                        {label}:
                        {else_choice_code}
                        {label2}:'''
        else:
            # If there is no else choice, create code block without the else segment
            label = self.create_label()
            code = f'''{expr_code}
                    \tjz {expr_returned_reg}, {label}
                    {stmt_code}
                    {label}:'''

        return code

    def visit_Else_choice1(self, node, table):
        code = ""
        return code

    def visit_Else_choice2(self, node, table):
        # Find the symbol table for the 'else' block using the line number of the node.
        else_block_symbol_table = self.find_symbol_table(
            f"else_block_{node.lineno}", table)

        # Visit the statement node within the 'else' block and get the generated code.
        stmt_code = self.visit(node.stmt, else_block_symbol_table)

        # Create a formatted string combining the code from the statement node.
        code = f'''{stmt_code}'''

        # Return the generated code.
        return code

    def visit_Stmt4(self, node, table):
        # Visit the expression node within the Stmt4 node and get the generated code and returned register.
        res = self.visit(node.expr, table)
        expr_code = res["code"]
        expr_returned_reg = res["reg"]

        # Find the symbol table for the 'do' block of a while loop using the line number of the node.
        while_block_symbol_table = self.find_symbol_table(
            f"while_block_{node.lineno}", table)

        # Visit the statement node within the 'do' block of the while loop and get the generated code.
        stmt_code = self.visit(node.stmt, while_block_symbol_table)

        # Create labels for jumping to and from the while loop condition.
        label = self.create_label()
        label2 = self.create_label()

        # Create a code combining the labels, expression code, statement code, and jumps.
        code = f'''
                {label}:
                {expr_code}
                \tjz {expr_returned_reg}, {label2}
                {stmt_code}
                \tjmp {label}
                {label2}:'''

        return code

    def visit_Stmt5(self, node, table):
        # Find the symbol table for the 'for' block using the line number of the node.
        for_block_symbol_table = self.find_symbol_table(
            f"for_block_{node.lineno}", table)

        # Extract the name of the variable from the Stmt5 node.
        name = node.iden.iden_value

        # Initialize the variable symbol register for the variable in the 'for' block symbol table.
        iden_reg = self.initiate_var_symbol_register(
            name, for_block_symbol_table)

        # Visit the first expression node within the Stmt5 node and get the generated code and returned register.
        res = self.visit(node.expr1, table)
        expr_code = res["code"]
        expr_returned_reg = res["reg"]

        # Visit the second expression node within the Stmt5 node and get the generated code and returned register.
        res2 = self.visit(node.expr2, table)
        expr_code2 = res2["code"]
        expr_returned_reg2 = res2["reg"]

        # Visit the statement node within the 'for' block and get the generated code.
        stmt_code = self.visit(node.stmt, for_block_symbol_table)

        # Create temporary registers and labels for use in the generated code.
        tmp_reg = self.create_register()
        tmp_reg2 = self.create_register()
        label = self.create_label()
        label2 = self.create_label()

        # Create a code combining the expression codes, comparison, jumps, and statement code.
        code = f'''{expr_code}
                {expr_code2}
                \tmov {iden_reg}, {expr_returned_reg}
                {label}:
                \tcmp< {tmp_reg}, {iden_reg}, {expr_returned_reg2}
                \tjz {tmp_reg}, {label2}
                {stmt_code} 
                \tmov {tmp_reg2}, 1
                \tadd {iden_reg}, {tmp_reg2}, {iden_reg}
                \tjmp {label}
                {label2}:'''

        return code

    def visit_Stmt6(self, node, table):
        res = self.visit(node.expr, table)
        expr_code = res["code"]
        expr_returned_reg = res["reg"]

        # if we're returning from main function, we have to release all allocated vector registers
        if table.name == "main_function_body_block_table":
            code = f'''{expr_code}
                    \tmov r0, {expr_returned_reg}
                    {self.get_release_memory_codes()}
                    \tret'''
        else:
            code = f'''{expr_code}
                    \tmov r0, {expr_returned_reg}
                    \tret'''
        return code

    def visit_Stmt6(self, node, table):
        # Visit the expression node within the Stmt6 node and get the generated code and returned register.
        res = self.visit(node.expr, table)
        expr_code = res["code"]
        expr_returned_reg = res["reg"]

        # Check if we are returning from the main function. If so, release all allocated vector registers.
        if table.name == "main_function_body_block_table":
            code = f'''{expr_code}
                        \tmov r0, {expr_returned_reg}
                        {self.get_release_memory_codes()}
                        \tret'''
        else:
            code = f'''{expr_code}
                    \tmov r0, {expr_returned_reg}
                    \tret'''

        return code

    def visit_Stmt7(self, node, table):
        # Find the symbol table for the 'body' block using the line number of the node.
        body_block_symbol_table = self.find_symbol_table(
            f"body_block_{node.lineno}", table)

        # Visit the body node within the Stmt7 node and generate code for it.
        body_code = self.visit(node.body, body_block_symbol_table)

        # Assign the generated code to the 'code' variable.
        code = body_code

        return code

    def visit_Stmt8(self, node, table):
        code = ""
        return code

    def visit_Defvar(self, node, table):
        # Get the name and type of the variable from the node.
        name = node.iden.iden_value
        type = node.type.type_value

        # Initialize the variable symbol register for the variable.
        reg = self.initiate_var_symbol_register(name, table)

        # Generate code to move 0 into the register.
        code = f'''
    \tmov {reg}, {0}'''

        return code

    def visit_Expr1(self, node, table):
        # Visit the expr1 node within the Expr1 node and get the result.
        res = self.visit(node.expr1, table)
        vector_iden_reg = res["reg"]

        # Visit the expr2 node within the Expr1 node and get the result.
        res2 = self.visit(node.expr2, table)
        expr2_returned_code = res2["code"]
        expr2_returned_reg = res2["reg"]

        # Create temporary registers.
        tmp_reg = self.create_register()
        tmp_reg2 = self.create_register()
        tmp_reg3 = self.create_register()
        tmp_reg4 = self.create_register()

        # Generate code for accessing a vector cell using the format "A[n]".
        # The result includes the register containing the value of the specific vector cell,
        # and the address of that cell.
        return {"reg": tmp_reg4, "addr": tmp_reg3,
                "code": f'''{expr2_returned_code}
                        \tmov {tmp_reg}, 1
                        \tmov {tmp_reg2}, 8
                        \tadd {tmp_reg}, {expr2_returned_reg}, {tmp_reg}
                        \tmul {tmp_reg2}, {tmp_reg}, {tmp_reg2}
                        \tadd {tmp_reg3}, {vector_iden_reg}, {tmp_reg2}
                        \tld {tmp_reg4}, {tmp_reg3}'''}

    def visit_Expr2(self, node, table):
        code = ""
        return code

    def visit_Expr3(self, node, table):
        # Visit the expr1 node within the Expr3 node and get the result.
        res = self.visit(node.expr1, table)
        expr_returned_code = res["code"]
        expr_returned_reg = res["reg"]

        # Visit the expr2 node within the Expr3 node and get the result.
        res2 = self.visit(node.expr2, table)
        expr2_returned_code = res2["code"]
        expr2_returned_reg = res2["reg"]

        # Visit the expr3 node within the Expr3 node and get the result.
        res3 = self.visit(node.expr3, table)
        expr3_returned_code = res3["code"]
        expr3_returned_reg = res3["reg"]

        # Create temporary register, labels.
        tmp_reg = self.create_register()
        label = self.create_label()
        label2 = self.create_label()

        # Generate code for conditional branching based on the value of expr_returned_reg.
        # If expr_returned_reg is zero, jump to label.
        # If not zero, continue to expr2_returned_code and move expr2_returned_reg to tmp_reg.
        # Jump to label2 to skip expr3_returned_code if expr_returned_reg was zero.
        # Generate code for executing expr3_returned_code and moving expr3_returned_reg to tmp_reg.
        return {"reg": tmp_reg,
                "code": f'''{expr_returned_code}
                        \tjz {expr_returned_reg}, {label}
                        {expr2_returned_code}
                        \tmov {tmp_reg}, {expr2_returned_reg}
                        \jmp {label2}
                        {label}:
                        {expr3_returned_code}
                        \tmov {tmp_reg}, {expr3_returned_reg}
                        {label2}:'''}

    def visit_Expr4(self, node, table):
        # Get the operator from the node.
        operator = node.oper

        # Visit the expr1 node within the Expr4 node and get the result.
        res = self.visit(node.expr1, table)
        expr_returned_code = res["code"]
        expr_returned_reg = res["reg"]

        # Visit the expr2 node within the Expr4 node and get the result.
        res2 = self.visit(node.expr2, table)
        expr2_returned_code = res2["code"]
        expr2_returned_reg = res2["reg"]

        # Check if the operator is "=" (assignment).
        if operator == "=":
            # Check if the left-hand side expression is a vector.
            if isinstance(node.expr1, AST.Expr1):
                # Get the address of that cell of the vector from the result.
                address_of_that_cell_of_vector = res["addr"]
                tmp_reg = self.create_register()
                # Generate code to execute the expressions and store the value of expr2_returned_reg to the address_of_that_cell_of_vector.
                return {"reg": tmp_reg,
                        "code": f'''
                                {expr_returned_code}
                                {expr2_returned_code}
                                \tst {expr2_returned_reg}, {address_of_that_cell_of_vector}'''}

            else:
                # If it is not a vector, simply move the value of expr2_returned_reg to expr_returned_reg.
                return {"reg": expr_returned_reg,
                        "code": f'''{expr_returned_code}
                                {expr2_returned_code}
                                \tmov {expr_returned_reg}, {expr2_returned_reg}'''}

        # Check if the operator is "+" (addition).
        if operator == "+":
            # Create a temporary register
            tmp_reg = self.create_register()
            # Generate code to execute the expressions and add expr_returned_reg and expr2_returned_reg, storing the result in tmp_reg.
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
                            {expr2_returned_code}
                            \tadd {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        # Check if the operator is "-" (subtraction)
        if operator == "-":
            tmp_reg = self.create_register()
            # Generate code to execute the expressions and subtract expr2_returned_reg from expr_returned_reg, storing the result in tmp_reg.
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
                            {expr2_returned_code}
                            \tsub {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        # Check if the operator is "*" (multiplication)
        if operator == "*":
            tmp_reg = self.create_register()
            # Generate code to execute the expressions and multiply expr_returned_reg by expr2_returned_reg, storing the result in tmp_reg.
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
                            {expr2_returned_code}
                            \tmul {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        # Check if the operator is "/" (division)
        if operator == "/":
            tmp_reg = self.create_register()
            # Generate code to execute the expressions and divide expr_returned_reg by expr2_returned_reg, storing the result in tmp_reg.
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
                            {expr2_returned_code}
                            \tdiv {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        # Check if the operator is "%" (modulus)
        if operator == "%":
            tmp_reg = self.create_register()
            # Generate code to execute the expressions and calculate the modulus of expr_returned_reg by expr2_returned_reg, storing the result in tmp_reg.
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
                            {expr2_returned_code}
                            \tmod {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        # Check if the operator is "<" (less than)
        if operator == "<":
            tmp_reg = self.create_register()
            # Generate code to execute the expressions and compare if expr_returned_reg is less than expr2_returned_reg, storing the result in tmp_reg.
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
                            {expr2_returned_code}
                            \tcmp< {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        # Check if the operator is ">" (greater than)
        if operator == ">":
            tmp_reg = self.create_register()
            # Generate code to execute the expressions and compare if expr_returned_reg is greater than expr2_returned_reg, storing the result in tmp_reg.
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
                            {expr2_returned_code}
                            \tcmp> {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        # Check if the operator is "==" (equal to)
        if operator == "==":
            tmp_reg = self.create_register()
            # Generate code to execute the expressions and compare if expr_returned_reg is equal to expr2_returned_reg, storing the result in tmp_reg.
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
                            {expr2_returned_code}
                            \tcmp= {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        # Check if the operator is "<=" (less than or equal to)
        if operator == "<=":
            tmp_reg = self.create_register()
            # Generate code to execute the expressions and compare if expr_returned_reg is less than or equal to expr2_returned_reg, storing the result in tmp_reg.
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
                            {expr2_returned_code}
                            \tcmp<= {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        # Check if the operator is ">=" (greater than or equal to)
        if operator == ">=":
            tmp_reg = self.create_register()
            # Generate code to execute the expressions and compare if expr_returned_reg is greater than or equal to expr2_returned_reg, storing the result in tmp_reg.
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
                            {expr2_returned_code}
                            \tcmp>= {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        # Check if the operator is "!=" (not equal to)
        if operator == "!=":
            tmp_reg = self.create_register()
            # Create labels for branching
            label = self.create_label()
            label2 = self.create_label()

            # Generate code to execute the expressions and compare if expr_returned_reg is not equal to expr2_returned_reg
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
                            {expr2_returned_code}
                            \tcmp= {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}
                            \tjz {tmp_reg}, {label}
                            \tmov {tmp_reg}, 0
                            \tjmp {label2}
                            {label}:
                            \tmov {tmp_reg}, 1
                            {label2}:'''}

        # Check if the operator is "||" (logical OR)
        if operator == "||":
            # Create labels for branching
            label = self.create_label()
            label2 = self.create_label()
            label3 = self.create_label()

            # Generate code to execute the expressions and perform logical OR
            return {"reg": expr_returned_reg,
                    "code": f'''{expr_returned_code}
                            {expr2_returned_code}
                            \tjz {expr_returned_reg}, {label}
                            \tmov {expr_returned_reg}, 1
                            \tjmp {label3}
                            {label}: 
                            \tjz {expr2_returned_reg}, {label2}
                            \tmov {expr_returned_reg}, 1
                            \tjmp {label3}
                            {label2}: 
                            \tmov {expr_returned_reg}, 0
                            {label3}:'''}

        # Check if the operator is "&&" (logical AND)
        if operator == "&&":
            # Create labels for branching
            label = self.create_label()
            label2 = self.create_label()
            label3 = self.create_label()

            # Generate code to execute the expressions and perform logical AND
            return {"reg": expr_returned_reg,
                    "code": f'''{expr_returned_code}
                            {expr2_returned_code}
                            \tjz {expr_returned_reg}, {label2}
                            \tjz {expr2_returned_reg}, {label2}
                            {label}:
                            \tmov {expr_returned_reg}, 1
                            \tjmp {label3}
                            {label2}:
                            \tmov {expr_returned_reg}, 0
                            {label3}:'''}

    def visit_Expr5(self, node, table):
        operator = node.oper

        res = self.visit(node.expr, table)
        expr_returned_code = res["code"]
        expr_returned_reg = res["reg"]

        # Check if the operator is "!"
        if operator == "!":
            label = self.create_label()
            label2 = self.create_label()

            # Generate code to execute the expression and perform logical NOT
            return {"reg": expr_returned_reg,
                    "code": f'''{expr_returned_code}
                            \tjz {expr_returned_reg}, {label}
                            \tmov {expr_returned_reg}, 0
                            \tjmp {label2}
                            {label}:
                            \tmov {expr_returned_reg}, 1
                            {label2}:'''}

        # Check if the operator is "+"
        if operator == "+":
            # Return the result of the expression without any modifications
            return {"reg": expr_returned_reg,
                    "code": expr_returned_code}

        # Check if the operator is "-"
        if operator == "-":
            tmp_reg = self.create_register()

            # Generate code to execute the expression and perform arithmetic negation
            return {"reg": expr_returned_reg,
                    "code": f'''{expr_returned_code}
                            \tmov {tmp_reg}, 2
                            \tmul {tmp_reg}, {expr_returned_reg}, {tmp_reg}
                            \tsub {expr_returned_reg}, {tmp_reg}, {expr_returned_reg}'''}

    def visit_Expr6(self, node, table):
        name = node.iden.iden_value

        iden_reg = ""

        # Check if the variable has a "reg" attribute, indicating it has been initialized before
        if hasattr(table.get(name), "reg"):
            iden_reg = table.get(name).reg

        # If the variable doesn't have a "reg" attribute, it means it wasn't defined initially but was added to the table
        # due to error correction. In this case, it needs to be initiated.
        else:
            reg = self.initiate_var_symbol_register(name, table)
            iden_reg = reg

        # Return the register and an empty code block
        return {"reg": iden_reg,
                "code": ""}

    def visit_Expr7(self, node, table):
        # function call
        function_iden = node.iden.iden_value

        # Loop through the list of built-in functions
        for i in range(len(self.builtin_funcs)):
            # Check if the function identifier matches the name of a built-in function
            if function_iden == self.builtin_funcs[i]["name"]:
                # Set the "used" attribute of the matched built-in function to True
                self.builtin_funcs[i]["used"] = True

        # Get the arguments from the node and table
        arguments = self.get_arguments(node, table)

        # Initialize empty strings for storing argument registers and codes
        arguments_registers_string = ""
        arguments_codes_string = ""

        # Create a register for storing the returned value
        returning_reg = self.create_register()

        # If the function being called is "list", add the returned register to release it later
        if function_iden == "list":
            self.memory_allocated_registers.append(returning_reg)

        # Loop through the arguments
        for i in range(len(arguments)):
            if i == 0:
                if len(arguments) == 1:
                    # If this is the only argument, add the returning register only to the argument registers string
                    arguments_registers_string += f"{returning_reg}"
                else:
                    # If there are more arguments, add the returning register and a comma to the argument registers string
                    arguments_registers_string += f"{returning_reg}, "

                # Append the code for the first argument to the argument codes string
                arguments_codes_string += f'''{arguments[i]['code']}
                                            \tmov {returning_reg}, {arguments[0]["reg"]}'''

            elif i == len(arguments) - 1:
                # If this is the last argument, add its register directly to the argument registers string
                arguments_registers_string += f"{arguments[i]['reg']}"

                # Append the code for the last argument to the argument codes string
                arguments_codes_string += f"{arguments[i]['code']}"

            else:
                # For other arguments, add their registers and a comma to the argument registers string
                arguments_registers_string += f"{arguments[i]['reg']}, "

                # Append the code for the current argument to the argument codes string
                arguments_codes_string += f"{arguments[i]['code']}, "

        # Check if there are no arguments
        if not arguments:
            # Return the returning register and the code for calling the function
            return {"reg": returning_reg,
                    "code": f'''\tcall {function_iden}, {returning_reg}'''}

        else:
            # Return the returning register and the code for calling the function with arguments
            return {"reg": returning_reg,
                    "code": f'''{arguments_codes_string}
                        \tcall {function_iden}, {arguments_registers_string}'''}

    def visit_Expr8(self, node, table):
        # Visit the 'num' node and get its value
        num = self.visit(node.num, table)

        # Create a register for storing the 'num' value
        num_reg = self.create_register()

        # Return the register and the code for moving the 'num' value into the register
        return {"reg": num_reg,
                "code": f'''
                        \tmov {num_reg}, {num}'''}

    # flist rules are handled inside visit_func

    def visit_Clist1(self, node, table):
        pass

    def visit_Clist2(self, node, table):
        return self.visit(node.expr, table)

    def visit_Clist3(self, node, table):
        self.visit(node.clist, table)
        return self.visit(node.expr, table)

    def visit_Num(self, node, table):
        num = node.num_value
        return num

    def visit_Empty(self, node, table):
        code = ""
        return code

    builtin_funcs = []

    def create_and_push_builtin_funcs(self):

        # Append the built-in function "scan" to the list of built-in functions
        # It takes a number from the input
        self.builtin_funcs.append({"name": "scan", "used": False, "included": False,
                                   "code": '''proc scan
                                            \tcall iget, r0
                                            \tret'''})

        # Append the built-in function "print" to the list of built-in functions
        # Prints a number in the output
        self.builtin_funcs.append({"name": "print", "used": False, "included": False,
                                   "code": '''proc print
                                            \tcall iput, r0
                                            \tret'''})

        # Append the built-in function "list" to the list of built-in functions
        # Allocate cells of memory with a size of 8*n (where n is the length of the vector, the argument to this function)
        # Return a register with the address of the first cell of the vector.
        # The value of the first cell is set to n (length of the vector).
        self.builtin_funcs.append({"name": "lsit", "used": False, "included": False,
                                   "code": '''proc lsit
                                            \tmov r1, 1
                                            \tadd r1, r0, r1
                                            \tmov r2, 8
                                            \tmul r2, r1, r2
                                            \tcall mem, r2
                                            \tst r0, r2
                                            \tmov r0, r2
                                            \tret'''})
        # Append the built-in function "length" to the list of built-in functions
        # Load the value stored in the first cell of the vector into register r1 and return it.
        self.builtin_funcs.append({"name": "length", "used": False, "included": False,
                                   "code": '''proc length
                                            \tld r1, r0
                                            \tmov r0, r1
                                            \tret'''})

    def create_register(self):
        # Check if the current register index is greater than the maximum register index used in the code
        if self.reginster_index > config.max_register_index_used_in_code:
            # Update the maximum register index used in the code to the current register index
            config.max_register_index_used_in_code = self.reginster_index
        # Increment the register index
        self.reginster_index += 1
        # Return the register name with its index (e.g., r0, r1, r2)
        return f"r{self.reginster_index - 1}"

    def create_label(self, name=None):
        # Increment the label index
        self.label_index += 1
        if name:
            # If a specific name is provided, return the label name with its index
            return f"{name}{self.label_index - 1}"
        # Otherwise, return a default label name with its index
        return f"label{self.label_index - 1}"

    def find_symbol_table(self, name, parent):
        # Iterate through the children of the parent symbol table
        for i in range(len(parent.children)):
            # Check if the name of the current child matches the given name
            if parent.children[i].name == name:
                # Return the matching child symbol table
                return parent.children[i]

    def get_parameters(self, node):
        # Initialize an empty list to store the parameters
        parameters = []

        # Access the flist attribute of the given node
        flist = node.flist

        # Check if the flist is not an instance of AST.Empty
        if not isinstance(flist, AST.Empty):
            # Check if flist has an iden attribute (denoting a parameter)
            if flist.iden:
                # Append a dictionary with the parameter identifier and type to the parameters list
                parameters.append({"iden": flist.iden, "type": flist.type})

            # Iterate until the flist no longer has a flist attribute
            while hasattr(flist, "flist"):
                # Update flist to its flist attribute
                flist = flist.flist

                # Check if flist is not an instance of AST.Empty
                if not isinstance(flist, AST.Empty):
                    # Append a dictionary with the parameter identifier and type to the parameters list
                    parameters.append({"iden": flist.iden, "type": flist.type})

        # Return the list of parameters
        return parameters

    def get_arguments(self, node, table):
        # Initialize an empty list to store the arguments
        arguments = []

        # Access the clist attribute of the given node
        clist = node.clist

        # Check if the clist is not an instance of AST.Empty
        if not isinstance(clist, AST.Empty):
            # Check if clist has an expr attribute (denoting an argument)
            if clist.expr:
                # Visit the clist and pass in the table for processing
                res = self.visit(clist, table)

                # Obtain the code and register returned from the visit operation
                expr_returned_code = res["code"]
                expr_returned_reg = res["reg"]

                # Check if the result is not a string and if it exists
                if not isinstance(res, str) and res:
                    res = expr_returned_reg

                # Append a dictionary with the register and code to the arguments list
                arguments.append(
                    {"reg": expr_returned_reg, "code": expr_returned_code})

            # Iterate until the clist no longer has a clist attribute
            while hasattr(clist, "clist"):
                # Update clist to its clist attribute
                clist = clist.clist

                # Check if clist is not an instance of AST.Empty
                if not isinstance(clist, AST.Empty):
                    # Visit the clist and pass in the table for processing
                    res = self.visit(clist, table)

                    # Obtain the code and register returned from the visit operation
                    expr_returned_code = res["code"]
                    expr_returned_reg = res["reg"]

                    # Check if the result is not a string and if it exists
                    if not isinstance(res, str):
                        res = expr_returned_reg

                    # Append a dictionary with the register and code to the arguments list
                    arguments.append(
                        {"reg": expr_returned_reg, "code": expr_returned_code})

        # Return the list of arguments
        return arguments

    def initiate_var_symbol_register(self, name, table):
        # Get the variable symbol from the table using the given name
        var_symbol = table.get(name)

        # Create a new register for the variable symbol
        reg = self.create_register()

        # Set the "reg" attribute of the var_symbol object to the created register
        setattr(var_symbol, "reg", reg)

        # Return the register
        return reg

    def update_var_symbol_register(self, name, value, table):
        # Get the variable symbol from the table using the given name
        var_symbol = table.get(name)

        # Create the code to update the variable symbol's register with the given value
        code = f"\tmov {var_symbol}, {value}"

        return code

    def get_release_memory_codes(self):
        # Initialize an empty string to store the release memory codes
        code = ""

        # Iterate over the memory_allocated_registers list
        for reg in self.memory_allocated_registers:
            # Append the code to release the memory associated with the register
            code += f"\n\tcall rel, {reg}"

        return code
