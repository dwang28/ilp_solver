import unittest
from sympy import *

from ..solver import *
from .test_case_lib import *
from .test_helper import *

cases = get_cases()
case = cases[-1]

class TestDebug(unittest.TestCase):

    def setUp(self): # This runs at the beginning of every test case
        self.result = case.solve(case.algo.implicit_enumeration)


    def test_all_solve_methods_get_same_result(self):

        result = run_all_algos(case, True)

        self.assertEqual(result['a'].obj_val, result['b'].obj_val)
        self.assertEqual(result['a'].obj_val, result['c'].obj_val)

    def test_objective_val_is_correct(self):

        if self.result.obj_val != -oo:
            direct_obj_val = case.get_obj_fn_val(case.obj_fn, self.result.var_vals)
            self.assertEqual(self.result.obj_val, direct_obj_val)

    def test_all_constraints_met(self):

        if self.result.obj_val != -oo:
            self.assertTrue(case.is_all_constraints_met(b=case.b, var_vals=self.result.var_vals, debug=True))


if __name__ == '__main__':
    unittest.main()
