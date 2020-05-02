from sympy import *


x1, x2, x3, x4, x5 = symbols('x1, x2, x3, x4, x5')

objective_fn = -8*x1 + -2*x2 -4*x3 -7*x4 -5*x5 + 10

# Constraints
b1 = -3*x1 -3*x2 + x3 + 2*x4 + 3*x5 <= -2
b2 = -5*x1 - 3*x2 -2*x3 - x4 + x5 <= -4


class Binary_ILP_case:
    # variables
    # obj_fn: the function to maximize or minimize
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

        print(self.b)

    def solve(self, debug=False):

    	print("Solving ILP: ", self.obj_fn, "\n")

    	for var in self.vars:

    		print(var)
    		a = Poly(self.obj_fn, var)
    		print('Coef:', a.coeffs())
    		print('All coef', a.all_coeffs())


case1 = Binary_ILP_case(variables=[x1, x2, x3], b=[b1, b2], obj_fn=objective_fn,  maximize=True)

case1.solve()