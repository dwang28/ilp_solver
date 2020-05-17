import unittest
from sympy import *

from ..solver import *
from .test_case_lib import *
from .test_helper import *

cases = get_cases()

test_call_cases = True
isDebugMode = False


class TestSolveMethods(unittest.TestCase):

    def test_is_feasible_fn(self):

        case = cases[0]
        variables = case.variables[:]

        self.assertTrue(case.is_feasible(case.b, [VarVal(variables[0], 0), VarVal(variables[1], 1), VarVal(variables[2], 1), VarVal(variables[3], 0), VarVal(variables[4], 0)]))
        self.assertFalse(case.is_feasible(case.b, [VarVal(variables[0], 0), VarVal(variables[1], 0), VarVal(variables[2], 0), VarVal(variables[3], 0), VarVal(variables[4], 0)]))


    def test_get_obj_fn_val(self):

        case = cases[0]

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

        c = cases[2]

        sample = c.get_preprocessed_result()
        self.assertEqual(sample['_obj_fn'], -8*c._(x1) - c._(x2) - c._(x3) - 5*c._(x4) - 10*c._(x5) + 29)
        self.assertEqual(sample['_b'][0], 1 - c._(x5) <= 2)


    def test_all_solve_methods_get_same_result(self):

        if test_call_cases:

            for case in cases:
                result = run_all_algos(case, debug=isDebugMode)

                self.assertEqual(result['a'].obj_val, result['b'].obj_val)
                self.assertEqual(result['a'].obj_val, result['c'].obj_val)
                self.assertEqual(result['a'].obj_val, case.expected_obj_val)

if __name__ == '__main__':
    unittest.main()
