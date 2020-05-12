#!/usr/bin/env python3
from sympy import *
from itertools import product

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

class VarRef:
    def __init__(self, counter_part, isReverse):
        self.counter_part = counter_part # sympy symbol, example: the counter part of x1 should be a sympy symbold _x1
        self.isReverse = isReverse # if true, x1 = 1 - _x1

    def __repr__(self): # for shell
        return self.get_print_string()

    def __str__(self): # for print
        return self.get_print_string()

    def get_print_string(self):
        return str((self.counter_part, 'Reverse? ', self.isReverse))

class Binary_ILP_case:
    # variables
    # obj_fn [sympy expression]: the function to maximize or minimize
    # b: array of constraints
    def __init__(self, variables, obj_fn, b, maximize=True, expected_obj_val=None):

        # init
        self.variables = variables
        self.obj_fn = obj_fn
        self.b = b # all inEquality functions must be less than for now.
        self.expected_obj_val = expected_obj_val

        self._variables = []
        self._obj_fn = obj_fn
        self._b = b[:]

        self.var_ref = {} # True means _xi = xi, False means _xi = (1-xi)
        self.counter_var_ref = {} # get x1 from _x1

        self.i = 0
        self.algo = self.get_supported_algos()

        self.goal = 'maximize'

        if(maximize == False):
            self.goal = 'minimize'

        self.pre_process()

    def __repr__(self): # for shell
        return self.get_print_string()

    def __str__(self): # for print
        return self.get_print_string()

    def get_print_string(self):

        variables = ''

        for var in self.variables:
            variables += str(var) + ', '

        variables = variables[: -2]

        result = 'Case:'.ljust(10) + variables + '\n'
        result += 'Z:'.ljust(10) + str(self.obj_fn) + '\n\n'

        first_line = True
        for inEq in self.b:
            if first_line:
                result += 'b:'.ljust(10) + str(inEq) + '\n'
                first_line = False
            else:
                result += ''.ljust(10) + str(inEq) + '\n'

        result += '\n'

        if self.expected_obj_val:
            result += 'Exp val:'.ljust(10) + str(self.expected_obj_val)

        return result

    def pre_process(self):

        self.covert_all_constraints_to_less_than()

        # update variable reference and objective fxn reference
        obj_args = self.obj_fn.args

        # when calling args, sympy will change the order of variables appearing in expression with the constant at the first place, and
        # some arbitary order for the rest of the variables
        for item in obj_args:

            if not isinstance(item, numbers.Integer):

                if not isinstance(item, symbol.Symbol):
                    coeff = item.args[0]
                    var = item.args[1]
                else:
                    coeff = 1
                    var = item

                _var = "_" + str(var)
                _var = Symbol(_var)
                self._variables.append(_var)

                if coeff > 0:
                    self.var_ref[var] = VarRef(_var, True) # True for isReverse
                    self._obj_fn = self._obj_fn.subs(var, (1-_var))
                    self._b =  self.get_substitute_b(self._b, var, (1-_var))

                else:
                    self.var_ref[var] = VarRef(_var, False)
                    self._obj_fn = self._obj_fn.subs(var, _var)
                    self._b =  self.get_substitute_b(self._b, var, _var)

                self.counter_var_ref[_var] = var

        # print(self.variables)
        # print(self._variables)
        # print('Result', self.obj_fn)
        # print('Result', self._obj_fn)
        # print('Result', self.b)
        # print('Result', self._b)

    def covert_all_constraints_to_less_than(self):

        # print('start covert_all_constraints_to_less_than', self._b)

        _b = []

        for inEq in self._b:

            # print('inEqu is: ', inEq)
            if isinstance(inEq, (StrictLessThan, LessThan)):
                _b.append(inEq)
            else:
                _b.append(inEq.reversedsign)

        self._b = _b

    def _(self, var):
        return self.var_ref[var].counter_part

    def get_preprocessed_result(self):

        return {
            '_variables' : self._variables,
            '_obj_fn' : self._obj_fn,
            '_b': self._b
        }

    def get_supported_algos(self):

        class Algo:
            def __init__(self):
                self.brutal_divide_and_conquer = 'brutal_divide_and_conquer'
                self.brutal_explicit_enumeration = 'brutal_explicit_enumeration'
                self.implicit_enumeration = 'implicit_enumeration'

        return Algo()

    def reset_counter(self):
        self.i = 0

    def get_run_count(self):
        return self.i

    def get_substitute_b(self, old_b, var, val):

        # to do: add check in this fxn, if result is false, the function that call this function should stop evaluate this possibility
        # print('calc get_substitute_b,', old_b, var, val)
        # val could be value, or the counter part of var
        # example: get_substitute_b(b, x1, (1-_x1))

        result = []

        for inEq in old_b:
            result.append(inEq.subs(var, val))

        # print('sub b result', result)

        return result

    def is_feasible(self, b, var_vals, debug=False):

        for constraint in b:

            c =  constraint

            for var_val in var_vals:
                c = c.subs(var_val.var, var_val.val)

                if c == False:
                    if debug:
                        print('\nConstraint not met: ', constraint, ' with var vals: ', var_vals, '\n')
                    return False

        return True

    def get_obj_fn_val(self, obj_fn, var_vals):

        obj_val = obj_fn
        for item in var_vals:
            obj_val = obj_val.subs(item.var, item.val)

        return obj_val

    def translate_result(self, result):

        if result.obj_val == -oo:
            return result

        var_vals_ref = {}

        for item in result.var_vals:

            _var = item.var
            val = item.val

            var = self.counter_var_ref[_var]

            if self.var_ref[var].isReverse:
                var_vals_ref[var] = 1-val
            else:
                var_vals_ref[var] = val

        sorted_var_vals = [] #based on order of vars

        for var in self.variables:
            sorted_var_vals.append(VarVal(var, var_vals_ref[var]))

        return Result(result.obj_val, sorted_var_vals)

    def solve(self, algo, print_run_count=False):

        variables = self._variables[:]
        obj_fn = self._obj_fn
        b = self._b[:]

        self.reset_counter()

        if algo == self.algo.brutal_divide_and_conquer:
            result = self.solve_by_brutal_divide_and_conquer(variables, obj_fn, b)

        if algo == self.algo.brutal_explicit_enumeration:
            result = self.solve_by_brutal_explicit_enumeration(variables, obj_fn, b)

        if algo == self.algo.implicit_enumeration:
            result = self.solve_by_implicit_enumeration(variables, obj_fn, b)

        if print_run_count:
            print("Run count", self.get_run_count())

        return self.translate_result(result)

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

        all_cases = list(product([0, 1], repeat=len(variables)))

        best_result = Result(obj_val = -oo, var_vals = [])

        for case in all_cases:
            var_vals = []
            for i in range(0, len(variables)):
                var_vals.append(VarVal(variables[i], case[i]))

            obj_val = self.get_obj_fn_val(obj_fn, var_vals)
            self.i += 1
            if obj_val > best_result.obj_val and self.is_feasible(b, var_vals):
                best_result = Result(obj_val, var_vals)

        return best_result

    def sort_vars_by_priority_for_implicit_enumeration(self, variables):

        # to be implemented
        return variables

    def solve_by_implicit_enumeration(self, variables, obj_fn, b):

        # implicit enumeration assume all vars has a negative coefficient in objective function and thus best obj val will be set all vars to 0


        self.i += 1

        # print('running with vars:', variables)
        # print('fn:', obj_fn)
        # print('b:', b)

        best_result = Result(obj_val = -oo, var_vals = [])

        fix_var = variables.pop(0)

        # branch to fix_var = 0

        var_vals = [VarVal(fix_var, 0)]

        for var in variables:
            var_vals.append(VarVal(var, 0))

        if self.is_feasible(b, var_vals): # best case scenario
            obj_val = self.get_obj_fn_val(obj_fn, var_vals)

            # print('all 0 is feasible, returning val:', obj_val)
            return Result(obj_val, var_vals)

        elif len(variables)>0: # can be divided further

            obj_zero = obj_fn.subs(fix_var, 0)
            b_zero = self.get_substitute_b(b, fix_var, 0)
            result_zero = self.solve_by_implicit_enumeration(variables[:], obj_zero, b_zero)

            if result_zero.obj_val > best_result.obj_val:
                # print('best result updated from: ', best_result.obj_val, ' to: ', result_zero.obj_val)
                best_result = Result(result_zero.obj_val, [VarVal(fix_var, 0)] + result_zero.var_vals)

        # branch to fix_var = 1

        var_vals[0].val = 1

        if self.is_feasible(b, var_vals):
            obj_val = self.get_obj_fn_val(obj_fn, var_vals)

            if obj_val > best_result.obj_val:
                # print('best result updated from: ', best_result.obj_val, ' to: ', obj_val)
                best_result = Result(obj_val, var_vals)

        elif len(variables)>0:

            obj_one = obj_fn.subs(fix_var, 1)
            b_one = self.get_substitute_b(b, fix_var, 1)
            result_one = self.solve_by_implicit_enumeration(variables[:], obj_one, b_one)

            if result_one.obj_val > best_result.obj_val:
                # print('best result updated from: ', best_result.obj_val, ' to: ', result_one.obj_val)
                best_result = Result(result_one.obj_val, [VarVal(fix_var, 1)] + result_one.var_vals)


        # print('returning best result', best_result)
        return best_result

if __name__ == '__main__':

    x1, x2, x3, x4, x5 = symbols('x1, x2, x3, x4, x5')
    obj_fn = -8*x1 - x2 - x3 - 5*x4 + 10*x5 + 19
    # b = [
    #     -7*x4 <= 9,
    #     2*x2 - 6*x4 - 3*x1 <= -1,
    #     10*x1 - 3*x2 - 7*x3 <= 15
    # ]

    b = [x5 <=2]

    case = Binary_ILP_case(variables=[x1, x2, x3, x4, x5], b=b, obj_fn=obj_fn,  maximize=True)

    # result = case1.hcase1.algo.brutal_explicit_enumeration, print_run_count=True)
    # print('Result - brutal brutal_explicit_enumeration:', result)
    result = case.solve(case.algo.brutal_divide_and_conquer, print_run_count=True)
    print('Result - brutal divide and conquer:', result)
    result = case.solve(case.algo.implicit_enumeration, print_run_count=True)
    print('Result - implicit_enumeration:', result)

