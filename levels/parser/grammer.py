from levels.lexer.tokens import Tokens
from utils.color_prints import Colorprints



class Grammar(object):

    tokens = Tokens.tokens

    def __init__(self, parser_messages, lines_we_corrected):
        self.parser_messages = parser_messages
        self.lines_we_corrected = lines_we_corrected

    def p_prog1(self, p):
        '''prog : empty'''
    
    def p_prog2(self, p):
        '''prog : func prog'''
    
    def p_func(self, p):
        '''func : DEF type iden LPAREN flist RPAREN func_choice'''

    def p_func_error(self, p):
        '''func : DEF type iden LPAREN error RPAREN func_choice'''
        self.parser_messages.add_message(
            {"message": "Suitable parameters wasn't defined", "lineno": self.lines_we_corrected.pop(), "is_warning": True})
        Colorprints.print_in_cyan(f"message: Suitable parameters wasn't defined, lineno: {self.lexer.lineno}")
    
    def p_func_choice1(self, p):
        '''func_choice : LBRACE body RBRACE'''

    def p_func_choice2(self, p):
        '''func_choice : RETURN expr SEMICOLON'''

    def p_body1(self, p):
        '''body : empty'''
    
    def p_body2(self, p):
        '''body : stmt body'''

    '''Note: error token usually does not appear as 
        the last token on the right in an error rule'''
    def p_body2_error(self, p):
        '''body : stmt error'''
        self.parser_messages.add_message({"message": "There must be an statement before ; or }","lineno": self.lines_we_corrected.pop(), "is_warning":True})
        Colorprints.print_in_cyan("message: There must be an statement before ; or }" + f", lineno: {self.lexer.lineno}")


    def p_stmt1(self, p):
        '''stmt : expr SEMICOLON'''
    
    def p_stmt1_error(self, p):
        '''stmt : error SEMICOLON'''
        self.parser_messages.add_message({"message": "There must be an expression before ;","lineno": self.lines_we_corrected.pop(), "is_warning":True})
        Colorprints.print_in_cyan(f"message: There must be an expression before ;, lineno: {self.lexer.lineno}")


    def p_stmt2(self, p):
        '''stmt : defvar SEMICOLON'''

    def p_stmt3(self, p):
        '''stmt : IF LPAREN expr RPAREN stmt else_choice'''

    def p_stmt3_error(self, p): # For errors in the paranthesis
        '''stmt : IF LPAREN error RPAREN stmt else_choice'''
        self.parser_messages.add_message({"message": "There must be an expression inside the paranthesis","lineno": self.lines_we_corrected.pop(), "is_warning":True})
        Colorprints.print_in_cyan(f"message: There must be an expression inside the paranthesis, lineno: {self.lexer.lineno}")

    def p_else_choice1(self, p):
        '''else_choice : empty'''

    def p_else_choice2(self, p):
        '''else_choice : ELSE stmt'''

    def p_stmt4(self, p):
        '''stmt : WHILE LPAREN expr RPAREN stmt'''
    
    def p_stmt4_error(self, p):
        '''stmt : WHILE LPAREN error RPAREN stmt'''
        self.parser_messages.add_message({"message": "There must be an expression inside the paranthesis","lineno": self.lexer.lineno, "is_warning":True})
        Colorprints.print_in_cyan(f"message: There must be an expression inside the paranthesis, lineno: {self.lexer.lineno}")
       
    def p_stmt5(self, p):
        '''stmt : FOR LPAREN iden ASSIGN expr TO expr RPAREN stmt'''
    
    def p_stmt5_error(self, p):
        '''stmt : FOR LPAREN iden ASSIGN error TO expr RPAREN stmt'''
        self.parser_messages.add_message({"message": "There must be an expression inside the paranthesis","lineno": self.lines_we_corrected.pop(), "is_warning":True})
        Colorprints.print_in_cyan(f"message: There must be an expression inside the paranthesis, lineno: {self.lexer.lineno}")

    def p_stmt6(self, p):
        '''stmt : RETURN expr SEMICOLON'''
    
    def p_stmt7(self, p):
        '''stmt : LBRACE body RBRACE'''

    def p_stmt8(self, p):
        '''stmt : func'''

    def p_defvar(self, p):
        '''defvar : VAR type iden defvar_choice'''

    def p_defvar_choice1(self, p):
        '''defvar_choice : empty'''

    def p_defvar_choice2(self, p):
        '''defvar_choice : ASSIGN expr'''

    def p_flist1(self, p):
        '''flist : empty'''

    def p_flist2(self, p):
        '''flist : type iden'''

    def p_flist3(self, p):
        '''flist : type iden COMMA flist'''

    def p_clist1(self, p):
        '''clist : empty'''

    def p_clist2(self, p):
        '''clist : expr'''

    def p_clist3(self, p):
        '''clist : expr COMMA clist'''

    def p_type(self, p):
        '''type : INT_TYPE
                | VECTOR_TYPE
                | STR_TYPE
                | NULL_TYPE'''

    def p_expr1(self, p):
        '''expr : expr LBRACKET expr RBRACKET'''
    
    def p_expr1_error(self, p):
        '''expr : expr LBRACKET error RBRACKET'''
        self.parser_messages.add_message({"message": "There must be an expression inside the bracket","lineno": self.lexer.lineno, "is_warning":True})
        Colorprints.print_in_cyan(f"message: There must be an expression inside the paranthesis, lineno: {self.lexer.lineno}")

    def p_expr2(self, p):
        '''expr : LBRACKET clist RBRACKET'''
    
    def p_expr2_error(self, p):
        '''expr : LBRACKET error RBRACKET'''
        self.parser_messages.add_message({"message": "Error Inside the paranthesis,you should put the arguments inside it","lineno": self.lexer.lineno, "is_warning":True})
        Colorprints.print_in_cyan(f"message: Error Inside the paranthesis,you should put the arguments inside it, lineno: {self.lexer.lineno}")

    def p_expr3(self, p):
        '''expr : expr QUESTIONMARK expr COLON expr'''


    def p_expr3_error(self, p): # For errors when you put "";" instead of ":"
        '''expr : expr QUESTIONMARK expr error expr'''
        self.parser_messages.add_message({"message": "The syntax is 'expr ? expr : expr'","lineno": self.lexer.lineno, "is_warning":True})
        Colorprints.print_in_cyan(f"message: The syntax is 'expr ? expr : expr', lineno: {self.lexer.lineno}")

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
        
    # def p_expr4_error(self, p):
    #     '''expr : error ASSIGN expr'''
    #     self.parser_messages.add_message({"message": "There must be an expression inside the bracket","lineno": self.lexer.lineno, "is_warning":True})
    #     Colorprints.print_in_cyan(f"message: There must be an expression inside the paranthesis, lineno: {self.lexer.lineno}")

    def p_expr5(self, p):
        '''expr : NOT expr
                | PLUS expr
                | MINUS expr'''

    def p_expr6(self, p):
        '''expr : iden'''

    def p_expr7(self, p):
        '''expr : iden LPAREN clist RPAREN'''

    def p_expr7_error(self, p):
        '''expr : iden LPAREN error RPAREN'''
        self.parser_messages.add_message({"message": "Error Inside the paranthesis,you should put the arguments inside it","lineno": self.lexer.lineno, "is_warning":True})
        Colorprints.print_in_cyan(f"message: Error Inside the paranthesis,you should put the arguments inside it, lineno: {self.lexer.lineno}")

    def p_expr8(self, p):
        '''expr : num'''

    def p_expr9(self, p):
        '''expr : str'''

    def p_iden(self, p):
        '''iden : IDENTIFIER'''
    
    def p_str(self, p):
        '''str : STRING'''
    
    def p_num(self, p):
        '''num : NUMBER'''

    def p_empty(self, p):
        '''empty :'''

    def p_error(self, p):
        if p:
            self.lines_we_corrected.append(self.lexer.lineno)
            Colorprints.print_in_cyan(f"Syntax error at token: {p.value}, lineno: {self.lexer.lineno}")
            self.parser_messages.add_message(
                {"message": f"Syntax error at token: {p.value}", "lineno": self.lexer.lineno})
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