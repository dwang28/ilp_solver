import unittest
import random

from sympy import *
from ..solver import *

# To do:
#   if test failed:
#       print json

class TestRandomData(unittest.TestCase):


    def gen_vars(self, number_of_vars):

        variables = []

        for i in range(0, number_of_vars):
            variables.append(Symbol('x' + str(i+1)))

        return variables

    def gen_obj_fn(self, variables):

        c = random.randint(-20, 20)

        obj_fn = c

        for i in range(0, len(variables)):

            coeff = random.randint(-10, 10)
            obj_fn += coeff * variables[i]

        return obj_fn

    def get_binary_list(self, number_of_items, number_of_ones):

        l = [0] * (number_of_items - number_of_ones) + [1] * number_of_ones

        random.shuffle(l)
        return l

    def gen_constraints(self, variables, number_of_constraints):

        b = []

        for i in range(0, number_of_constraints):

            expr = 0
            # generate a single lessThan inequlaity equation
            number_of_vars_in_constraint = random.randint(1, len(variables))
            on_off = self.get_binary_list(len(variables), number_of_vars_in_constraint)

            for j in range(0, len(variables)):
                expr += random.randint(-10, 10) * on_off[j] * variables[j]

            b.append(expr <= random.randint(-20, 20))

        return b

    def gen_new_case(self, number_of_vars, number_of_constraints):

        variables = self.gen_vars(number_of_vars)
        obj_fn = self.gen_obj_fn(variables)
        b = self.gen_constraints(variables, number_of_constraints)

        # print('case', variables, obj_fn)
        # print('b', b)
        return Binary_ILP_case(variables, obj_fn, b)


    # def run_case(self, case):

    #     print('case symbols: ', case.variables)
    #     print('obj_fn: ', case.obj_fn)
    #     print('b: ', case.b)

    #     a = case.solve(case.algo.brutal_explicit_enumeration)
    #     b = case.solve(case.algo.brutal_divide_and_conquer)
    #     c = case.solve(case.algo.implicit_enumeration)

    #     self.assertEqual(a.obj_val, 14)
    #     self.assertEqual(a.obj_val, b.obj_val)
    #     self.assertEqual(a.obj_val, c.obj_val)

    #     print('Result: ', c)



    def test_run(self):

        number_of_runs = 10

        while number_of_runs > 0:

            number_of_vars = random.randint(2, 6)
            number_of_constraints = random.randint(1, 3)
            case = self.gen_new_case(number_of_vars, number_of_constraints)

            print('case symbols: ', case.variables)
            print('obj_fn: ', case.obj_fn)
            print('b: ', case.b)

            a = case.solve(case.algo.brutal_explicit_enumeration)
            b = case.solve(case.algo.brutal_divide_and_conquer)
            c = case.solve(case.algo.implicit_enumeration)

            # self.assertEqual(a.obj_val, 4)
            self.assertEqual(a.obj_val, b.obj_val)
            self.assertEqual(a.obj_val, c.obj_val)

            print('result: ', a)

            number_of_runs -=1

    # def test_debug(self):

    #     x1, x2, x3, x4, x5 = symbols('x1, x2, x3, x4, x5')
    #     obj_fn = -8*x1 - x2 - x3 - 5*x4 - 10*x5 + 19
    #     b = [-7*x4 <= 9, 2*x2 - 6*x4 - 3*x5 <= -1, 10*x1 - 3*x2 - 7*x3 <= 15]

    #     case = Binary_ILP_case([x1, x2, x3, x4, x5], obj_fn, b)

    #     self.run_case(case)


if __name__ == '__main__':
    unittest.main()