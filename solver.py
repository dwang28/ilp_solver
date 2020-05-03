from sympy import *





class Binary_ILP_case:
    # variables
    # obj_fn [sympy expression]: the function to maximize or minimize
    # b: array of constraints
    def __init__(self, variables, obj_fn, b, maximize=True):

        # init
        self.vars = variables
        self.obj_fn = obj_fn
        self.b = b

        self.z = symbols('z')
        self.obj_fn = Eq(self.z, self.obj_fn)

        self.goal = 'maximize'
        if(maximize == False):
            self.goal = 'minimize'

        # print(self.b)

    def solve(self, debug=False):

    	print("Solving ILP: ", self.obj_fn, "\n")

    	for var in self.vars:

    		print(var)
    		a = Poly(self.obj_fn, var)
    		print('Coef:', a.coeffs())
    		print('All coef', a.all_coeffs())

    def solve_by_brutal_divide_and_conquer(self, vars=None, obj_fn=None, b=None):

        if vars == None:
            vars = self.vars

        if obj_fn == None:
            obj_fn = self.obj_fn

        if b ==None:
            b = self.b



        print('vars', vars)
        print('len vars', len(vars))

        # if number of free vars is greater than 1, pick one var, update objective function and inequality constraints
        if(len(vars) > 1):
            




x1, x2, x3, x4, x5 = symbols('x1, x2, x3, x4, x5')
vars = [x1, x2, x3, x4, x5]

objective_fn = -8*x1 + -2*x2 - 4*x3 - 7*x4 - 5*x5 + 10  # expression

# Constraints
# b1, b2 are sympy expressions here
b1 = -3*x1 - 3*x2 + x3 + 2*x4 + 3*x5 <= -2
b2 = -5*x1 - 3*x2 - 2*x3 - x4 + x5 <= -4

case1 = Binary_ILP_case(variables=vars, b=[b1, b2], obj_fn=objective_fn,  maximize=True)
case1.solve_by_brutal_divide_and_conquer()
