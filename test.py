import unittest

from sympy import *
from solver import *


# Assertion types

    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)


# book example
x1, x2, x3, x4, x5 = symbols('x1, x2, x3, x4, x5')
b1 = -3*x1 - 3*x2 + x3 + 2*x4 + 3*x5 <= -2
b2 = -5*x1 - 3*x2 - 2*x3 - x4 + x5 <= -4
objective_fn = -8*x1 + -2*x2 - 4*x3 - 7*x4 - 5*x5 + 10  # sympy expression


dataset = [
    Binary_ILP_case(
        variables = [x1, x2, x3, x4, x5],
        b = [b1, b2],
        obj_fn = objective_fn
    )
]

class TestStringMethods(unittest.TestCase):

    # def setUp(self):
    #     print("This run at beginning of each test method")


    def test_is_feasible_method(self):

        case = dataset[0]
        variables = case.variables[:]

        self.assertTrue(case.is_feasible(case.b, [VarVal(variables[0], 0), VarVal(variables[1], 1), VarVal(variables[2], 1), VarVal(variables[3], 0), VarVal(variables[4], 0)]))
        self.assertFalse(case.is_feasible(case.b, [VarVal(variables[0], 0), VarVal(variables[1], 0), VarVal(variables[2], 0), VarVal(variables[3], 0), VarVal(variables[4], 0)]))



if __name__ == '__main__':
    unittest.main()