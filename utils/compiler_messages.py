import config
from sys import maxsize
from utils.color_prints import Colorprints

class CompilerMessages(object):

    def __init__(self):
        self.errors = 0
        self.warnings = 0
        self.messages = []

    def __repr__(self) -> str:
        return f"errors:{self.errors}, warnings:{self.warnings}, messages:{self.messages}"

    def duplicate_lines(self, d):
        seen = set()
        duplicates = set( x['lineno'] for x in d if x['lineno'] in seen or seen.add(x['lineno']) )
        return list( duplicates )

    def duplicate_lines_search(self, line):
        indexes = []
        for i, msg in enumerate(self.messages):
            if msg['lineno'] == line:
                indexes.append(i)
        return indexes
    
    def print_messages(self, one_line=True):
        self.messages.sort(key=self.sort_by_lineno)
        duplicate_lines = self.duplicate_lines(self.messages)
        for line in duplicate_lines:
            common_line = self.duplicate_lines_search(line)
            if len(common_line) > 2:
                error_lines_messages = []
                warning_lines_messages = []
                for cline in common_line:
                    if "is_warning" in self.messages[cline]:
                        warning_lines_messages.append(self.messages[cline])
                    else:
                        error_lines_messages.append(self.messages[cline])

                k = 0
                for cline in common_line:
                    if k % 2 == 0:
                        if len(error_lines_messages) != 0:
                            self.messages[cline] = error_lines_messages.pop(0)
                        elif len(warning_lines_messages) != 0:
                            self.messages[cline] = warning_lines_messages.pop()
                    else:
                        if len(warning_lines_messages) != 0:
                            self.messages[cline] = warning_lines_messages.pop()
                        elif len(error_lines_messages) != 0:
                            self.messages[cline] = error_lines_messages.pop(0)
                    k += 1
        


        for i, msg in enumerate(self.messages):
            # Colorprints.print_in_black(f"{config.code_file_path}:", end="")
            
            
            if "is_warning" in msg:
                if msg['message'] != "":
                    Colorprints.print_in_yellow(f"=> {msg['message']}")
                    
            else:
                Colorprints.print_in_cyan(f"{msg['lineno']}: ", end="")
                
                if one_line and i+1 < len(self.messages) and\
                    self.messages[i]['lineno'] == self.messages[i+1]['lineno'] and self.messages[i+1]['message'] != "": 
                    Colorprints.print_in_red(f"{msg['message']}", end=" ")
                else:
                    Colorprints.print_in_red(f"{msg['message']}")


    
    def add_message(self, message):
        if not message in self.messages:
            self.messages.append(message)
            if not "is_warning" in message:
                self.errors += 1 
            else:
                message["message"] = message["message"]
                self.warnings +=1

    def sort_by_lineno(self, msg):
        return msg["lineno"]
