import os
import find

def nr_vars(path, variable_files, component):
    components_variables = {}
    total_variables = 0

    c_files = find.check_valid_c(path)
    h_files = find.check_valid_h(path)

    for file in c_files + h_files:
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                for variable, comp in variable_files.items():
                    if variable in line and comp != component:
                        if comp not in components_variables:
                            components_variables[comp] = 0
                        components_variables[comp] += 1
                        total_variables += 1

    return components_variables, total_variables