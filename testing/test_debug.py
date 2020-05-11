import unittest
from sympy import *

from ..solver import *
from .test_case_lib import *
from .test_helper import *

cases = get_cases()

class TestDebug(unittest.TestCase):

    def test_all_solve_methods_get_same_result(self):

        case = cases[-1]

        result = run_all_algos(case, True)

        self.assertEqual(result['a'].obj_val, result['b'].obj_val)
        self.assertEqual(result['a'].obj_val, result['c'].obj_val)

if __name__ == '__main__':
    unittest.main()
