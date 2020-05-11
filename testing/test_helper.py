from sympy import *
from ..solver import *

def run_all_algos(case, debug=False):

    if debug:
        print(case)

    a = case.solve(case.algo.brutal_explicit_enumeration)
    b = case.solve(case.algo.brutal_divide_and_conquer)
    c = case.solve(case.algo.implicit_enumeration)

    if debug:
        print('Result a - brutal explicit enumeration:', a)
        print('Result b - brutal divide and conquer:', b)
        print('Result c - implicit enumeration', c)

    return {
        'a': a,
        'b': b,
        'c': c
    }