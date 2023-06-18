def p_prog1(self, p):
    '''prog : empty'''
        
def p_prog2(self, p):
    '''prog : func prog'''

def p_func(self, p):
    '''func : DEF type iden LPAREN flist RPAREN func_choice'''

def p_func_choice1(self, p):
    '''func_choice : LBRACE body RBRACE'''

def p_func_choice2(self, p):
    '''func_choice : RETURN expr SEMICOLON'''

def p_body1(self, p):
    '''body : empty'''

def p_body2(self, p):
    '''body : stmt body'''

def p_stmt1(self, p):
    '''stmt : expr SEMICOLON'''

def p_stmt2(self, p):
    '''stmt : defvar SEMICOLON'''

def p_stmt3(self, p):
    '''stmt : IF LPAREN expr RPAREN stmt else_choice'''

def p_else_choice1(self, p):
    '''else_choice : empty'''

def p_else_choice2(self, p):
    '''else_choice : ELSE stmt'''

def p_stmt4(self, p):
    '''stmt : WHILE LPAREN expr RPAREN stmt'''

def p_stmt5(self, p):
    '''stmt : FOR LPAREN iden ASSIGN expr TO expr RPAREN stmt'''

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

def p_expr1(self, p):
    '''expr : expr LBRACKET expr RBRACKET'''

def p_expr2(self, p): # ok
    '''expr : LBRACKET clist RBRACKET'''

def p_expr3(self, p):
    '''expr : expr QUESTIONMARK expr COLON expr'''

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

def p_expr5(self, p):
    '''expr : NOT expr
            | PLUS expr
            | MINUS expr'''

def p_expr6(self, p):
    '''expr : iden'''

def p_expr7(self, p):
    '''expr : iden LPAREN clist RPAREN'''

def p_expr8(self, p):
    '''expr : num'''

def p_expr9(self, p):
    '''expr : str'''

def p_type1(self, p):
    '''type : INT_TYPE
            | STR_TYPE
            | NULL_TYPE'''

def p_type2(self, p):
    '''type : VECTOR_TYPE LT INT_TYPE GT 
            | VECTOR_TYPE LT STR_TYPE GT'''

def p_iden(self, p):
    '''iden : IDENTIFIER'''

def p_str(self, p):
    '''str : STRING'''

def p_num(self, p):
    '''num : NUMBER'''

def p_empty(self, p):
    '''empty :'''