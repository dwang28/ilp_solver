#!/usr/bin/env python3

from sympy import *

class VarVal:
    def __init__(self, var, val):
        self.var = var # sympy symbol
        self.val = val # 0 or 1

class Result:
    def __init__(self, obj_val, var_vals):
        self.obj_val = obj_val # numbers or -oo
        self.var_vals = var_vals # list of VarVal obj

    def __repr__(self): # for shell
        return self.get_print_string()

    def __str__(self): # for print
        return self.get_print_string()

    def get_print_string(self):

        vars_list = []

        for item in self.var_vals:
            vars_list.append((item.var, item.val)) #for easy reading, keep it short as a list

        result_obj = {
            'obj_val': self.obj_val,
            'var_vals' : vars_list
        }

        return str(result_obj)


class Binary_ILP_case:
    # variables
    # obj_fn [sympy expression]: the function to maximize or minimize
    # b: array of constraints
    def __init__(self, variables, obj_fn, b, maximize=True):

        # init
        self.variables = variables
        self.obj_fn = obj_fn
        self.b = b # all inEquality functions must be less than for now.

        self.i = 0

        self.goal = 'maximize'
        if(maximize == False):
            self.goal = 'minimize'

        # print(self.b)

    def reset_counter(self):
        self.i = 0

    def get_run_count(self):
        return self.i

    def solve(self, debug=False):

    	print("Solving ILP: ", self.obj_fn, "\n")

    	# for var in self.vars:

    	# 	print(var)
    	# 	a = Poly(self.obj_fn, var)
    	# 	print('Coef:', a.coeffs())
    	# 	print('All coef', a.all_coeffs())

    def get_substitute_b(self, old_b, var, val):

        result = []

        for inEq in old_b:
            result.append(inEq.subs(var, val))

        return result

    def is_feasible(self, b, var_vals):

        print('check feasible', b)

        for lessThanEq in b:
            lhs = lessThanEq.lhs
            for item in var_vals:
                print('subs var:', item.var, item.val)
                lhs = lhs.subs(item.var, item.val)
                print('updated lhs', lhs)


            if lhs > lessThanEq.rhs:
                return False

        return True


    def solve_by_brutal_divide_and_conquer(self, variables=None, obj_fn=None, b=None):

        self.i += 1

        if variables == None:
            variables = self.variables[:]

        if obj_fn == None:
            obj_fn = self.obj_fn

        if b ==None:
            b = self.b[:]

        # print('vars:', variables)
        # print('obj fn:', obj_fn)
        # print('b:', b)

        # if number of free vars is greater than 1, pick one var, update objective function and inequality constraints
        if(len(variables) > 1):

            fix_var = variables[0] # modify vars list

            # print('vars:', variables)
            # print('fix_var:', variables)
            # print('obj fn:', obj_fn)


            obj_zero = obj_fn.subs(fix_var, 0)
            b_zero = self.get_substitute_b(b, fix_var, 0)
            result_zero = self.solve_by_brutal_divide_and_conquer(variables[1:], obj_zero, b_zero)

            obj_one = obj_fn.subs(fix_var, 1)
            b_one = self.get_substitute_b(b, fix_var, 1)
            result_one = self.solve_by_brutal_divide_and_conquer(variables[1:], obj_one, b_one)

            # print('given x1 is 0', obj_zero)
            # print('b_zero', b_zero)
            # print('given x1 is 1', obj_one)
            # print('b_one', b_one)

            if result_zero.obj_val > result_one.obj_val:
                return Result(
                    obj_val = result_zero.obj_val,
                    var_vals= [VarVal(var = fix_var, val = 0)] + result_zero.var_vals
                )
            else:
                # print('result_one', fix_var, obj_fn)
                return Result(
                    obj_val = result_one.obj_val,
                    var_vals= [VarVal(var = fix_var, val = 1)] + result_one.var_vals
                )

        else: # base case
            # print('Base case: now only 1 var left', variables)
            # print('obj_fn', obj_fn)
            # print('b', b)

            var = variables[0]

            is_feasible_zero = self.is_feasible(b, [VarVal(var, 0)])

            if not is_feasible_zero:
                obj_val_zero = -oo
            else:
                obj_val_zero = obj_fn.subs(var, 0)

            is_feasible_one = self.is_feasible(b, [VarVal(var, 1)])

            if not is_feasible_one:
                obj_val_one = -oo
            else:
                obj_val_one = obj_fn.subs(var, 1)

            if obj_val_zero > obj_val_one:
                result = Result(obj_val = obj_val_zero, var_vals = [ VarVal(var = var, val = 0) ])
            else:
                result = Result(obj_val = obj_val_one, var_vals = [ VarVal(var = var, val = 1) ])

            # print('result', result)
            return result


    def sort_vars_by_priority(self):

        # to be implemented
        return self.variables

    def solve_by_implicit_enumeration(self, variables=None, obj_fn=None, b=None):
        # set default vars
        if variables == None:
            variables = self.variables[:]

        if obj_fn == None:
            obj_fn = self.obj_fn

        if b ==None:
            b = self.b[:]


        stopper = 50
        best_obj_val = -oo
        var_vals = ()


        print('test result', test)

        while len(variables) > 0:

            fix_var = variables.pop(0)


            stopper -= 1
            if stopper == 0:
                return

        # branch to fix_var = 0


        # branch to fix_var = 1

        # Thsi is going to be a while loop

        # When set all free variables to 0, is feasible?
            # calculate best case z in this scenario
            # is best case z better than global best case z?
                # update global best case z

            # else
                # do nothing
        # branch further



if __name__ == '__main__':

    # Test case data
    x1, x2, x3, x4, x5 = symbols('x1, x2, x3, x4, x5')
    variables = [x1, x2, x3, x4, x5]

    objective_fn = -8*x1 + -2*x2 - 4*x3 - 7*x4 - 5*x5 + 10  # expression

    # Constraints
    # b1, b2 are sympy expressions here
    b1 = -3*x1 - 3*x2 + x3 + 2*x4 + 3*x5 <= -2
    b2 = -5*x1 - 3*x2 - 2*x3 - x4 + x5 <= -4

    case1 = Binary_ILP_case(variables=variables, b=[b1, b2], obj_fn=objective_fn,  maximize=True)
    # result = case1.solve_by_brutal_divide_and_conquer()
    # print("Run count", case1.get_run_count())
    # print("Result - Brutal.divide and conquer: ", result)

    case1.reset_counter()
    result = case1.solve_by_implicit_enumeration()
