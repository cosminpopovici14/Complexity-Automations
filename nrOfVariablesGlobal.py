import find


def variables_number(path, component):
    num_variables = 0
    c_files = find.check_valid_c(path)
    h_files = find.check_valid_h(path)
    for c_file in c_files:
        variables = find.find_variables(c_file, component)
        num_variables += len(variables)
    for h_file in h_files:
        variables = find.find_variables(h_file, component)
        num_variables += len(variables)
    return num_variables
