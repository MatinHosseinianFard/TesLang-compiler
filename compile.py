import os

from utils.compiler_messages import CompilerMessages
from levels.lexer.tokens import Tokens
from levels.lexer.lexer import Lexer
from levels.parser.grammer import Grammar
from levels.parser.parser import Parser
import config
from utils.color_prints import Colorprints


class Compiler(object):
    def __init__(self):
        self.lexer_messages = CompilerMessages()
        self.parser_messages = CompilerMessages()
        self.lines_we_corrected = []

        self.tokens = Tokens(self.lexer_messages)
        self.lexer = Lexer(self.tokens)

        self.grammar = Grammar(self.parser_messages, self.lines_we_corrected)
        self.grammar.lexer = self.lexer.lexer # lexer attribute in lexer object of Lexer class!
        self.parser = Parser(self.grammar)        


    def compile(self, data, show_syntax_tree=False, print_messages=True):
        # self.lexer.build(data)

        self.parser.build(data)
        print(self.lines_we_corrected)
        if print_messages:
            if self.lexer_messages.errors == 0:
                Colorprints.print_in_green(f"***Congrats! No lexer errors!***")
                self.lexer_messages.print_messages()

            elif self.lexer_messages.errors != 0:
                Colorprints.print_in_yellow(f"***{self.lexer_messages.errors} lexer errors detected***")
                self.lexer_messages.print_messages()
            
            #parser errors
            if self.parser_messages.errors == 0:
                Colorprints.print_in_green(f"***Congrats! No parser errors!***")
                self.parser_messages.print_messages()

            elif self.parser_messages.errors != 0:
                Colorprints.print_in_yellow(f"***{self.parser_messages.errors} parser errors detected***")
                self.parser_messages.print_messages()


if __name__ == '__main__':
    with open("./test/parser.txt") as f:
        data = f.read()
        f.close()
    compiler = Compiler()
    compiler.compile(data, show_syntax_tree=True, print_messages=True)