# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 08:54:54 2024

@author: Abdelrahman Ellithy
"""
import sympy as sp
import time

def HbisectionFalseMS(f, a, b, tol, max_iter=100, delta=1e-4):
    fa, fb = f(a), f(b)
    n = 0
    while n < max_iter:
        n += 1
        mid = (a + b) * 0.5
        fmid = f(mid)
        
        if fa * fmid < 0:
            b, fb = mid, fmid
        else:
            a, fa = mid, fmid
        try:
            dx = (a * fb) - (b * fa)
            fp = dx / (fb - fa )
            ffp = f(fp)
        except ZeroDivisionError:
            ffp = fmid
            fp = mid

        if fa * ffp < 0:
            b, fb = fp, ffp
        else:
            a, fa = fp, ffp

        if abs(ffp) <= tol:
            return n, fp, ffp, a, b

        xS = fp - delta * ffp / (f(fp + delta) - ffp)
        if (a < xS< b):
            fxS = f(xS)
            if abs(fxS) < abs(ffp):
                if fa * fxS < 0:
                    b, fb = xS, fxS
                else:
                    a, fa = xS, fxS
                if abs(fxS) <= tol:
                    return n, xS, fxS, a, b

    final_x = (a + b) * 0.5
    return n, final_x, f(final_x), a, b

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