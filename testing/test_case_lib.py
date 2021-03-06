from sympy import *
from ..solver import *

x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = symbols('x1, x2, x3, x4, x5, x6, x7, x8, x9, x10')

def _get_vars_from_obj_fn(obj_fn):

    vars_in_obj_fn = []
    obj_args = obj_fn.args

    for expr in obj_args:
        if not isinstance(expr, numbers.Integer):

            if not isinstance(expr, symbol.Symbol):
                var = expr.args[1]
            else:
                var = expr

            vars_in_obj_fn.append(var)

    sorted_variables = []
    for var in [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10]:

        if var in vars_in_obj_fn:
            sorted_variables.append(var)

    return sorted_variables

def get_cases():

    cases = []

    for case in all_cases:
        variables = _get_vars_from_obj_fn(case['obj_fn'])
        cases.append(Binary_ILP_case(variables, case['obj_fn'], case['b'], maximize=True, expected_obj_val=case['obj_val']))

    return cases

all_cases = [{
    # 0 book example
    'obj_fn': -8*x1 + -2*x2 - 4*x3 - 7*x4 - 5*x5 + 10,
    'b': [-3*x1 - 3*x2 + x3 + 2*x4 + 3*x5 <= -2, -5*x1 - 3*x2 - 2*x3 - x4 + x5 <= -4],
    'obj_val': 4

},{
    # 1
    'obj_fn': -8*x1 - x2 - x3 - 5*x4 - 10*x5 + 19,
    'b': [-7*x4 <= 9,    2*x2 - 6*x4 - 3*x5 <= -1,  10*x1 - 3*x2 - 7*x3 <= 15],
    'obj_val': 14
},{
    # 2 with positive coefficient in obj_fn z
    'obj_fn': -8*x1 - x2 - x3 - 5*x4 + 10*x5 + 19,
    'b': [x5 <=2],
    'obj_val': 29
},{
    # 3
    'obj_fn': 10*x1 - 10*x2 - 9*x3 - 4*x4 + 8*x5 - 20,
    'b': [-8*x2 + 9*x3 - 4*x4 <= 5, -2*x2 + 10*x4 + 7*x5 <= -11, -7*x2 <= 4],
    'obj_val': -oo
},{
    # 4
    'obj_fn': 6*x1 + 6*x2 + 6,
    'b': [-6*x1 - 2*x2 <= -9, 2*x1 + x2 <= 20],
    'obj_val': -oo
},{
    # 5
    'obj_fn': -5*x1 + 6*x2 + 6,
    'b': [x1 + x2 >=2],
    'obj_val': 7
},{
    # 6
    'obj_fn': 8*x1 - 10*x2 + 7*x3 - 9*x4 - 3*x5 + 5*x6 + 1,
    'b': [ 6*x1 - 8*x3 <= -16, x1 - 6*x2 - 3*x3 + 9*x5 <= -15, 7*x5 <= -12],
    'obj_val': -oo
},{
    # 7
    'obj_fn': 3*x1 - 6*x2 + 6*x3 - 6*x4 - 20,
    'b': [ x2 - 5*x3 - 2*x4 >= -2,  -x2 - 8*x4 < 10,  10*x2 < 0],
    'obj_val': -oo
},{
    # 9
    'obj_fn': -4*x1 - 4*x2 - 6*x3 - 4*x4 + x5 + 5*x6 - 2,
    'b': [ 9*x2 - 10*x6 <= -10],
    'obj_val': 4
}]


if __name__ == '__main__':
    cases = get_cases()
    print(cases[0])