from utils.symbol_table import SymbolTable
from utils.compiler_messages import CompilerMessages
from levels.lexer.tokens import Tokens
from levels.lexer.lexer import Lexer
from levels.parser.grammer import Grammar
from levels.parser.parser import Parser
from levels.semantic.preprocess import PreProcess
from levels.semantic.type_checker import TypeChecker
from levels.IR.IR_generator import IRGenerator
from levels.IR.IR_optimizer import IR_optimizer
import config
from utils.color_prints import Colorprints


class Compiler(object):
    def __init__(self):

        # Initialize instance variables

        self.compiled_failed = False

        # Create instance of CompilerMessages for lexer, parser, and semantic messages
        self.lexer_messages = CompilerMessages()
        self.parser_messages = CompilerMessages()
        self.semantic_messages = CompilerMessages()

        # Initialize empty list to store lines that were corrected during compilation
        self.lines_we_corrected = []

        # Create instance of Tokens with lexer_messages as an argument
        self.tokens = Tokens(self.lexer_messages)

        # Create instance of Lexer with tokens as an argument
        self.lexer = Lexer(self.tokens)

        # Create instance of Grammar with parser_messages and lines_we_corrected as arguments
        self.grammar = Grammar(self.parser_messages, self.lines_we_corrected)

        # Set lexer attribute in grammar object to the lexer object's lexer attribute
        self.grammar.lexer = self.lexer.lexer

        # Create instance of Parser with grammar as an argument
        self.parser = Parser(self.grammar)

        # Create global symbol table
        config.global_symbol_table = SymbolTable(None, "global")

        # Create instance of TypeChecker with semantic_messages as an argument
        self.type_checker = TypeChecker(self.semantic_messages)

        # Create instance of PreProcess with semantic_messages as an argument
        self.preprocess = PreProcess(self.semantic_messages)

        # Initialize the compiled_failed variable to False
        self.compiled_failed = False

        # Create instance of IRGenerator
        self.iR_generator = IRGenerator()

        # Create instance of IR_optimizer
        self.iR_optimizer = IR_optimizer()

    def compile(self, data, show_syntax_tree=False, print_messages=True):
        # Build the parser using the input data
        self.parser.build(data)
    
        if print_messages:
            if self.lexer_messages.errors == 0:
                Colorprints.print_in_green(f"***No lexer errors!***")
    
            # Print lexer messages and set compiled_failed to True if there are lexer errors
            elif self.lexer_messages.errors != 0:
                Colorprints.print_in_yellow(
                    f"***{self.lexer_messages.errors} lexer errors detected***")
                self.lexer_messages.print_messages()
                self.compiled_failed = True
    
            if self.parser_messages.errors == 0:
                Colorprints.print_in_green(f"***No parser errors!***")
    
            # Print parser messages and set compiled_failed to True if there are parser errors
            elif self.parser_messages.errors != 0:
                Colorprints.print_in_yellow(
                    f"***{self.parser_messages.errors} parser errors detected***")
                self.parser_messages.print_messages()
                self.compiled_failed = True
    
        # Perform semantic analysis on the abstract syntax tree
        self.preprocess.visit(config.ast, None)
        self.type_checker.visit(config.ast, None)
    
        if print_messages:
            if self.semantic_messages.errors == 0 and not self.compiled_failed:
                Colorprints.print_in_green(f"***No semantic errors!***")
    
            # Print semantic messages and set compiled_failed to True if there are semantic errors
            elif self.semantic_messages.errors != 0:
                Colorprints.print_in_yellow(
                    f"***{self.semantic_messages.errors} semantic errors detected***")
                self.semantic_messages.print_messages(one_line=False)
    
        # Generate intermediate representation (IR) code if there are no lexer, parser, and semantic errors
        if self.lexer_messages.errors == 0 and self.parser_messages.errors == 0 and self.semantic_messages.errors == 0:
            self.iR_generator.visit(config.ast, None)
    
            # Optimize the generated IR code
            self.iR_optimizer.delete_mov_to_same_register()
            self.iR_optimizer.delete_empty_lines_from_code()
            self.iR_optimizer.sort_indetation()
    
            # Write the optimized IR code to a file
            f = open("generated_IR.out", "w")
            f.write(config.iR_code)
            f.close()
    
            Colorprints.print_in_lightPurple("***TSLANG Terminal***")
    

        else:
            self.compiled_failed = True

        if self.compiled_failed:
            Colorprints.print_in_red("!!! Compile failed :( !!!")


if __name__ == '__main__':
    with open("./test/correct.txt") as f:
        data = f.read()
        f.close()
    compiler = Compiler()
    compiler.compile(data, show_syntax_tree=True, print_messages=True)
