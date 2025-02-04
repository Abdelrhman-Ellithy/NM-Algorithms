# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 08:54:54 2024

@author: Abdelrahman Ellithy
"""

# Import modules
import sympy as sp
import time
def HbisectionFalse(f, a, b, tol, max_iter=100):
    """
    Optimized hybrid bisection-false position method with:
    - 2 function evaluations per iteration (down from 5)
    - O(1) memory complexity
    - Early termination checks
    - Numerical stability safeguards
    """
    fa, fb = f(a), f(b)
    
    # Immediate checks for root at boundaries
    if abs(fa) <= tol: return 0, a, fa, a, b
    if abs(fb) <= tol: return 0, b, fb, a, b

    for n in range(1, max_iter + 1):
        # Bisection phase (1 evaluation)
        mid = 0.5 * (a + b)
        fmid = f(mid)
        
        if abs(fmid) <= tol:
            return n, mid, fmid, a, b
        
        # Update interval using bisection
        if fa * fmid < 0:
            b, fb = mid, fmid
        else:
            a, fa = mid, fmid

        # False position phase (1 evaluation)
        try:
            dx = (a * fb - b * fa)
            fp = dx / (fb - fa)
        except ZeroDivisionError:
            continue

        ffp = f(fp)
        if abs(ffp) <= tol:
            return n, fp, ffp, a, b
        # Update interval using false position
        if fa * ffp < 0:
            b, fb = fp, ffp
        else:
            a, fa = fp, ffp

    # Max iterations reached
    final_x = 0.5 * (a + b)
    return max_iter, final_x, f(final_x), a, b

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
print("\nAbdelrahman Hybrid HbisectionFalse")
print("\t\tIter\t\t Root\t\tFunction Value\t\t Lower Bound\t\t Upper Bound\t\t Time")
for i in range(0,len(dataset)) :    
    f=dataset[i][0]
    f = sp.lambdify('x', f)
    a=dataset[i][1]
    b=dataset[i][2]
    t1=time.time()
    n, x, fx, a, b = HbisectionFalse(f, a, b, tol)
    t=time.time()-(t1)
    print(f"problem{i+1}| \t{n} \t {x:.16f} \t {fx:.16f} \t {a:.16f} \t {b:.16f} \t {t:.16f}")