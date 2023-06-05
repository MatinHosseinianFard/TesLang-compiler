import re

class Tokens(object):

    def __init__(self, lexer_messages):
        self.lexer_messages = lexer_messages

    tokens = (
    'IDENTIFIER', 'INT_TYPE', 'VECTOR_TYPE', 'STR_TYPE', 'NULL_TYPE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
    'COMMA', 'COLON', 'SEMICOLON',
    'VAR', 'RETURN',
    'FOR', 'WHILE', 'TO', 'DEF', 'IF', 'ELSE',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'ASSIGN', 'EQUAL', 'NOT_EQUAL', 'LT', 'LTE', 'GT', 'GTE', 'AND', 'OR', 'NOT',
    'QUESTIONMARK',
    'NUMBER', 'STRING',
    'COMMENT'
    )

    # Regular expression rules for tokens
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'{'
    t_RBRACE = r'}'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_COMMA = r','
    t_COLON = r':'
    t_SEMICOLON = r';'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MOD = r'%'
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_QUESTIONMARK = r'\?'
    t_NOT = r'!'
    t_ASSIGN = r'='
    t_EQUAL = r'=='
    t_NOT_EQUAL = r'!='
    t_LT = r'<'
    t_LTE = r'<='
    t_GT = r'>'
    t_GTE = r'>='
    t_FOR = r'for'
    t_WHILE = r'while'
    t_TO = r'to'
    t_VAR = r'var'
    t_DEF = r'def'
    t_IF = r'if'
    t_ELSE = r'else'
    t_RETURN = r'return'
    t_INT_TYPE = r'int'
    t_VECTOR_TYPE = r'vector'
    t_STR_TYPE = r'str'
    t_NULL_TYPE = r'null'

    t_ignore = ' \t'


    def t_IDENTIFIER(self, t):
        # This regular expression matches any word (a string that starts with a letter or underscore, followed
        # by zero or more letters or digits)
        r'[a-zA-Zـ][a-zA-Z0-9]*'

        # A dictionary containing some reserved keywords and their corresponding token types.
        keywords = {
            'def': 'DEF',
            'int': 'INT_TYPE',
            'vector': 'VECTOR_TYPE',
            'str': 'STR_TYPE',
            'null': 'NULL_TYPE',
            'var': 'VAR',
            'return': 'RETURN',
            'for': 'FOR',
            'while': 'WHILE',
            'if': 'IF',
            'else': 'ELSE',
            'to': 'TO',
            # 'and': 'AND',
            # 'or': 'OR',
            # 'not': 'NOT',
        }

        # If the matched string is a reserved keyword, set its type accordingly.
        # Otherwise, it is an identifier.
        t.type = keywords.get(t.value, 'IDENTIFIER')
        return t


    def t_NUMBER(self, t):
        # This is a regular expression that matches one or more digits (0-9)
        r'[0-9]+'

        # Convert the matched string (representing the NUMBER) to an actual NUMBER value
        # and store it in the token's value field
        t.value = int(t.value)
        return t


    def t_STRING(self, t):
        # The first expression matches text that begins with a double-quote,
        # followed by any number of characters that are not double-quotes or newline characters,
        # and ends with a double-quote.
        # The second expression matches text that begins with a single-quote,
        # followed by any number of characters that are not single-quotes or newline characters,
        # and ends with a single-quote.
        r'"[^"\n]*"|\'[^\'\n]*\''

        # Define two regular expressions for matching strings in single or double quotes
        t_STRING_RE1 = r'"[^"\n]*"'
        t_STRING_RE2 = r'\'[^\'\n]*\''

        # Define a dictionary for escape sequences in string literals
        escape_dict = {'\\n': '\n', '\\t': '\t',
                    '\\r': '\r', '\\\\': '\\', '\\"': '\"'}

        # Use re.match() to match the input string to the two regex patterns
        match = re.match(t_STRING_RE1, t.value) or re.match(t_STRING_RE2, t.value)

        # If there is a match to the first pattern, extract the string and replace escape sequences with their respective characters
        if match:
            string = match.group(0)[1:-1]
            for escape_seq, escape_char in escape_dict.items():
                string = string.replace(escape_seq, escape_char)
            t.value = string
            return t
        # If there is no match to the first pattern, try the second pattern
        else:
            raise ValueError("Invalid string")


    def t_COMMENT(self, t):
        # The following regular expression matches the pattern for comments
        # that start with '#', and extends to the end of the line.
        r'\#.*'

        # This function doesn't do anything besides matching the comment pattern.
        pass

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)


    # This function is defined to handle errors that occur during tokenization.
    def t_error(self, t):
        # Print an error message indicating the illegal character that was found.
        self.lexer_messages.add_message({"message":f"Illegal character '{t.value[0]}'","lineno": t.lexer.lineno})

        # Use the 'skip' method to skip over and discard the illegal character and move on to the next one.
        # The parameter 1 indicates the number of characters to skip i.e. 1.
        t.lexer.skip(1)