import unittest

from sympy import *
from solver import *
from test_case_lib import *


# book example
# x1, x2, x3, x4, x5 = symbols('x1, x2, x3, x4, x5')
# b1 = -3*x1 - 3*x2 + x3 + 2*x4 + 3*x5 <= -2
# b2 = -5*x1 - 3*x2 - 2*x3 - x4 + x5 <= -4
# objective_fn = -8*x1 + -2*x2 - 4*x3 - 7*x4 - 5*x5 + 10


# dataset = [
#     Binary_ILP_case(
#         variables = [x1, x2, x3, x4, x5],
#         b = [b1, b2],
#         obj_fn = objective_fn
#     )
# ]

cases = get_cases()
case = cases[1].case

class TestSolveMethods(unittest.TestCase):

    # def setUp(self):
    #     print("This run at beginning of each test method")

    def test_is_feasible_fn(self):

        variables = case.variables[:]

        self.assertTrue(case.is_feasible(case.b, [VarVal(variables[0], 0), VarVal(variables[1], 1), VarVal(variables[2], 1), VarVal(variables[3], 0), VarVal(variables[4], 0)]))
        self.assertFalse(case.is_feasible(case.b, [VarVal(variables[0], 0), VarVal(variables[1], 0), VarVal(variables[2], 0), VarVal(variables[3], 0), VarVal(variables[4], 0)]))

    def test_get_obj_fn_val(self):

        obj_fn = -8*x1 - 2*x2 - 4*x3 - 7*x4 - 5*x5 + 10
        var_vals = [
            VarVal(x1, 1),
            VarVal(x2, 0),
            VarVal(x3, 0),
            VarVal(x4, 0),
            VarVal(x5, 0),
        ]

        self.assertEqual(case.get_obj_fn_val(obj_fn, var_vals), 2)


    def test_pre_proces_fn(self):

        c = Binary_ILP_case(
            variables = [x1, x2, x3, x4, x5],
            obj_fn = -8*x1 - x2 - x3 - 5*x4 + 10*x5 + 19,
            b = [x5 <=2]
        )

        sample = c.get_preprocessed_result()
        self.assertEqual(sample['_obj_fn'], -8*c._(x1) - c._(x2) - c._(x3) - 5*c._(x4) - 10*c._(x5) + 29)
        self.assertEqual(sample['_b'][0], 1 - c._(x5) <= 2)


    def test_all_solve_methods_get_same_result(self):

        case = cases[1].case
        # print('case', cases[1])

        a = case.solve(case.algo.brutal_explicit_enumeration)

        b = case.solve(case.algo.brutal_divide_and_conquer)
        c = case.solve(case.algo.implicit_enumeration)

        # print('a result', a)
        # print('b result', b)
        # print('c result', c)


        self.assertEqual(a.obj_val, 4)
        self.assertEqual(a.obj_val, b.obj_val)
        self.assertEqual(a.obj_val, c.obj_val)

if __name__ == '__main__':
    unittest.main()