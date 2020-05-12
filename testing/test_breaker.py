import unittest
import random

from sympy import *
from ..solver import *
from .test_helper import *

class TestRandomData(unittest.TestCase):

    def get_random_int(self, lower_bound, upper_bound, allow_zero=False):

        num = random.randint(lower_bound, upper_bound)

        if allow_zero:
            return num

        else:
            while num == 0:
                num = random.randint(lower_bound, upper_bound)

        return num


    def gen_vars(self, number_of_vars):

        variables = []

        for i in range(0, number_of_vars):
            variables.append(Symbol('x' + str(i+1)))

        return variables

    def gen_obj_fn(self, variables):

        c = self.get_random_int(-20, 20, allow_zero=True)

        obj_fn = c

        for i in range(0, len(variables)):

            coeff = 0
            while coeff==0:
                coeff = self.get_random_int(-10, 10)

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
            number_of_vars_in_constraint = self.get_random_int(1, len(variables))

            on_off = self.get_binary_list(len(variables), number_of_vars_in_constraint)

            for j in range(0, len(variables)):
                expr += self.get_random_int(-10, 10) * on_off[j] * variables[j]


            inEqType = self.get_random_int(0, 3, allow_zero=True)

            if inEqType == 0:
                b.append(expr < self.get_random_int(-20, 20, allow_zero=True))

            elif inEqType == 1:
                b.append(expr <= self.get_random_int(-20, 20, allow_zero=True))

            elif inEqType == 2:
                b.append(expr > self.get_random_int(-20, 20, allow_zero=True))

            else:
                b.append(expr >= self.get_random_int(-20, 20, allow_zero=True))

        return b

    def gen_new_case(self, number_of_vars, number_of_constraints):

        variables = self.gen_vars(number_of_vars)
        obj_fn = self.gen_obj_fn(variables)
        b = self.gen_constraints(variables, number_of_constraints)

        return Binary_ILP_case(variables, obj_fn, b)


    def test_run(self):

        total_runs = 100
        debug = False

        i=0
        while i <= total_runs:

            print('start test ' + str(i) + '/' + str(total_runs) + '... ')

            # build a new case
            number_of_vars = self.get_random_int(2, 6)
            number_of_constraints = self.get_random_int(1, 3)

            try:
                case = self.gen_new_case(number_of_vars, number_of_constraints)
                result = run_all_algos(case, debug=debug)

                self.assertEqual(result['a'].obj_val, result['b'].obj_val)
                self.assertEqual(result['a'].obj_val, result['c'].obj_val)

                self.assertTrue(case.is_feasible(case.b, result['c'].var_vals, debug=True))

            except Exception as e:
                print(case)
                raise e

            print('test passed\n')
            i +=1

if __name__ == '__main__':
    unittest.main()