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

        self.compiled_failed = False

        self.lexer_messages = CompilerMessages()
        self.parser_messages = CompilerMessages()
        self.lines_we_corrected = []
        self.semantic_messages = CompilerMessages()

        self.tokens = Tokens(self.lexer_messages)
        self.lexer = Lexer(self.tokens)

        self.grammar = Grammar(self.parser_messages, self.lines_we_corrected)
        self.grammar.lexer = self.lexer.lexer # lexer attribute in lexer object of Lexer class!
        self.parser = Parser(self.grammar)        

        config.global_symbol_table = SymbolTable(None, "global")
        self.type_checker = TypeChecker(self.semantic_messages)
        self.preprocess = PreProcess(self.semantic_messages)
        self.compiled_failed = False

        self.iR_generator = IRGenerator() 
        self.iR_optimizer = IR_optimizer()


    def compile(self, data, show_syntax_tree=False, print_messages=True):
        # self.lexer.build(data)

        # try:
            self.parser.build(data)
            if print_messages:
                if self.lexer_messages.errors == 0:
                    Colorprints.print_in_green(f"***No lexer errors!***")
                    self.lexer_messages.print_messages()

                elif self.lexer_messages.errors != 0:
                    Colorprints.print_in_yellow(f"***{self.lexer_messages.errors} lexer errors detected***")
                    self.lexer_messages.print_messages()
                    self.compiled_failed = True
                
                #parser errors
                if self.parser_messages.errors == 0:
                    Colorprints.print_in_green(f"***No parser errors!***")
                    self.parser_messages.print_messages()

                elif self.parser_messages.errors != 0:
                    Colorprints.print_in_yellow(f"***{self.parser_messages.errors} parser errors detected***")
                    self.parser_messages.print_messages()
                    self.compiled_failed = True
            
            
            #semantic
            self.preprocess.visit(config.ast, None)
            self.type_checker.visit(config.ast, None)
            #semantic errors
            if print_messages:
                if self.semantic_messages.errors == 0 and not self.compiled_failed:
                    Colorprints.print_in_green(f"***No semantic errors!***")
                    self.semantic_messages.print_messages(one_line=False)

                elif self.semantic_messages.errors != 0:
                    Colorprints.print_in_yellow(f"***{self.semantic_messages.errors} semantic errors detected***")
                    self.semantic_messages.print_messages(one_line=False)

            if self.lexer_messages.errors == 0 and self.parser_messages.errors == 0 and self.semantic_messages.errors == 0:
                    self.iR_generator.visit(config.ast, None)
                    
                    self.iR_optimizer.delete_mov_to_same_register()
                    self.iR_optimizer.delete_empty_lines_from_code()
                    self.iR_optimizer.sort_indetation()

                    f = open("generated_IR.out", "w")
                    f.write(config.iR_code)
                    f.close()


                    Colorprints.print_in_lightPurple("***TSLANG Terminal***")
                    # self.run_tsvm.run()

            else:
                self.compiled_failed = True

        # except Exception as e:
        #     self.compiled_failed = True
        #     print(e)

            if self.compiled_failed:
                Colorprints.print_in_red("!!! Compile failed :( !!!")

if __name__ == '__main__':
    with open("./test/semantic.txt") as f:
    # with open("./test/nested_func.txt") as f:
        data = f.read()
        f.close()
    compiler = Compiler()
    compiler.compile(data, show_syntax_tree=True, print_messages=True)