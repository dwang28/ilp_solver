import unittest
from sympy import *

from ..solver import *
from .test_case_lib import *
from .test_helper import *

# cases = get_cases()
# case = cases[-1]

p402, p83, p199, p14, p145, p205, p390, p189, p471, p500 = symbols('p402 p83 p199 p14 p145 p205 p390 p189 p471 p500')

obj_fn = p14 + 12*p145 + p189 + 2*p199 + 3*p390 + p471 + 3*p83

b = [
    p402 <= 3,
    p83 <= 3,
    p199 + 9*p205 + 9*p471 <= 3,
    p14 <= 3,
    p145 <= 3,
    p390 <= 3,
    p189 <= 3,
    p500 <= 3,
    p145 + p402 <= 5,
    p14 + p199 + p205 + p390 + p471 + p500 + p83 <= 5,
    p189 <= 3,
    75*p14 + 40*p145 + 45*p189 + 55*p199 + 45*p205 + 60*p390 + 55*p402 + 50*p471 + 55*p500 + 50*p83 <= 1000,
    p14 + p145 + p189 + p199 + p205 + p390 + p402 + p471 + p500 + p83 <= 3,
    p14 + p145 + p189 + p199 + p205 + p390 + p402 + p471 + p500 + p83 >= 3
]

case = Binary_ILP_case([p402, p83, p199, p14, p145, p205, p390, p189, p471, p500], obj_fn, b)


class TestDebug(unittest.TestCase):

    def setUp(self): # This runs at the beginning of every test case
        self.result = case.solve(case.algo.implicit_enumeration)

    # def test_all_solve_methods_get_same_result(self):

    #     result = run_all_algos(case, True)

    #     self.assertEqual(result['a'].obj_val, result['b'].obj_val)
    #     self.assertEqual(result['a'].obj_val, result['c'].obj_val)

    # def test_objective_val_is_correct(self):

    #     if self.result.obj_val != -oo:
    #         direct_obj_val = case.get_obj_fn_val(case.obj_fn, self.result.var_vals)
    #         self.assertEqual(self.result.obj_val, direct_obj_val)

    def test_all_constraints_met(self):

        if self.result.obj_val != -oo:
            self.assertTrue(case.is_all_constraints_met(b=case.b, var_vals=self.result.var_vals, debug=True))


if __name__ == '__main__':
    unittest.main()
