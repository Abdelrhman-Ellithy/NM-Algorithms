# -*- coding: utf-8 -*-
"""
Brent's Method (Corrected)
@author: Abdelrahman Ellithy (adapted for comparison)
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
        problemId Integer not null,
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

def BrentsMethod(f, a, b, tol, max_iter=100):
    fa, fb = f(a), f(b)
    if fa * fb >= 0:
        return max_iter, (a + b) * 0.5, f((a + b) * 0.5), a, b
    if abs(fa) < abs(fb):
        a, b, fa, fb = b, a, fb, fa
    c, fc = a, fa
    mflag = True
    n = 0
    delta = 1e-4  # Small step to avoid division by zero
    while n < max_iter:
        n += 1
        prev_b = b
        # Inverse Quadratic Interpolation
        if fa != fc and fb != fc:
            try:
                s = a * fb * fc / ((fa - fb) * (fa - fc)) + b * fa * fc / ((fb - fa) * (fb - fc)) + c * fa * fb / ((fc - fa) * (fc - fb))
                # Ensure s is within acceptable bounds
                if not ((3*a + b)/4 < s < b or b < s < (3*a + b)/4) or \
                   (mflag and abs(s - b) >= abs(b - c) / 2) or \
                   (not mflag and abs(s - b) >= abs(c - prev_c) / 2):
                    s = (a + b) * 0.5
                    mflag = True
                else:
                    mflag = False
            except ZeroDivisionError:
                s = (a + b) * 0.5
                mflag = True
        else:
            # Secant
            try:
                s = b - fb * (b - a) / (fb - fa)
                if not ((3*a + b)/4 < s < b or b < s < (3*a + b)/4) or \
                   (mflag and abs(s - b) >= abs(b - c) / 2) or \
                   (not mflag and abs(s - b) >= abs(c - prev_c) / 2):
                    s = (a + b) * 0.5
                    mflag = True
                else:
                    mflag = False
            except ZeroDivisionError:
                s = (a + b) * 0.5
                mflag = True
        fs = f(s)
        if abs(fs) <= tol or abs(b - a) <= tol:
            return n, s, fs, a, b
        prev_c = c
        c, fc = a, fa
        a, fa = b, fb
        b, fb = s, fs
        if fa * fb >= 0:
            a, fa = c, fc
        if abs(fa) < abs(fb):
            a, b, fa, fb = b, a, fb, fa
        # Ensure minimum step size
        if abs(b - a) < delta:
            return n, b, fb, a, b
    final_x = (a + b) * 0.5
    return n, final_x, f(final_x), a, b

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
method = '10-Brent,R.P-1973'
print(method)
rest_data()
print("\t\tIter\t\t Root\t\tFunction Value\t\t Lower Bound\t\t Upper Bound\t\t Time")
records = []
for c in range(1000):
    for i, (func, a, b) in enumerate(dataset):
        f = sp.lambdify('x', func)
        t1 = time.perf_counter()
        for j in range(100):
            n, x_val, fx, a_val, b_val = BrentsMethod(f, a, b, tol)
        t2 = time.perf_counter()
        t = t2 - t1
        records.append((i+1, method, t))
        print(f"problem{i+1}| \t{n} \t {x_val:.16f} \t {fx:.16f} \t {a_val:.16f} \t {b_val:.16f} \t {t:.20f}")
if records:
    record_speeds(records)