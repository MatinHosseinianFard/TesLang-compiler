import re
import config

class IR_optimizer(object):
    def __init__(self):
        pass

    def delete_mov_to_same_register(self):
        regex = ""
        for i in range(0, config.max_register_index_used_in_code+1):
            if i != config.max_register_index_used_in_code:
                regex +=f"(mov r{i}, r{i})|" 
            else:
                regex +=f"(mov r{i}, r{i})" 
        config.iR_code = re.sub(regex, "", config.iR_code)


    def delete_empty_lines_from_code(self):
        lines = config.iR_code.split("\n")
        non_empty_lines = [line for line in lines if line.strip() != ""]
        modified_code = ""
        for line in non_empty_lines:
            modified_code += line + "\n"

        #because only after keyword "ret", there should be an empty line
        config.iR_code = modified_code.replace("ret", "ret\n")


    def sort_indetation(self):
        output_code = ''

        indentation_level = 0

        for line in config.iR_code.split('\n'):
            line = line.strip()
            if line.startswith('proc') or line.startswith('main'):
                output_code += '    ' * indentation_level + line + '\n'
                indentation_level += 1
            elif line.startswith('ret'):
                output_code += '    ' * indentation_level + line + '\n'
                indentation_level -= 1
            else:
                output_code += '    ' * indentation_level + line + '\n'

        config.iR_code = output_code