from utils.color_prints import Colorprints

class CompilerMessages(object):

    # Constructor method to initialize the attributes of the class
    def __init__(self):
        self.errors = 0
        self.warnings = 0
        self.messages = []

    # Method to return a string representation of the object
    def __repr__(self) -> str:
        return f"errors:{self.errors}, warnings:{self.warnings}, messages:{self.messages}"

    # Method to find and return a list of duplicate line numbers in the messages list
    def duplicate_lines(self, d):
        seen = set()
        duplicates = set(x['lineno'] for x in d if x['lineno'] in seen or seen.add(x['lineno']))
        return list(duplicates)

    # Method to search for messages with a specific line number and return their indexes
    def duplicate_lines_search(self, line):
        indexes = []
        for i, msg in enumerate(self.messages):
            if msg['lineno'] == line:
                indexes.append(i)
        return indexes

    
    # Function to print compiler messages
    def print_messages(self, one_line=True):
        # Sort the messages list by line number
        self.messages.sort(key=self.sort_by_lineno)
    
        # Find duplicate lines in the messages list
        duplicate_lines = self.duplicate_lines(self.messages)
    
        # Iterate over each duplicate line
        for line in duplicate_lines:
            # Find messages with the same line number as the current duplicate line
            common_line = self.duplicate_lines_search(line)
    
            # Check if there are more than 2 common lines
            if len(common_line) > 2:
                error_lines_messages = []
                warning_lines_messages = []
    
                # Separate error and warning messages
                for cline in common_line:
                    if "is_warning" in self.messages[cline]:
                        warning_lines_messages.append(self.messages[cline])
                    else:
                        error_lines_messages.append(self.messages[cline])
    
                k = 0
                # Assign messages to common lines alternating between error and warning messages
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
    
        # Iterate over each message in the sorted messages list
        for i, msg in enumerate(self.messages):
            if "is_warning" in msg:
                # Print the warning message in red if it is not empty
                if msg['message'] != "":
                    Colorprints.print_in_red(f"=> {msg['message']}")
            else:
                # Print the line number in cyan
                Colorprints.print_in_cyan(f"{msg['lineno']}: ", end="")
                
                if one_line and i+1 < len(self.messages) and self.messages[i]['lineno'] == self.messages[i+1]['lineno'] and self.messages[i+1]['message'] != "":
                    # Print the message in red if it is not empty and the next message has the same line number
                    Colorprints.print_in_red(f"{msg['message']}", end=" ")
                else:
                    # Print the message in red
                    Colorprints.print_in_red(f"{msg['message']}")
    

    # Function to add a message to the list of messages
    def add_message(self, message):
        # Check if the message is not already in the messages list
        if not message in self.messages:
            # Append the message to the messages list
            self.messages.append(message)
            
            # Update the error and warning counts based on the message type
            if not "is_warning" in message:
                # If the message is not a warning, increment the error count
                self.errors += 1 
            else:
                # If the message is a warning, increment the warning count
                message["message"] = message["message"]
                self.warnings += 1
    
    # Function used as the sorting key for the sort method
    def sort_by_lineno(self, msg):
        # Return the line number of the message dictionary
        return msg["lineno"]
    
