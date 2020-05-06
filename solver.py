#!/usr/bin/env python3

from sympy import *

class VarVal:
    def __init__(self, var, val):
        self.var = var # sympy symbol
        self.val = val # 0 or 1

    def __repr__(self): # for shell
        return self.get_print_string()

    def __str__(self): # for print
        return self.get_print_string()

    def get_print_string(self):
        return str((self.var, self.val))

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

        class Algo:
            def __init__(self):
                self.brutal_divide_and_conquer = 'brutal_divide_and_conquer'
                self.brutal_explicit_enumeration = 'brutal_explicit_enumeration'
                self.implicit_enumeration = 'implicit_enumeration'

        self.algo = Algo()

    def reset_counter(self):
        self.i = 0

    def get_run_count(self):
        return self.i

    def get_substitute_b(self, old_b, var, val):

        result = []

        for inEq in old_b:
            result.append(inEq.subs(var, val))

        return result

    def is_feasible(self, b, var_vals):

        for lessThanEq in b:
            lhs = lessThanEq.lhs
            for item in var_vals:
                lhs = lhs.subs(item.var, item.val)

            if lhs > lessThanEq.rhs:
                return False

        return True

    def get_obj_fn_val(self, obj_fn, var_vals):

        obj_val = obj_fn
        for item in var_vals:
            obj_val = obj_val.subs(item.var, item.val)

        return obj_val



    def solve(self, algo, print_run_count=False):

        variables = self.variables[:]
        obj_fn = self.obj_fn
        b = self.b[:]

        self.reset_counter()

        if algo == self.algo.brutal_divide_and_conquer:
            result = self.solve_by_brutal_divide_and_conquer(variables, obj_fn, b)

        if algo == self.algo.brutal_explicit_enumeration:
            result = self.solve_by_brutal_explicit_enumeration(variables, obj_fn, b)

        if algo == self.algo.implicit_enumeration:
            result = self.solve_by_implicit_enumeration(variables, obj_fn, b)

        if print_run_count:
            print("Run count", self.get_run_count())

        return result

    def solve_by_brutal_divide_and_conquer(self, variables, obj_fn, b):

        self.i += 1

        # if number of free vars is greater than 1, pick one var, update objective function and inequality constraints
        if len(variables) > 1:

            fix_var = variables[0] # modify vars list

            obj_zero = obj_fn.subs(fix_var, 0)
            b_zero = self.get_substitute_b(b, fix_var, 0)
            result_zero = self.solve_by_brutal_divide_and_conquer(variables[1:], obj_zero, b_zero)

            obj_one = obj_fn.subs(fix_var, 1)
            b_one = self.get_substitute_b(b, fix_var, 1)
            result_one = self.solve_by_brutal_divide_and_conquer(variables[1:], obj_one, b_one)


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

    def solve_by_brutal_explicit_enumeration(self, variables, obj_fn, b):

        print('solving by explicit enumeration')


    def sort_vars_by_priority_for_implicit_enumeration(self, variables):

        # to be implemented
        return variables

    def solve_by_implicit_enumeration(self, variables, obj_fn, b):

        self.i += 1

        best_result = Result(obj_val = -oo, var_vals = [])


        fix_var = variables.pop(0)


        # branch to fix_var = 0
        var_vals = [VarVal(fix_var, 0)]

        for var in variables:
            var_vals.append(VarVal(var, 0))

        if self.is_feasible(b, var_vals): # best case scenario
            obj_val = self.get_obj_fn_val(obj_fn, var_vals)
            return Result(obj_val, var_vals)

        elif len(variables)>0: # can be divided further

            obj_zero = obj_fn.subs(fix_var, 0)
            b_zero = self.get_substitute_b(b, fix_var, 0)
            result_zero = self.solve_by_brutal_divide_and_conquer(variables[:], obj_zero, b_zero)

            if result_zero.obj_val > best_result.obj_val:
                best_result = Result(result_zero.obj_val, [VarVal(fix_var, 0)] + result_zero.var_vals)

        # branch to fix_var = 1

        var_vals[0].val = 1

        if self.is_feasible(b, var_vals):
            obj_val = self.get_obj_fn_val(obj_fn, var_vals)

            if result_zero.obj_val > best_result.obj_val:
                best_result = Result(obj_val, var_vals)

        elif len(variables)>0:

            obj_one = obj_fn.subs(fix_var, 1)
            b_one = self.get_substitute_b(b, fix_var, 1)
            result_one = self.solve_by_brutal_divide_and_conquer(variables[:], obj_one, b_one)

            if result_one.obj_val > best_result.obj_val:
                best_result = Result(result_one.obj_val, [VarVal(fix_var, 1)] + result_one.var_vals)

        return best_result

if __name__ == '__main__':

    # Test case data
    x1, x2, x3, x4, x5 = symbols('x1, x2, x3, x4, x5')
    variables = [x1, x2, x3, x4, x5]

    objective_fn = -8*x1 -2*x2 - 4*x3 - 7*x4 - 5*x5 + 10  # expression

    # Constraints
    # b1, b2 are sympy expressions here
    b1 = -3*x1 - 3*x2 + x3 + 2*x4 + 3*x5 <= -2
    b2 = -5*x1 - 3*x2 - 2*x3 - x4 + x5 <= -4

    case1 = Binary_ILP_case(variables=variables, b=[b1, b2], obj_fn=objective_fn,  maximize=True)

    result = case1.solve(cases1.algo.implicit_enumeration, print_run_count=True)

