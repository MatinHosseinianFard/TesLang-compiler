import config
from utils.color_prints import Colorprints

class CompilerMessages(object):

    def __init__(self):
        self.errors = 0
        self.warnings = 0
        self.messages = []

    def __repr__(self) -> str:
        return f"errors:{self.errors}, warnings:{self.warnings}, messages:{self.messages}"



    def print_messages(self):
        self.messages.sort(key=self.sort_by_lineno)
        for i, msg in enumerate(self.messages):
            # Colorprints.print_in_black(f"{config.code_file_path}:", end="")
            
            if "is_warning" in msg:
                Colorprints.print_in_yellow(f"=> {msg['message']}")
            else:
                Colorprints.print_in_cyan(f"{msg['lineno']}: ", end="")
                if i+1 < len(self.messages) and\
                    self.messages[i]['lineno'] == self.messages[i+1]['lineno']: 
                    Colorprints.print_in_red(f"{msg['message']}", end=" ")
                else:
                    Colorprints.print_in_red(f"{msg['message']}")

    # def print_messages(self):
    #     self.messages.sort(key=self.sort_by_lineno)
    #     for msg in self.messages:
    #         # Colorprints.print_in_black(f"{config.code_file_path}:", end="")
    #         Colorprints.print_in_cyan(f"{msg['lineno']}: ", end="")
    #         if "is_warning" in msg:
    #             Colorprints.print_in_yellow(f"{msg['message']}")
    #         else:
    #             Colorprints.print_in_red(f"{msg['message']}")
    
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
