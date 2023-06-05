from levels.lexer.tokens import Tokens
from utils.color_prints import Colorprints
import config
from utils.ast import *


class Grammar(object):

    tokens = Tokens.tokens

    def __init__(self, parser_messages, lines_we_corrected):
        self.parser_messages = parser_messages
        self.lines_we_corrected = lines_we_corrected

    def p_prog1(self, p):
        '''prog : empty'''
        p[0] = {
            "name": "prog",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Empty(self.lexer.lineno)
        }
        # config.ast = p[0]["ast"]

    def p_prog2(self, p):
        '''prog : func prog'''
        p[0] = {
            "name": "prog",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p), # st: syntax tree
            # ast: abstract syntax tre, self.lexer.linenoe
            "ast": Prog2(p[1]["ast"], p[2]["ast"], self.lexer.lineno)
        }
        config.ast = p[0]["ast"]

    def p_func(self, p):
        '''func : DEF type iden LPAREN flist RPAREN func_choice'''
        p[0] = {
            "name": "func",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Func(p[2]["ast"], p[3]["ast"], p[5]["ast"], p[7]["ast"], self.lexer.lineno)
        }
    
    
    def p_func_error1(self, p):
        '''func : DEF type iden LPAREN error RPAREN func_choice'''
        p[0] = {
            "name": "func",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Func(p[2]["ast"], p[3]["ast"], p[5], p[7]["ast"], self.lexer.lineno)
        }
        # self.p_error()
        self.parser_messages.add_message(
            {"message": "Suitable parameters wasn't defined", "lineno": self.lines_we_corrected.pop(), "is_warning": True})
    
    def p_func_error2(self, p):
        '''func : DEF error iden LPAREN flist RPAREN func_choice'''
        p[0] = {
            "name": "func",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Func(Type("null", None, self.lexer.lineno), p[3]["ast"], p[5]["ast"], p[7]["ast"], self.lexer.lineno)
        }
        # self.p_error()
        self.parser_messages.add_message(
            {"message": "Type must be on of 'int', 'str', 'vector<int>', 'vector<str>'", "lineno": self.lines_we_corrected.pop(), "is_warning": True})

    
    def p_func_choice1(self, p):
        '''func_choice : LBRACE body RBRACE'''
        p[0] = {
            "name": "func_choice",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": FuncChoice1(p[2]["ast"], self.lexer.lineno)
        }

    def p_func_choice2(self, p):
        '''func_choice : RETURN expr SEMICOLON'''
        p[0] = {
            "name": "func_choice",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": FuncChoice2(p[2]["ast"], self.lexer.lineno)
        }

    def p_body1(self, p):
        '''body : empty'''
        p[0] = {
            "name": "body",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Empty(self.lexer.lineno)
        }

    def p_body2(self, p):
        '''body : stmt body'''
        p[0] = {
            "name": "body",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Body2(p[1]["ast"], p[2]["ast"], self.lexer.lineno)
        }

    '''Note: error token usually does not appear as 
        the last token on the right in an error rule'''

    def p_body2_error(self, p):
        '''body : error body'''
        p[0] = {
            "name": "body",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Body2(p[1], p[2]["ast"], self.lexer.lineno)
        }

        self.parser_messages.add_message({"message": "There must be an statement",
                                         "lineno": self.lines_we_corrected.pop(), "is_warning": True})
        # self.parser_messages.add_message({"message": "",
        #                                  "lineno": self.lines_we_corrected.pop(), "is_warning": True})

    def p_stmt1(self, p):
        '''stmt : expr SEMICOLON'''
        p[0] = {
            "name": "stmt",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt1(p[1]["ast"], self.lexer.lineno)
        }

    def p_stmt1_error(self, p):
        '''stmt : error SEMICOLON'''
        p[0] = {
            "name": "stmt",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt1(p[1], self.lexer.lineno)
        }

        self.parser_messages.add_message(
            {"message": "There must be an expression before ;", "lineno": self.lines_we_corrected.pop(), "is_warning": True})

    def p_stmt2(self, p):
        '''stmt : defvar SEMICOLON'''
        p[0] = {
            "name": "stmt",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt2(p[1]["ast"], self.lexer.lineno)
        }

    def p_stmt3(self, p):
        '''stmt : IF LPAREN expr RPAREN stmt else_choice'''
        p[0] = {
            "name": "stmt",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt3(p[3]["ast"], p[5]["ast"], p[6]["ast"], self.lexer.lineno)
        }

    def p_stmt3_error(self, p):  # For errors in the paranthesis
        '''stmt : IF LPAREN error RPAREN stmt else_choice'''
        p[0] = {
            "name": "stmt",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt3(p[3], p[5]["ast"], p[6]["ast"], self.lexer.lineno)
        }

        self.parser_messages.add_message({"message": "There must be an expression inside the paranthesis",
                                         "lineno": self.lines_we_corrected.pop(), "is_warning": True})

    def p_else_choice1(self, p):
        '''else_choice : empty'''
        p[0] = {
            "name": "else_choice",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Empty(self.lexer.lineno)
        }

    def p_else_choice2(self, p):
        '''else_choice : ELSE stmt'''
        p[0] = {
            "name": "else_choice",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": ElseChoice2(p[2]["ast"], self.lexer.lineno)
        }

    def p_stmt4(self, p):
        '''stmt : WHILE LPAREN expr RPAREN stmt'''
        p[0] = {
            "name": "stmt",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt4(p[3]["ast"], p[5]["ast"], self.lexer.lineno)
        }

    def p_stmt4_error(self, p):
        '''stmt : WHILE LPAREN error RPAREN stmt'''
        p[0] = {
            "name": "stmt",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt4(p[3], p[5]["ast"], self.lexer.lineno)
        }

        self.parser_messages.add_message(
            {"message": "There must be an expression inside the paranthesis", "lineno": self.lexer.lineno, "is_warning": True})

    def p_stmt5(self, p):
        '''stmt : FOR LPAREN iden ASSIGN expr TO expr RPAREN stmt'''
        p[0] = {
            "name": "stmt",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt5(p[3]["ast"], p[5]["ast"], p[7]["ast"], p[9]["ast"], self.lexer.lineno)
        }

    def p_stmt5_error1(self, p):
        '''stmt : FOR LPAREN iden ASSIGN error TO expr RPAREN stmt'''
        p[0] = {
            "name": "stmt",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt5(p[3]["ast"], p[5], p[7]["ast"], p[9]["ast"], self.lexer.lineno)
        }

        self.parser_messages.add_message({"message": "There must be an expression inside the paranthesis",
                                         "lineno": self.lines_we_corrected.pop(), "is_warning": True})

    def p_stmt5_error2(self, p):
        '''stmt : FOR LPAREN iden ASSIGN expr TO error RPAREN stmt'''
        p[0] = {
            "name": "stmt",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt5(p[3]["ast"], p[5]["ast"], p[7], p[9]["ast"], self.lexer.lineno)
        }

        self.parser_messages.add_message({"message": "There must be an expression inside the paranthesis",
                                         "lineno": self.lines_we_corrected.pop(), "is_warning": True})
    
    def p_stmt5_error3(self, p):
        '''stmt : FOR LPAREN iden ASSIGN expr TO expr RPAREN error'''
        p[0] = {
            "name": "stmt",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt5(p[3]["ast"], p[5]["ast"], p[7]["ast"], p[9], self.lexer.lineno)
        }

        self.parser_messages.add_message({"message": "There must be an expression inside the paranthesis",
                                         "lineno": self.lines_we_corrected.pop(), "is_warning": True})

    def p_stmt6(self, p):
        '''stmt : RETURN expr SEMICOLON'''
        p[0] = {
            "name": "stmt",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt6(p[2]["ast"], self.lexer.lineno)
        }

    def p_stmt7(self, p):
        '''stmt : LBRACE body RBRACE'''
        p[0] = {
            "name": "stmt",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt7(p[2]["ast"], self.lexer.lineno)
        }

    def p_stmt8(self, p):
        '''stmt : func'''
        p[0] = {
            "name": "stmt",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt8(p[1]["ast"], self.lexer.lineno)
        }

    def p_defvar(self, p):
        '''defvar : VAR type iden defvar_choice'''
        p[0] = {
            "name": "defvar",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Defvar(p[2]["ast"], p[3]["ast"], p[4]["ast"], self.lexer.lineno)
        }

    def p_defvar_error(self, p):
        '''defvar : VAR error iden defvar_choice'''
        p[0] = {
            "name": "defvar",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Defvar(Type("null", None, self.lexer.lineno), p[3]["ast"], p[4]["ast"], self.lexer.lineno)
        }

        self.parser_messages.add_message(
            {"message": "Type must be on of 'int', 'str', 'vector<int>', 'vector<str>'", "lineno": self.lines_we_corrected.pop(), "is_warning": True})

    
    def p_defvar_choice1(self, p):
        '''defvar_choice : empty'''
        p[0] = {
            "name": "defvar_choice",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Empty(self.lexer.lineno)
        }

    def p_defvar_choice2(self, p):
        '''defvar_choice : ASSIGN expr'''
        p[0] = {
            "name": "defvar_choice",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": DefvarChoice2(p[2]["ast"], self.lexer.lineno)
        }

    def p_flist1(self, p):
        '''flist : empty'''
        p[0] = {
            "name": "flist",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Empty(self.lexer.lineno)
        }

    def p_flist2(self, p):
        '''flist : type iden'''
        p[0] = {
            "name": "flist",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Flist2(p[1]["ast"], p[2]["ast"], self.lexer.lineno)
        }

    def p_flist2_error(self, p):
        '''flist : error iden'''
        p[0] = {
            "name": "flist",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Flist2(Type("null", None, self.lexer.lineno), p[2]["ast"], self.lexer.lineno)
        }

    def p_flist3(self, p):
        '''flist : type iden COMMA flist'''
        p[0] = {
            "name": "flist",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Flist3(p[1]["ast"], p[2]["ast"], p[4]["ast"], self.lexer.lineno)
        }
    
    def p_flist3_error(self, p):
        '''flist : error iden COMMA flist'''
        p[0] = {
            "name": "flist",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Flist3(Type("null", None, self.lexer.lineno), p[2]["ast"], p[4]["ast"], self.lexer.lineno)
        }

    def p_clist1(self, p):
        '''clist : empty'''
        p[0] = {
            "name": "clist",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Empty(self.lexer.lineno)
        }

    def p_clist2(self, p):
        '''clist : expr'''
        p[0] = {
            "name": "clist",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Clist2(p[1]["ast"], self.lexer.lineno)
        }

    def p_clist3(self, p):
        '''clist : expr COMMA clist'''
        p[0] = {
            "name": "clist",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Clist3(p[1]["ast"], p[3]["ast"], self.lexer.lineno)
        }

    def p_expr1(self, p):
        '''expr : expr LBRACKET expr RBRACKET'''
        p[0] = {
            "name": "expr",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr1(p[1]["ast"], p[3]["ast"], self.lexer.lineno)
        }

    def p_expr1_error(self, p):
        '''expr : expr LBRACKET error RBRACKET'''
        p[0] = {
            "name": "expr",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr1(p[1]["ast"], p[3], self.lexer.lineno)
        }

        self.parser_messages.add_message(
            {"message": "There must be an expression inside the bracket", "lineno": self.lexer.lineno, "is_warning": True})

    def p_expr2(self, p):
        '''expr : LBRACKET clist RBRACKET'''
        p[0] = {
            "name": "expr",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr2(p[2]["ast"], self.lexer.lineno)
        }

    def p_expr2_error(self, p):
        '''expr : LBRACKET error RBRACKET'''
        p[0] = {
            "name": "expr",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr2(p[2], self.lexer.lineno)
        }

        self.parser_messages.add_message(
            {"message": "Error Inside the paranthesis,you should put the arguments inside it", "lineno": self.lexer.lineno, "is_warning": True})

    def p_expr3(self, p):
        '''expr : expr QUESTIONMARK expr COLON expr'''
        p[0] = {
            "name": "expr",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr3(p[1]["ast"], p[3]["ast"], p[5]["ast"], self.lexer.lineno)
        }

    def p_expr3_error(self, p):  # For errors when you put "";" instead of ":"
        '''expr : expr QUESTIONMARK expr error expr'''
        p[0] = {
            "name": "expr",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr3(p[1]["ast"], p[3]["ast"], p[5]["ast"], self.lexer.lineno)
        }

        self.parser_messages.add_message(
            {"message": "The syntax is 'expr ? expr : expr'", "lineno": self.lexer.lineno, "is_warning": True})

    def p_expr4(self, p):
        '''expr : expr ASSIGN expr
                | expr PLUS expr
                | expr MINUS expr
                | expr TIMES expr
                | expr DIVIDE expr
                | expr MOD expr
                | expr GT expr
                | expr LT expr
                | expr EQUAL expr
                | expr GTE expr
                | expr LTE expr
                | expr NOT_EQUAL expr
                | expr OR expr
                | expr AND expr'''
        p[0] = {
            "name": "expr",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr4(p[1]["ast"], p[2], p[3]["ast"], self.lexer.lineno)
        }
    # def p_expr4_error(self, p):
    #     '''expr : error ASSIGN expr'''
    #     self.parser_messages.add_message({"message": "There must be an expression inside the bracket","lineno": self.lexer.lineno, "is_warning":True})
    def p_expr5(self, p):
        '''expr : NOT expr
                | PLUS expr
                | MINUS expr'''
        p[0] = {
            "name": "expr",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr5(p[1], p[2]["ast"], self.lexer.lineno)
        }

    def p_expr6(self, p):
        '''expr : iden'''
        p[0] = {
            "name": "expr",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr6(p[1]["ast"], self.lexer.lineno)
        }

    def p_expr7(self, p):
        '''expr : iden LPAREN clist RPAREN'''
        p[0] = {
            "name": "expr",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr7(p[1]["ast"], p[3]["ast"], self.lexer.lineno)
        }

    def p_expr7_error(self, p):
        '''expr : iden LPAREN error RPAREN'''
        p[0] = {
            "name": "expr",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr7(p[1]["ast"], p[3], self.lexer.lineno)
        }

        self.parser_messages.add_message(
            {"message": "Error Inside the paranthesis,you should put the arguments inside it", "lineno": self.lexer.lineno, "is_warning": True})

    def p_expr8(self, p):
        '''expr : num'''
        p[0] = {
            "name": "expr",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr8(p[1]["ast"], self.lexer.lineno)
        }

    def p_expr9(self, p):
        '''expr : str'''
        p[0] = {
            "name": "expr",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr9(p[1]["ast"], self.lexer.lineno)
        }

    def p_type1(self, p):
        '''type : INT_TYPE
                | STR_TYPE
                | NULL_TYPE'''
        p[0] = {
            "name": "type",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Type(p[1], None, self.lexer.lineno)
        }
    
    def p_type2(self, p):
        '''type : VECTOR_TYPE LT INT_TYPE GT 
                | VECTOR_TYPE LT STR_TYPE GT'''
        
        p[0] = {
            "name": "type",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Type(p[1], p[3], self.lexer.lineno)
        }
    
    def p_type2_error1(self, p):
        '''type : VECTOR_TYPE LT INT_TYPE error 
                | VECTOR_TYPE error INT_TYPE GT
                | VECTOR_TYPE error INT_TYPE error
                | VECTOR_TYPE LT STR_TYPE error
                | VECTOR_TYPE error STR_TYPE GT
                | VECTOR_TYPE error STR_TYPE error'''
        
        p[0] = {
            "name": "type",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Type(p[1], p[3], self.lexer.lineno)
        }
        self.parser_messages.add_message(
            {"message": "Vector type must be on of 'vector<int>', 'vector<str>'", "lineno": self.lines_we_corrected.pop(), "is_warning": True})
    
    def p_type2_error2(self, p):
        '''type : VECTOR_TYPE LT error GT '''
        
        p[0] = {
            "name": "vector_type",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Type(p[1], "null", self.lexer.lineno)
        }
        self.parser_messages.add_message(
            {"message": "Vector type must be on of 'vector<int>', 'vector<str>'", "lineno": self.lines_we_corrected.pop(), "is_warning": True})


    def p_iden(self, p):
        '''iden : IDENTIFIER'''
        p[0] = {
            "name": "iden",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Iden(p[1], self.lexer.lineno)
        }

    def p_str(self, p):
        '''str : STRING'''
        p[0] = {
            "name": "string",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Str(p[1], self.lexer.lineno)
        }

    def p_num(self, p):
        '''num : NUMBER'''
        p[0] = {
            "name": "number",
            "lineno": self.lexer.lineno,
            # "st": SyntaxTreeUtil.create_node(p),
            "ast": Num(p[1], self.lexer.lineno)
        }

    def p_empty(self, p):
        '''empty :'''

    def p_error(self, p):
        if p:
            self.lines_we_corrected.append(self.lexer.lineno)
            self.parser_messages.add_message(
                {"message": f"Syntax error at token: '{p.value}'", "lineno": self.lexer.lineno})
            # Colorprints.print_in_red(f"Syntax error at token: '{p.value}'")
            # Just discard the token and tell the parser it's okay.
            # parser.errok()
        else:
            self.parser_messages.add_message(
                {"message": "Syntax error at EOF", "lineno": self.lexer.lineno})

    precedence = (  # olaviat bandi az chap
        ('left', 'error'),
        ('left', 'AND', 'OR'),
        ('left', 'NOT', 'LTE', 'GTE',
         'NOT_EQUAL', 'EQUAL', 'LT', 'GT'),
        ('left', 'ASSIGN', 'QUESTIONMARK', 'COLON'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MOD'),
        ('left', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET'),
    )
