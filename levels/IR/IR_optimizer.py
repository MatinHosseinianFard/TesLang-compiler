import re
import config


class IR_optimizer(object):
    def __init__(self):
        pass

    def delete_mov_to_same_register(self):
        # Define a regular expression pattern string
        regex = ""

        # Iterate over the range from 0 to the maximum register index used in the code
        for i in range(0, config.max_register_index_used_in_code+1):
            if i != config.max_register_index_used_in_code:
                # Append pattern for "mov r{i}, r{i}" to the regex string
                regex += f"(mov r{i}, r{i})|"
            else:
                # Append pattern for "mov r{i}, r{i}" to the regex string without "|" at the end
                regex += f"(mov r{i}, r{i})"

        # Replace occurrences of the regex pattern with an empty string in the iR_code
        config.iR_code = re.sub(regex, "", config.iR_code)

    def delete_empty_lines_from_code(self):
        # Split the iR_code into individual lines
        lines = config.iR_code.split("\n")

        # Create a list of non-empty lines by filtering out lines that are empty or contain only whitespace characters
        non_empty_lines = [line for line in lines if line.strip() != ""]

        # Concatenate the non-empty lines to create a modified code string
        modified_code = ""
        for line in non_empty_lines:
            modified_code += line + "\n"

        # Replace all occurrences of "ret" with "ret\n" to ensure there is an empty line after "ret"
        config.iR_code = modified_code.replace("ret", "ret\n")

    def sort_indetation(self):
        # Initialize an empty string to store the output code
        output_code = ''

        # Initialize the indentation level to 0
        indentation_level = 0

        # Iterate over each line in the iR_code
        for line in config.iR_code.split('\n'):
            line = line.strip()

            if line.startswith('proc') or line.startswith('main'):
                # Add the line to the output code with the current indentation level
                output_code += '    ' * indentation_level + line + '\n'

                # Increase the indentation level by 1
                indentation_level += 1

            elif line.startswith('ret'):
                # Add the line to the output code with the current indentation level
                output_code += '    ' * indentation_level + line + '\n'

                # Decrease the indentation level by 1
                indentation_level -= 1

            else:
                # Add the line to the output code with the current indentation level
                output_code += '    ' * indentation_level + line + '\n'

        # Update the iR_code with the sorted and indented code
        config.iR_code = output_code
