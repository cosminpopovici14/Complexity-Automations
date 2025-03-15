#this file contains helping functions for checking the usage of fucntions/variables between components

import re
import utilityFiles as Ufiles

def nr_external_headers(path, headers_components, component):
    """
    :param path: path to component
    :param headers_components: a dictionary type(HEADER_DEFINED_IN_COMPX:COMPX)
    :param component: name of the component
    :return: number of headers used from other components
    """
    headers_number = 0
    c_files = Ufiles.check_valid_c(path)

    for c_file in c_files:
        with open(c_file, 'r') as f:
            for line in f:
                match = re.search(r'#include\s+"([^"]+)"', line)
                if match:
                    header_name = match.group(1)
                    if header_name in headers_components and component != headers_components[header_name]:
                        headers_number += 1

    return headers_number
def count_external_function_usage(path, function_defines, component):
    """
    Counts the number of functions used from other components in a list of C files.
    It considers only one usage per function, even if a function is called multiple times.

    Args:
        path  : path to the verified component
        function_defines (dict): A dictionary mapping function names to the components where they are defined.
        component (str): The name of the component for the provided C files.

    Returns:
        dict: A dictionary mapping components to the count of functions used from those components.
        total_functions : nr of functions from other components called from our component
    """
    external_function_usage = {}

    # Regular expression to match function calls with parameters, considering variations
    function_call_pattern = re.compile(r'\b([a-zA-Z_][\w]*)\s*\([^)]*\)\s*(?:;|\{|\s*$)')

    # Get all C files from the component
    c_files = Ufiles.check_valid_c(path)

    # List to store all function call matches
    all_function_calls = []

    #total number of calls made to functions from other modules
    total_functions = 0

    # Iterate over each C file
    for file_path in c_files:
        lines = Ufiles.JustValidLines(file_path)
        # State to track multi-line function calls
        multi_line_function = ""
        inside_function_call = False

        # Iterate through each line to accumulate function calls (single and multi-line)
        for line in lines:
            line = line.strip()

            # Skip control flow statements such as if, while, for, etc.
            if any(line.startswith(keyword) for keyword in ['if', 'while', 'for', 'switch']):
                continue

            # If we're inside a multi-line function call, accumulate the lines
            if inside_function_call:
                multi_line_function += " " + line
                # Check if the function call has ended (ends with ')')
                if multi_line_function.endswith(")"):
                    matches = function_call_pattern.findall(multi_line_function)
                    for function_name in matches:
                        all_function_calls.append(function_name)
                    inside_function_call = False
                    multi_line_function = ""  # Reset for the next possible multi-line function

            # Match function calls in the current line
            matches = function_call_pattern.findall(line)

            # If a match is found, check if it's a multi-line function call
            if matches:
                for function_name in matches:
                    # Exclude function definitions (e.g., void, int return types)
                    if function_name and not line.startswith(('void', 'int', 'char', 'float', 'double', 'long', 'short')):
                        all_function_calls.append(function_name)
                    # If the function call isn't complete (i.e., doesn't have a closing parenthesis), it's multi-line
                    if not line.strip().endswith(')'):
                        inside_function_call = True
                        multi_line_function = line.strip()

    # Now process the collected function calls
    called_functions = set()
    for function_name in all_function_calls:
        if function_name in function_defines:
            defining_component = function_defines[function_name]
            if defining_component != component:  # Only count if it's from another component
                called_functions.add(defining_component)

    # Count the functions called from other components
    for other_component in called_functions:
        total_functions += 1
        if other_component in external_function_usage:
            external_function_usage[other_component] += 1
        else:
            external_function_usage[other_component] = 1

    #print(f"{component} funcUsage:: {external_function_usage}")
    return external_function_usage, total_functions



def count_external_variable_usage(path, variable_defines, component):
    """
    Counts the number of variables used from other components in a list of C files.
    It considers only one usage per variable, even if a variable is used multiple times.

    Args:
        path (str): Path to the component directory.
        variable_defines (dict): A dictionary mapping variable names to the components where they are defined.
        component (str): The name of the component for the provided C files.

    Returns:
        dict: A dictionary mapping components to the count of variables used from those components.
    """
    external_variable_usage = {}
    total_external_variables_used = 0

    # Regular expression to match variable usage (excluding function definitions)
    variable_usage_pattern = re.compile(r'\b([a-zA-Z_][\w]*)\b')

    # Get all C files from the component
    c_files = Ufiles.check_valid_c(path)

    # Iterate over each C file
    for file_path in c_files:
        lines = Ufiles.JustValidLines(file_path)
        # Set to store all unique variable names that are used from other components
        all_used_variables = set()

        for line in lines:
            line = line.strip()
            print(line)

            # Match variable usage in the line (excluding function definitions)
            matches = variable_usage_pattern.findall(line)
            all_used_variables.update(matches)  # Add matches to the set (ensures uniqueness)

        # Now process the accumulated matches at the end of the line processing
        used_variables_from_other_components = set()

        for variable_name in all_used_variables:
            # Check if the variable is defined in another component
            if variable_name in variable_defines:
                defining_component = variable_defines[variable_name]
                if defining_component != component:  # Only count if it's from another component
                    used_variables_from_other_components.add(defining_component)

        # Count the variables used from other components
        for other_component in used_variables_from_other_components:
            total_external_variables_used += 1
            if other_component in external_variable_usage:
                external_variable_usage[other_component] += 1
            else:
                external_variable_usage[other_component] = 1

    print(component, " VarUsage::", external_variable_usage)
    return external_variable_usage, total_external_variables_used




