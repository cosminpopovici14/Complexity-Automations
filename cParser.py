#this file contains helper fucntions for extracting data from c/h files ex func/variables defined
import re
import utilityFiles as Ufiles
def extract_c_functions(file_path, comp):
    """
    Extracts all function definitions from a C file, including macro-based functions,
    while excluding control structures like if, while, for, and switch.

    Args:
        file_path (str): Path to the C file.
        comp (str): Component name.

    Returns:
        dict: A dictionary mapping function names to their component.
    """
    # Improved regex to match FUNC(...) macros and standard function definitions
    function_pattern = re.compile(
        r'^\s*(?:FUNC\s*\(\s*([\w\s,\*]+)\s*,\s*[\w_]+\s*\)|([\w\s\*]+))\s+([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*'
    )

    # Exclude keywords that indicate control structures (not function definitions)
    control_keywords = {"if", "while", "for", "switch", "else"}

    function_names = {}
    functions = []
    in_function_declaration = False
    function_header = ""

    clean_lines = Ufiles.JustValidLines(file_path)  # Preprocess file

    for line in clean_lines:
        line = line.strip()
        # Skip preprocessor macros and variable definitions
        if line.startswith("#") or line.startswith("VAR("):
            continue

        # Ignore control structures
        if any(line.startswith(keyword + " ") for keyword in control_keywords):
            continue

        # Ignore function calls (lines ending in `;`)
        if line.endswith(";"):
            continue

        # Handle multi-line function definitions
        if in_function_declaration:
            function_header += " " + line
            if "{" in line:  # End of function declaration
                function_header = function_header.replace("{", "").strip()
                in_function_declaration = False
                match = function_pattern.match(function_header)
                if match:
                    return_type = match.group(1) or match.group(2)
                    function_name = match.group(3)
                    function_names[function_name] = comp
                    functions.append((return_type.strip(), function_name.strip()))
            continue

        # Match function definitions (without '{' yet)
        match = function_pattern.match(line)
        if match:
            function_name = match.group(3)

            # Exclude control structures that might accidentally match
            if function_name in control_keywords:
                continue

            in_function_declaration = True
            function_header = line
            continue

        # Check if this is the opening '{' of a function
        if in_function_declaration and "{" in line:
            in_function_declaration = False
            function_header = function_header.replace("{", "").strip()
            match = function_pattern.match(function_header)
            if match:
                return_type = match.group(1) or match.group(2)
                function_name = match.group(3)
                function_names[function_name] = comp
                functions.append((return_type.strip(), function_name.strip()))

    #print("Extracted functions:" + comp, function_names)
    #more info about func should be find in functions var
    return function_names

def extract_c_variables(file_path, comp):
    """
    Extracts all global variable definitions from a C file, excluding local variables inside functions.

    Args:
        file_path (str): Path to the C file.
        comp (str): Component name.

    Returns:
        dict: A dictionary mapping global variable names to their component.
    """
    var_pattern = re.compile(r'^\s*(?:VAR\s*\(\s*([\w\s\*]+)\s*,\s*[\w_]+\s*\)|([\w\s\*\[\]]+))\s+([\w_][\w\d]*)\s*(?:=\s*[^;]*)?;')
    variable_names = {}

    inside_function = 0  # Tracks function scope
    clean_lines = Ufiles.JustValidLines(file_path)  # Preprocess file

    for line in clean_lines:
        line = line.strip()

        # Track function scope
        if "{" in line:
            inside_function += 1
        if "}" in line:
            inside_function -= 1

        # Skip everything inside a function
        if inside_function > 0:
            continue

        # Match global variable declarations
        match = var_pattern.match(line)
        if match:
            variable_name = match.group(3)
            variable_names[variable_name] = comp

    #print("Extracted global variables:", variable_names)
    return variable_names


def extract_c_defines(file_path, comp):
    """
    Extracts all #define statements from a C file, excluding those followed by #include.

    Args:
        file_path (str): Path to the C file.
        comp (str): Component name.

    Returns:
        dict: A dictionary mapping define names to their component.
    """
    define_pattern = re.compile(r'^\s*#define\s+([\w_]+)')  # Match #define NAME
    define_names = {}

    clean_lines = Ufiles.JustValidLines(file_path)  # Preprocess file
    prev_define = None  # Store last valid define

    for i, line in enumerate(clean_lines):
        line = line.strip()

        # Check if it's a #define statement
        match = define_pattern.match(line)
        if match:
            prev_define = match.group(1)  # Store define name temporarily
            continue

        # Exclude if the next line is #include
        if prev_define and not line.startswith("#include"):
            define_names[prev_define] = comp

        prev_define = None  # Reset after checking

    print("Extracted defines:", define_names)
    return define_names
