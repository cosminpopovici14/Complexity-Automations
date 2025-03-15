import os
import re

def JustValidLines(file_path):
    """
    Reads a C file, removes only comments and unnecessary newlines while preserving executable code.

    Args:
        file_path (str): Path to the C file.

    Returns:
        list: A list of valid code lines without comments and excessive newlines.
    """
    valid_lines = []
    inside_block_comment = False
    previous_was_code = False  # Track if the last valid line was meaningful

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            stripped_line = line.strip()

            # Handle block comments while preserving code before/after
            if "/*" in stripped_line:
                inside_block_comment = True
                before_comment = stripped_line.split("/*")[0].strip()  # Keep code before comment
                if "*/" in stripped_line:  # Handle one-line block comments
                    inside_block_comment = False
                    after_comment = stripped_line.split("*/")[-1].strip()
                    stripped_line = before_comment + " " + after_comment
                else:
                    stripped_line = before_comment  # Remove everything after `/*`
            elif inside_block_comment:
                if "*/" in stripped_line:
                    inside_block_comment = False
                continue  # Skip lines inside block comments

            # Remove inline comments (// ...)
            stripped_line = re.sub(r'//.*', '', stripped_line).strip()

            # Skip empty lines unless the last valid line was meaningful
            if not stripped_line:
                previous_was_code = False
                continue

            # Ensure newlines after key constructs like `;`, `#define`, `#include`
            if re.match(r'.*;$', stripped_line) or stripped_line.startswith(("#define", "#include")):
                valid_lines.append(stripped_line)
                previous_was_code = True
            else:
                # Avoid unnecessary blank lines but keep proper spacing
                if previous_was_code:
                    valid_lines.append(stripped_line)
                else:
                    valid_lines.append(stripped_line)
                previous_was_code = True

    return valid_lines



def check_valid_c(path):
    valid_paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if(file_path.__contains__("autosar_rtw" or "template")):
                file_ignored = file_path
            else:
                if(file_path.endswith(".c")):
                   valid_paths.append(file_path)
    return valid_paths

def check_valid_h(path):
    valid_paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if(file_path.__contains__("autosar_rtw" or "template")):
                file_ignored = file_path
            else:
                if(file_path.endswith(".h")):
                   valid_paths.append(file_path)
    return valid_paths

def get_comp_headers(path, component):
    """
    parses the comp folder and gets all valid headers.

    Args:
        path (str): Path to the component folder.
        component (str): name of the component

    Returns:
        list: A list of headers that are contained in the component
    """
    headers_components = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".h"):
                file_path = os.path.join(root, file)
                if (file_path.__contains__("autosar_rtw" or "template")):
                    file_ignored = file_path
                else:
                    headers_components[file] = component
    return headers_components

