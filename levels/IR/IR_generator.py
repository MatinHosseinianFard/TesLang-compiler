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
        # print(func_code)
        # the following if-else statmement makes sure that "main" function always come after all other functions
        if func_name == "main":
            code = prog_code + "\n" + func_code
        else:
            code = func_code + "\n" + prog_code

        # add used builtint functions
        self.builtin_funcs.reverse()
        for i in range(len(self.builtin_funcs)):
            if self.builtin_funcs[i]["used"] and not self.builtin_funcs[i]["included"]:
                code = f'''{self.builtin_funcs[i]["code"]}
{code}'''
                self.builtin_funcs[i]["included"] = True

        config.iR_code = code
        return code

    def visit_Func(self, node, table):
        function_iden = node.iden.iden_value
        function_symbol = table.get(function_iden)
        function_iden = function_symbol.name
        function_body_block = self.find_symbol_table(
            f"{function_iden}_function_body_block_table", table)

        parameters = self.get_parameters(node)

        self.reginster_index = 0
        parameters_initiation_code = ""
        for param in parameters:
            self.initiate_var_symbol_register(
                param["iden"].iden_value, function_body_block)

        func_body_code = self.visit(node.func_choice, function_body_block)
        code = f'''proc {function_iden}
{func_body_code}'''
        return code

    def visit_FuncChoice1(self, node, table):
        body_code = self.visit(node.body, table)
        return body_code

    def visit_FuncChoice2(self, node, table):
        body_code = self.visit(node.expr, table)
        return body_code

    def visit_Body1(self, node, table):
        code = ""
        return code

    def visit_Body2(self, node, table):
        # print(f"visiting: body2")
        stmt_code = self.visit(node.stmt, table)
        body_code = self.visit(node.body, table)

        if not stmt_code:
            code = body_code
        else:
            code = f'''{stmt_code}{body_code}'''
        return code

    def visit_Stmt1(self, node, table):
        res = self.visit(node.expr, table)
        if res:
            expr_code = res["code"]
            code = expr_code
        else:
            code = ""
        return code

    def visit_Stmt2(self, node, table):
        code = self.visit(node.defvar, table)
        return code

    def visit_Stmt3(self, node, table):
        res = self.visit(node.expr, table)
        expr_code = res["code"]
        expr_returned_reg = res["reg"]
        if_block_symbol_table = self.find_symbol_table(
            f"if_block_{node.lineno}", table)  # symbol table for "if" block
        stmt_code = self.visit(node.stmt, if_block_symbol_table)

        label = ""
        label2 = ""
        else_choice_code = ""
        if not isinstance(node.else_choice, AST.Empty):
            else_choice_code = self.visit(node.else_choice, table)
            label = self.create_label()
            label2 = self.create_label()
            code = f'''{expr_code}
\tjz {expr_returned_reg}, {label}
{stmt_code}
\tjmp {label2}
{label}:
{else_choice_code}
{label2}:'''
        else:
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
        # print(f"visiting: stmt4")
        else_block_symbol_table = self.find_symbol_table(
            f"else_block_{node.lineno}", table)  # symbol table for "else" block
        stmt_code = self.visit(node.stmt, else_block_symbol_table)

        code = f'''{stmt_code}'''

        return code

    def visit_Stmt4(self, node, table):
        res = self.visit(node.expr, table)
        expr_code = res["code"]
        expr_returned_reg = res["reg"]

        while_block_symbol_table = self.find_symbol_table(
            f"while_block_{node.lineno}", table)  # symbol table for "do" block of a while
        stmt_code = self.visit(node.stmt, while_block_symbol_table)

        label = self.create_label()
        label2 = self.create_label()
        code = f'''
{label}:
{expr_code}
\tjz {expr_returned_reg}, {label2}
{stmt_code}
\tjmp {label}
{label2}:'''

        return code

    def visit_Stmt5(self, node, table):
        foreach_block_symbol_table = self.find_symbol_table(
            f"foreach_block_{node.lineno}", table)  # symbol table for "foreach" block

        name = node.iden.iden_value
        iden_reg = self.initiate_var_symbol_register(
            name, foreach_block_symbol_table)

        res = self.visit(node.expr1, table)
        expr_code = res["code"]
        expr_returned_reg = res["reg"]

        res2 = self.visit(node.expr2, table)
        expr_code2 = res2["code"]
        expr_returned_reg2 = res2["reg"]

        stmt_code = self.visit(node.stmt, foreach_block_symbol_table)

        tmp_reg = self.create_register()
        tmp_reg2 = self.create_register()
        label = self.create_label()
        label2 = self.create_label()
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

    def visit_Stmt7(self, node, table):
        body_block_symbol_table = self.find_symbol_table(
            f"body_block_{node.lineno}", table)  # symbol table for "body" block
        body_code = self.visit(node.body, body_block_symbol_table)
        code = body_code
        return code

    def visit_Stmt8(self, node, table):
        code = ""
        return code

    def visit_Defvar(self, node, table):
        name = node.iden.iden_value
        type = node.type.type_value
        reg = self.initiate_var_symbol_register(name, table)

        code = f'''
\tmov {reg}, {0}'''
        return code

    def visit_Expr1(self, node, table):
        # calling an vector
        res = self.visit(node.expr1, table)
        vector_iden_reg = res["reg"]

        res2 = self.visit(node.expr2, table)
        expr2_returned_code = res2["code"]
        expr2_returned_reg = res2["reg"]

        tmp_reg = self.create_register()
        tmp_reg2 = self.create_register()
        tmp_reg3 = self.create_register()
        tmp_reg4 = self.create_register()

        # by calling an vector with format "A[n]", reg which contains the value of that specific vector cell, and also
        # addr which contains address of that cell, is being return
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
        res = self.visit(node.expr1, table)
        expr_returned_code = res["code"]
        expr_returned_reg = res["reg"]

        res2 = self.visit(node.expr2, table)
        expr2_returned_code = res2["code"]
        expr2_returned_reg = res2["reg"]

        res3 = self.visit(node.expr3, table)
        expr3_returned_code = res3["code"]
        expr3_returned_reg = res3["reg"]

        tmp_reg = self.create_register()
        label = self.create_label()
        label2 = self.create_label()
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
        operator = node.oper

        res = self.visit(node.expr1, table)
        expr_returned_code = res["code"]
        expr_returned_reg = res["reg"]

        res2 = self.visit(node.expr2, table)
        expr2_returned_code = res2["code"]
        expr2_returned_reg = res2["reg"]

        if operator == "=":
            # check if the left-hand side expr is an vector
            if isinstance(node.expr1, AST.Expr1):
                address_of_that_cell_of_vector = res["addr"]
                tmp_reg = self.create_register()
                return {"reg": tmp_reg,
                        "code": f'''
{expr_returned_code}
{expr2_returned_code}
\tst {expr2_returned_reg}, {address_of_that_cell_of_vector}'''}

            else:
                return {"reg": expr_returned_reg,
                        "code": f'''{expr_returned_code}
{expr2_returned_code}
\tmov {expr_returned_reg}, {expr2_returned_reg}'''}

        if operator == "+":
            tmp_reg = self.create_register()
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
{expr2_returned_code}
\tadd {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        if operator == "-":
            tmp_reg = self.create_register()
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
{expr2_returned_code}
\tsub {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        if operator == "*":
            tmp_reg = self.create_register()
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
{expr2_returned_code}
\tmul {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        if operator == "/":
            tmp_reg = self.create_register()
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
{expr2_returned_code}
\tdiv {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        if operator == "%":
            tmp_reg = self.create_register()
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
{expr2_returned_code}
\tmod {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        if operator == "<":
            tmp_reg = self.create_register()
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
{expr2_returned_code}
\tcmp< {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        if operator == ">":
            tmp_reg = self.create_register()
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
{expr2_returned_code}
\tcmp> {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        if operator == "==":
            tmp_reg = self.create_register()
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
{expr2_returned_code}
\tcmp= {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        if operator == "<=":
            tmp_reg = self.create_register()
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
{expr2_returned_code}
\tcmp<= {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        if operator == ">=":
            tmp_reg = self.create_register()
            return {"reg": tmp_reg,
                    "code": f'''{expr_returned_code}
{expr2_returned_code}
\tcmp>= {tmp_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        if operator == "!=":
            tmp_reg = self.create_register()
            label = self.create_label()
            label2 = self.create_label()

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

        if operator == "||":
            label = self.create_label()
            label2 = self.create_label()
            label3 = self.create_label()

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

        if operator == "&&":
            label = self.create_label()
            label2 = self.create_label()
            label3 = self.create_label()

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

        if operator == "!":
            label = self.create_label()
            label2 = self.create_label()
            return {"reg": expr_returned_reg,
                    "code": f'''{expr_returned_code}
\tjz {expr_returned_reg}, {label}
\tmov {expr_returned_reg}, 0
\tjmp {label2}
{label}:
\tmov {expr_returned_reg}, 1
{label2}:'''}

        if operator == "+":
            return {"reg": expr_returned_reg,
                    "code": expr_returned_code}

        if operator == "-":
            tmp_reg = self.create_register()
            return {"reg": expr_returned_reg,
                    "code": f'''{expr_returned_code}
\tmov {tmp_reg}, 2
\tmul {tmp_reg}, {expr_returned_reg}, {tmp_reg}
\tsub {expr_returned_reg}, {tmp_reg}, {expr_returned_reg}'''}

    
    def visit_Expr6(self, node, table):
        name = node.iden.iden_value

        iden_reg = ""
        # If the variable has "reg" attribute, it means it's initiated before
        if hasattr(table.get(name), "reg"):
            iden_reg = table.get(name).reg

        # If the variable dosn't have a "reg" attribute, it means it wasn't defines but due to error correction, It got
        # added to the table, and since It should be initiated
        else:
            reg = self.initiate_var_symbol_register(name, table)
            iden_reg = reg
        return {"reg": iden_reg,
                "code": ""}
    
    
    def visit_Expr7(self, node, table):
        # function call
        function_iden = node.iden.iden_value
        for i in range(len(self.builtin_funcs)):
            if function_iden == self.builtin_funcs[i]["name"]:
                self.builtin_funcs[i]["used"] = True

        arguments = self.get_arguments(node, table)

        arguments_registers_string = ""
        arguments_codes_string = ""

        returning_reg = self.create_register()

        # If function being called is "list", add the returned register to release it later
        if function_iden == "list":
            self.memory_allocated_registers.append(returning_reg)

        for i in range(len(arguments)):
            if i == 0:
                if len(arguments) == 1:
                    arguments_registers_string += f"{returning_reg}"
                else:
                    arguments_registers_string += f"{returning_reg}, "
                arguments_codes_string += f'''{arguments[i]['code']}
                                                \tmov {returning_reg}, {arguments[0]["reg"]}'''

            elif i == len(arguments) - 1:
                arguments_registers_string += f"{arguments[i]['reg']}"
                arguments_codes_string += f"{arguments[i]['code']}"

            else:
                arguments_registers_string += f"{arguments[i]['reg']}, "
                arguments_codes_string += f"{arguments[i]['code']}, "

        if not arguments:
            return {"reg": returning_reg,
                    "code": f'''\tcall {function_iden}, {returning_reg}'''}

        else:
            return {"reg": returning_reg,
                    "code": f'''{arguments_codes_string}
                        \tcall {function_iden}, {arguments_registers_string}'''}

    

    def visit_Expr8(self, node, table):
        num = self.visit(node.num, table)
        num_reg = self.create_register()
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

        self.builtin_funcs.append({"name": "scan", "used": False, "included": False,
                                   "code": '''proc scan
\tcall iget, r0
\tret'''})

        self.builtin_funcs.append({"name": "print", "used": False, "included": False,
                                   "code": '''proc print
\tcall iput, r0
\tret'''})

        # It allocate cells of memory with size of 8*n (n is length of the vector, the argument to this function)
        # and it reterns a register with the address if the first cell of the vector
        # also first cell of the vector has the value of n (length of the vector)
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

        self.builtin_funcs.append({"name": "length", "used": False, "included": False,
                                   "code": '''proc length
\tld r1, r0
\tmov r0, r1
\tret'''})

    def create_register(self):
        if self.reginster_index > config.max_register_index_used_in_code:
            config.max_register_index_used_in_code = self.reginster_index
        self.reginster_index += 1
        return f"r{self.reginster_index - 1}"

    def create_label(self, name=None):
        self.label_index += 1
        if name:
            return f"{name}{self.label_index - 1}"
        return f"label{self.label_index - 1}"

    def find_symbol_table(self, name, parent):
        for i in range(len(parent.children)):
            if parent.children[i].name == name:
                return parent.children[i]

    def get_parameters(self, node):
        parameters = []
        flist = node.flist
        if not isinstance(flist, AST.Empty):
            if flist.iden:
                parameters.append({"iden": flist.iden, "type": flist.type})
            while hasattr(flist, "flist"):
                flist = flist.flist
                if (not isinstance(flist, AST.Empty)):
                    parameters.append({"iden": flist.iden, "type": flist.type})
        # parameters.reverse()
        return parameters

    def get_arguments(self, node, table):
        # get arguments
        arguments = []
        clist = node.clist
        if not isinstance(clist, AST.Empty):
            if clist.expr:
                res = self.visit(clist, table)
                expr_returned_code = res["code"]
                expr_returned_reg = res["reg"]
                if not isinstance(res, str) and res:
                    res = expr_returned_reg
                arguments.append(
                    {"reg": expr_returned_reg, "code": expr_returned_code})
                while hasattr(clist, "clist"):
                    clist = clist.clist
                    if (not isinstance(clist, AST.Empty)):
                        res = self.visit(clist, table)
                        expr_returned_code = res["code"]
                        expr_returned_reg = res["reg"]
                        if not isinstance(res, str):
                            res = expr_returned_reg
                        arguments.append(
                            {"reg": expr_returned_reg, "code": expr_returned_code})
        return arguments

    def initiate_var_symbol_register(self, name, table):
        var_symbol = table.get(name)
        reg = self.create_register()
        setattr(var_symbol, "reg", reg)
        return reg

    def update_var_symbol_register(self, name, value, table):
        var_symbol = table.get(name)
        code = f"\tmov {var_symbol}, {value}"
        return code

    def get_release_memory_codes(self):
        code = ""
        for reg in self.memory_allocated_registers:
            code += f"\n\tcall rel, {reg}"
        return code
