from sympy import *
from solver import *

x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = symbols('x1, x2, x3, x4, x5, x6, x7, x8, x9, x10')


# To do :
#
# Write test in json

class Case:

    def __init__(self, variables, obj_fn, b, expected_obj_val):

        # variables = variables
        self.case = Binary_ILP_case(variables, obj_fn, b)
        self.expected_obj_val = expected_obj_val

    def __repr__(self): # for shell
        return self.get_print_string()

    def __str__(self): # for print
        return self.get_print_string()

    def get_print_string(self):

        variables = ''

        for var in self.case.variables:
            variables += str(var) + ', '

        variables = variables[: -2]

        result = 'Case:'.ljust(10) + variables + '\n'
        result += 'Z:'.ljust(10) + str(self.case.obj_fn) + '\n\n'

        first_line = True
        for inEq in self.case.b:
            if first_line:
                result += 'b:'.ljust(10) + str(inEq) + '\n'
                first_line = False
            else:
                result += ''.ljust(10) + str(inEq) + '\n'

        result += '\n'
        result += 'Exp val:'.ljust(10) + str(self.expected_obj_val)

        return result

def get_cases():

    cases = []

    # 0
    obj_fn = -8*x1 - x2 - x3 - 5*x4 - 10*x5 + 19 # sympy expression
    b = [-7*x4 <= 9,    2*x2 - 6*x4 - 3*x5 <= -1,  10*x1 - 3*x2 - 7*x3 <= 15]
    cases.append(Case([x1, x2, x3, x4, x5], obj_fn, b, expected_obj_val = 14))

    # 1
    b = [-3*x1 - 3*x2 + x3 + 2*x4 + 3*x5 <= -2, -5*x1 - 3*x2 - 2*x3 - x4 + x5 <= -4]
    obj_fn = -8*x1 + -2*x2 - 4*x3 - 7*x4 - 5*x5 + 10
    cases.append(Case([x1, x2, x3, x4, x5], obj_fn, b, expected_obj_val = 4))

    return cases


if __name__ == '__main__':
    cases = get_cases()

    print(cases[0])