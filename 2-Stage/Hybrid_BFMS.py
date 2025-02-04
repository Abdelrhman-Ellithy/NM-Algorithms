# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 08:54:54 2024

@author: Abdelrahman Ellithy
"""

# Import modules
import sympy as sp
import time

def HbisectionFalseMS(f, a, b, tol, max_iter=100,delta=1e-4):
    """
    This function implements the Bisection method to find a root of the
    function (f) within the interval [a, b] with a given tolerance (tol).
    
    Parameters:
        f   (function): The function for which we want to find a root.\n
        a      (float): The lower bound of the initial interval.\n
        b      (float): The upper bound of the initial interval.\n
        tol    (float): The desired tolerance.\n
        max_iter (int): The maximum number of iterations.
                     
    Returns:
        n    (int): The number of iterations.\n
        x  (float): The estimated root of the function f within the interval [a, b].\n
        fx (float): The function value at the estimated root.\n
        a  (float): The lower bound of the final interval.\n
        b  (float): The upper bound of the final interval.
    """
    
    fa, fb = f(a), f(b)
    for n in range(1, max_iter + 1):
        x = 0.5 * (a + b)
        fx = f(x)
        if fa * fx < 0:
            b, fb = x, fx
        else:
            a, fa = x, fx
        try:
            dx = ((a * fb) -( b * fa))
            x = dx / (fb - fa)
            fx = f(x)
        except ZeroDivisionError:
            continue
        if fa * fx < 0:
            b, fb = x, fx
        else:
            a, fa = x, fx

        if abs(fx) <= tol:
            return n, x, fx, a, b
        else:
            #Calculate xS using the modified secant method
            f_delta = f(delta + x)
            xS = x - (delta * fx) / (f_delta - fx)
            fxS = f(xS)
            if (abs(fxS) < abs(fx)) and (xS > a and xS < b):
                if fa * fxS < 0:
                    b = xS
                else:
                    a = xS
                x=xS
                fx=fxS
                if abs(fx) <= tol:
                    return n, x, fx, a, b
    # Return the number of iterations, estimated root, function value, lower bound, and upper bound
    return n, x, fx, a, b

# Define the symbolic variable x
x = sp.Symbol('x')
dataset=[
         (x * sp.exp(x) - 7,1,2)
         ,(x**3-x-1,1,2)
         ,(x**2-x-2,1,4)
         ,(x-sp.cos(x),0,1)
         ,(x**2-10,3,4)
         ,(sp.sin(x)-x**2,0.5,1)
         ,(x+sp.ln(x),0.1,1)
         ,(sp.exp(x)-3*x-2,2,3)
         ,(x**2+sp.exp(x/2)-5,1,2)
         ,(x*sp.sin(x)-1,0,2)
         ,(x*sp.cos(x)+1,-2,4)
         ,(x**10-1,0,1.3)
         ,(x**2-x-2,1,4)
         ,(x**2+2*x-7,1,3)
         ]
tol = 1e-14

print()
print("Abdelrahman Hybrid HbisectionFalseMS")
print("\t\tIter\t\t Root\t\tFunction Value\t\t Lower Bound\t\t Upper Bound")
for i in range(0,len(dataset)) :    
    f=dataset[i][0]
    f = sp.lambdify('x', f)
    a=dataset[i][1]
    b=dataset[i][2]
    t1=time.time()
    n, x, fx, a, b = HbisectionFalseMS(f, a, b, tol)
    t=time.time()-(t1)
    print(f"problem{i+1}| \t{n} \t {x:.16f} \t {fx:.16f} \t {a:.16f} \t {b:.16f} \t {t:.16f}")