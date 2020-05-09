from sympy import *
from solver import *

x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = symbols('x1, x2, x3, x4, x5, x6, x7, x8, x9, x10')



class Case:

    def __init__(self, variables, obj_fn, b, expected_obj_val):

        self.case = Binary_ILP_case(variables, obj_fn, b)
        self.expected_obj_val = expected_obj_val

def get_cases():

    cases = []

    obj_fn = -8*x1 - x2 - x3 - 5*x4 - 10*x5 + 19
    b = [-7*x4 <= 9,    2*x2 - 6*x4 - 3*x5 <= -1,  10*x1 - 3*x2 - 7*x3 <= 15]
    cases.append(Case([x1, x2, x3, x4, x5], obj_fn, b, expected_obj_val = 14))

    return cases


print(get_cases()[0].case)