from anytree import NodeMixin


class ASTNode(NodeMixin):
    def __init__(self, name, id, children=None):
        self.name = name
        self.id = id
        if children:
            self.children = children

class Node(object):
    def accept(self, visitor, table=None):
        return visitor.visit(self)

    def setParent(self, parent):
        self.parent = parent

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class Prog2(Node):
    def __init__(self, func, prog, lineno):
        self.lineno = lineno
        self.func = func
        self.prog = prog
        self.children = (func, prog)

    def __repr__(self):
        return f"{self.__class__.__name__}(func={self.func.__repr__()}, prog={self.prog.__repr__()}, lineno={self.lineno})"



class Func(Node):
    def __init__(self, type, vector_type_choice, iden, flist, func_choice, lineno):
        self.lineno = lineno
        self.type = type
        self.vector_type_choice = vector_type_choice
        self.iden = iden
        self.flist = flist
        self.func_choice = func_choice
        self.children = (type, vector_type_choice, iden, flist, func_choice)

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type.__repr__()}, (vector_type_choice={self.vector_type_choice.__repr__()},  iden={self.iden.__repr__()}, flist={self.flist.__repr__()}, " \
               f"func_choice={self.func_choice.__repr__()}, lineno={self.lineno})"


class FuncChoice1(Node):
    def __init__(self, body, lineno):
        self.lineno = lineno
        self.body = body
        self.children = (body,)

    def __repr__(self):
        return f"{self.__class__.__name__}(body={self.body.__repr__()}, lineno={self.lineno})"


class FuncChoice2(Node):
    def __init__(self, expr, lineno):
        self.lineno = lineno
        self.expr = expr
        self.children = (expr,)

    def __repr__(self):
        return f"{self.__class__.__name__}(expr={self.expr.__repr__()}, lineno={self.lineno})"


class Body2(Node):
    def __init__(self, stmt, body, lineno):
        self.lineno = lineno
        self.stmt = stmt
        self.body = body
        self.children = (stmt, body,)

    def __repr__(self):
        return f"{self.__class__.__name__}(stmt={self.stmt.__repr__()}, body={self.body.__repr__()}, lineno={self.lineno})"


class Stmt1(Node):
    def __init__(self, expr, lineno):
        self.lineno = lineno
        self.expr = expr
        self.children = (expr,)

    def __repr__(self):
        return f"{self.__class__.__name__}(expr={self.expr.__repr__()}, lineno={self.lineno})"


class Stmt2(Node):
    def __init__(self, defavr, lineno):
        self.lineno = lineno
        self.defvar = defavr
        self.children = (defavr,)

    def __repr__(self):
        return f"{self.__class__.__name__}(defvar={self.defvar.__repr__()}, lineno={self.lineno})"



class Stmt3(Node):
    def __init__(self, expr, stmt, else_choice, lineno):
        self.lineno = lineno
        self.expr = expr
        self.stmt = stmt
        self.else_choice = else_choice
        self.children = (expr, stmt, else_choice,)

    def __repr__(self):
        return f"Stmt3(expr={self.expr.__repr__()}, stmt={self.stmt.__repr__()}, else_choice={self.else_choice.__repr__()})"


class ElseChoice2(Node):
    def __init__(self, stmt, lineno):
        self.lineno = lineno
        self.stmt = stmt
        self.children = (stmt,)

    def __repr__(self):
        return f"ElseChoice2(stmt={self.stmt.__repr__()})"


class Stmt4(Node):
    def __init__(self, expr, stmt, lineno):
        self.lineno = lineno
        self.expr = expr
        self.stmt = stmt
        self.children = (expr, stmt)

    def __repr__(self):
        return f"Stmt4(expr={self.expr.__repr__()}, stmt={self.stmt.__repr__()})"


class Stmt5(Node):
    def __init__(self, iden, expr1, expr2, stmt, lineno):
        self.lineno = lineno
        self.iden = iden
        self.expr1 = expr1
        self.expr2 = expr2
        self.stmt = stmt
        self.children = (iden, expr1, expr2, stmt)

    def __repr__(self):
        return f"Stmt5(iden={self.iden.__repr__()}, expr1={self.expr1.__repr__()}, expr2={self.expr2.__repr__()}, stmt={self.stmt.__repr__()})"


class Stmt6(Node):
    def __init__(self, expr, lineno):
        self.lineno = lineno
        self.expr = expr
        self.children = (expr,)

    def __repr__(self):
        return f"Stmt6(expr={self.expr.__repr__()})"


class Stmt7(Node):
    def __init__(self, body, lineno):
        self.lineno = lineno
        self.body = body
        self.children = (body,)

    def __repr__(self):
        return f"Stmt7(body={self.body.__repr__()})"


class Stmt8(Node):
    def __init__(self, func, lineno):
        self.lineno = lineno
        self.func = func
        self.children = (func,)

    def __repr__(self):
        return f"Stmt8(func={self.func.__repr__()})"


class Defvar(Node):
    def __init__(self, type, vector_type_choice, iden, defvar_choice, lineno):
        self.lineno = lineno
        self.type = type
        self.iden = iden
        self.vector_type_choice = vector_type_choice
        self.defvar_choice = defvar_choice
        self.children = (type, vector_type_choice, iden, defvar_choice)

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type.__repr__()}, iden={self.iden.__repr__()}, " \
               f"vector_type_choice={self.vector_type_choice.__repr__()}, defvar_choice={self.defvar_choice.__repr__()}, lineno={self.lineno})"


class VectorTypeChoice2(Node):
    def __init__(self, type, lineno):
        self.lineno = lineno
        self.type = type
        self.children = (type,)

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type.__repr__()}, lineno={self.lineno})"


class DefvarChoice2(Node):
    def __init__(self, expr, lineno):
        self.lineno = lineno
        self.expr = expr
        self.children = (expr,)

    def __repr__(self):
        return f"{self.__class__.__name__}(expr={self.expr.__repr__()}, lineno={self.lineno})"


class Flist2(Node):
    def __init__(self, type, vector_type_choice, iden, lineno):
        self.lineno = lineno
        self.type = type
        self.vector_type_choice = vector_type_choice
        self.iden = iden
        self.children = (type, vector_type_choice, iden)

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type.__repr__()}, (vector_type_choice={self.vector_type_choice.__repr__()}, iden={self.iden.__repr__()}, lineno={self.lineno})"


class Flist3(Node):
    def __init__(self, type, vector_type_choice, iden, flist, lineno):
        self.lineno = lineno
        self.type = type
        self.vector_type_choice = vector_type_choice
        self.iden = iden
        self.flist = flist
        self.children = (type, vector_type_choice, iden, flist)

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type.__repr__()}, (vector_type_choice={self.vector_type_choice.__repr__()}, iden={self.iden.__repr__()}, flist={self.flist.__repr__()}, " \
               f"lineno={self.lineno})"


class Clist2(Node):
    def __init__(self, expr, lineno):
        self.lineno = lineno
        self.expr = expr
        self.children = (expr,)

    def __repr__(self):
        return f"{self.__class__.__name__}(expr={self.expr.__repr__()}, lineno={self.lineno})"


class Clist3(Node):
    def __init__(self, expr, clist, lineno):
        self.lineno = lineno
        self.expr = expr
        self.clist = clist
        self.children = (expr, clist)

    def __repr__(self):
        return f"Clist3(expr={self.expr.__repr__()}, clist={self.clist.__repr__()})"


class Expr1(Node):
    def __init__(self, expr1, expr2, lineno):
        self.lineno = lineno
        self.expr1 = expr1
        self.expr2 = expr2
        self.children = (expr1, expr2)

    def __repr__(self):
        return f"Expr1(expr1={self.expr1.__repr__()}, expr2={self.expr2.__repr__()})"


class Expr2(Node):
    def __init__(self, clist, lineno):
        self.lineno = lineno
        self.clist = clist
        self.children = (clist,)

    def __repr__(self):
        return f"Expr2(clist={self.clist.__repr__()})"


class Expr3(Node):
    def __init__(self, expr1, expr2, expr3, lineno):
        self.lineno = lineno
        self.expr1 = expr1
        self.expr2 = expr2
        self.expr3 = expr3
        self.children = (expr1, expr2, expr3)

    def __repr__(self):
        return f"Expr3(expr1={self.expr1.__repr__()}, expr2={self.expr2.__repr__()}, expr3={self.expr3.__repr__()})"


class Expr4(Node):
    def __init__(self, expr1, oper, expr2, lineno):
        self.lineno = lineno
        self.expr1 = expr1
        self.oper = oper
        self.expr2 = expr2
        self.children = (expr1, oper, expr2)

    def __repr__(self):
        return f"Expr4(expr1={self.expr1.__repr__()}, oper={self.oper.__repr__()}, expr2={self.expr2.__repr__()})"


class Expr5(Node):
    def __init__(self, oper, expr, lineno):
        self.lineno = lineno
        self.oper = oper
        self.expr = expr
        self.children = (oper, expr)

    def __repr__(self):
        return f"Expr5(oper={self.oper.__repr__()}, expr={self.expr.__repr__()})"



class Expr6(Node):
    def __init__(self, iden, lineno):
        self.lineno = lineno
        self.iden = iden
        self.children = (iden,)

    def __repr__(self):
        return f"{self.__class__.__name__}(iden={self.iden.__repr__()}, lineno={self.lineno})"


class Expr7(Node):
    def __init__(self, iden, clist, lineno):
        self.lineno = lineno
        self.iden = iden
        self.clist = clist
        self.children = (iden, clist)

    def __repr__(self):
        return f"{self.__class__.__name__}(iden={self.iden.__repr__()}, clist={self.clist.__repr__()}, lineno={self.lineno})"


class Expr8(Node):
    def __init__(self, num, lineno):
        self.lineno = lineno
        self.num = num
        self.children = (num,)

    def __repr__(self):
        return f"{self.__class__.__name__}(num={self.num.__repr__()}, lineno={self.lineno})"


class Expr9(Node):
    def __init__(self, str, lineno):
        self.lineno = lineno
        self.str = str
        self.children = (str,)

    def __repr__(self):
        return f"{self.__class__.__name__}(str={self.str.__repr__()}, lineno={self.lineno})"


class Type(Node):
    def __init__(self, type_value, lineno):
        self.lineno = lineno
        self.type_value = type_value
        self.children = (type_value,)

    def __repr__(self):
        return f"{self.__class__.__name__}(type_value={self.type_value.__repr__()}, lineno={self.lineno})"


class Iden(Node):
    def __init__(self, iden_value, lineno):
        self.lineno = lineno
        self.iden_value = iden_value
        self.children = (iden_value,)

    def __repr__(self):
        return f"{self.__class__.__name__}(iden_value={self.iden_value.__repr__()}, lineno={self.lineno})"



class Str(Node):
    def __init__(self, str_value, lineno):
        self.lineno = lineno
        self.str_value = str_value
        self.children = (str_value,)

    def __repr__(self):
        return f"{self.__class__.__name__}(str_value={self.str_value}, lineno={self.lineno})"


class Num(Node):
    def __init__(self, num_value, lineno):
        self.lineno = lineno
        self.num_value = num_value
        self.children = (num_value,)

    def __repr__(self):
        return f"{self.__class__.__name__}(num_value={self.num_value}, lineno={self.lineno})"


class Empty(Node):
    def __init__(self, lineno):
        self.lineno = lineno
        self.name = ""
        self.children = ()

    def __repr__(self):
        return f"{self.__class__.__name__}(lineno={self.lineno})"

