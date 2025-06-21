# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 08:54:54 2024

@author: Abdelrahman Ellithy
"""
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
def record_speeds(records):
    try:
        with sqlite3.connect('Results.db') as con:
            cursor = con.cursor()
            cursor.executemany("INSERT INTO results (problemId, method_name, CPU_Time) VALUES (?, ?, ?)", records)
            con.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
# Define the bisection function
def HbisectionFalse(f, a, b, tol, max_iter=100):
    fa, fb = f(a), f(b)
    for n in range(1, max_iter + 1):
        mid = 0.5 * (a + b)
        fmid = f(mid)
        if abs(fmid) <= tol:
            return n, mid, fmid, a, b
        
        if fa * fmid < 0:
            b, fb = mid, fmid
        else:
            a, fa = mid, fmid
        try:
            dx = (a * fb - b * fa)
            fp = dx / (fb - fa)
        except ZeroDivisionError:
            continue
        
        ffp = f(fp)
        if abs(ffp) <= tol:
            return n, fp, ffp, a, b
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
method='06-Optimized-Bisection-FalsePosition'
print(method)
rest_data()
print("\t\tIter\t\t Root\t\tFunction Value\t\t Lower Bound\t\t Upper Bound\t\t Time")
records = []
for c in range(1000):
    for i, (func, a, b) in enumerate(dataset):
        f = sp.lambdify('x', func)
        t1 = time.perf_counter()
        for j in range(100):
            n, x_val, fx, a_val, b_val = HbisectionFalse(f, a, b, tol)
        t2 = time.perf_counter()
        t = t2 - t1
        records.append((i+1, method, t))
        print(f"problem{i+1}| \t{n} \t {x_val:.16f} \t {fx:.16f} \t {a_val:.16f} \t {b_val:.16f} \t {t:.20f}")

# Batch insert all records at once
if records:
    record_speeds(records)