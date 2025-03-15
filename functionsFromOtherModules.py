import os
import find


def JustValidLines(file_path):
    """
    Reads a C file and removes all comments.

    Args:
        file_path (str): Path to the C file.

    Returns:
        list: A list of lines without comments.
    """
    valid_lines = []
    in_multiline_comment = False  # Flag to track multi-line comments

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            stripped_line = line.strip()

            # Check if we are inside a multi-line comment
            if in_multiline_comment:
                if "*/" in stripped_line:
                    in_multiline_comment = False  # End of multi-line comment
                continue  # Skip this line

            # Remove single-line comments (// ...)
            if '//' in stripped_line:
                stripped_line = stripped_line.split('//', 1)[0].rstrip()

            # Check for multi-line comment start
            if "/*" in stripped_line:
                in_multiline_comment = True
                stripped_line = stripped_line.split("/*", 1)[0].rstrip()

            # Add valid (non-empty) lines
            if stripped_line:
                valid_lines.append(stripped_line)
    return valid_lines
def nr_functions(path, function_files, component):
    c_files = find.check_valid_c(path)
    components_functions = {}
    total_functions = 0

    for file in c_files:
        lines = JustValidLines(file)
        for line in lines:
            for function, comp in function_files.items():
                if function in line and comp != component:
                    total_functions += 1
                    if comp not in components_functions:
                        components_functions[comp] = 0
                    components_functions[comp] += 1

    return components_functions, total_functions