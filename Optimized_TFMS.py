# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 08:54:54 2024

@author: Abdelrahman Ellithy
"""

# Import modules
import sympy as sp
import time
import sqlite3
def rest_data():
    con = sqlite3.connect('Results.db')
    cursor = con.cursor()
    cursor.execute(""" 
            create table IF NOT EXISTS results(
            id Integer PRIMARY KEY not null,
            problemId Integer problemId not null,
            method_name text,
            CPU_Time REAL
            )""")
    con.commit()
    con.close()
def record_speed(ID, methood,time ) :
    con=sqlite3.connect('Results.db')
    cursor=con.cursor()
    cursor.execute('insert into results(problemId, method_name , CPU_Time) values (?,?,?)',( ID,methood,time ))
    con.commit()
    con.close()
    
def HtrisectionFalseMS(f, a, b, tol, max_iter=100, delta=1e-4):

    fa, fb = f(a), f(b)
    for n in range(1, max_iter + 1):
        diff = b - a
        x1 = a + diff/3
        x2 = b - diff/3
        fx1, fx2 = f(x1), f(x2)
        if abs(fx1) <= tol: return n, x1, fx1, a, b
        if abs(fx2) <= tol: return n, x2, fx2, a, b

        if fa * fx1 < 0:
            b, fb = x1, fx1
        elif fx1 * fx2 < 0:
            a, b, fa, fb = x1, x2, fx1, fx2
        else:
            a, fa = x2, fx2
        try:
            dx = (a * fb) - (b * fa)
            fp = dx / (fb - fa )
            ffp = f(fp)
        except ZeroDivisionError:
            continue
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

    # Fallback to best estimate
    final_x = (a + b) * 0.5
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
method='Optimized_TFMS'
print(method)
rest_data()
print("\t\tIter\t\t Root\t\tFunction Value\t\t Lower Bound\t\t Upper Bound\t\t Time")
for i in range(0,len(dataset)) :
    for c in range(0,100): 
        t1=time.time() 
        for j in range (0,100):    
                f=dataset[i][0]
                f = sp.lambdify('x', f)
                a=dataset[i][1]
                b=dataset[i][2]
                n, x, fx, a, b = HtrisectionFalseMS(f, a, b, tol)
        t2=time.time()
        t=(t2-t1)
        record_speed(i,method,t)
        print(f'problem: {i}, method: {method}, time: {t}')
        print(f"problem{i+1}| \t{n} \t {x:.16f} \t {fx:.16f} \t {a:.16f} \t {b:.16f} \t {t:.20f}")