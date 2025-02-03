# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 08:54:54 2024

@author: Abdelrahman Ellithy
"""

# Import modules
import sympy as sp
def HtrisectionFalse(f, a, b, tol, max_iter=100):
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
    
    # Initialize the iteration counter
    n = 0
    # Iterate until maximum iterations reached, or |f(x)| <= tol
    while n < max_iter:
        # Increment the iteration counter by 1
        n += 1
        
        # Calculate the midpoint of the interval
        # Calculate x1 and x2
        x1 = (b + 2*a) / 3
        x2 = (2*b + a) / 3
        
        # Calculate f(x1), f(x2) and f(a)
        fx1 = f(x1)
        fx2 = f(x2)
        fa = f(a)
        
        # Choose the root with the smaller error
        if abs(fx1) < abs(fx2):
            x = x1
            fx = fx1
        else:
            x = x2
            fx = fx2
        
        # Check if the absolute value of f(x) is smaller than the tolerance
        if abs(fx) <= tol:
            break
        # Determine the new interval [a, b]
        elif fa * fx1 < 0:
            b = x1
        elif fx1 * fx2 < 0:
            a = x1
            b = x2
        else:
            a = x2
        fa=f(a)
        fb=f(b)
        x = (a*fb - b*fa) / (fb - fa)
        fx = f(x)
        if fa * fx < 0:
            b = x
        else:
            a = x
        if abs(fx) <= tol:
            break
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
print("Abdelrahman Hybrid HtrisectionFalse")
print("\t\t\tIter\t\t Root\t\t\t\tFunction Value\t\t\t Lower Bound\t\t\t Upper Bound")
for i in range(0,len(dataset)) :    
    f=dataset[i][0]
    f = sp.lambdify('x', f)
    a=dataset[i][1]
    b=dataset[i][2]
    n, x, fx, a, b = HtrisectionFalse(f, a, b, tol)
    #print(f"problem{i+1}| \t{n} \t {x:.16f} \t {fx:.16f} \t {a:.16f} \t {b:.16f}")
    print(f"{n}")