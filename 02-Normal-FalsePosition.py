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
    
def false_position(f, a, b, tol):
    """
    This function implements the False Position method to find a root of the function (f)
    within the interval [a, b] with a given tolerance (tol).
    
    Parameters:
        f (function): The function for which we want to find a root.\n
        a    (float): The left endpoint of the initial interval.\n
        b    (float): The right endpoint of the initial interval.\n
        tol  (float): The desired tolerance.
                     
    Returns:
        x (float): The estimated root of the function f within the interval [a, b].
    """
    i = 0
    fx=0
    while True:
        i += 1
        fa= f(a)
        fb= f(b)
        x = (a*fb - b*fa) / (fb - fa)
        fx = f(x)
        if abs(fx) <= tol:
            break
        elif fa * fx < 0:
            b = x
        else:
            a = x
    
    # Return the estimated root
    return i, x, fx, a, b



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
method='02-Normal-FalsePosition'
print(method)
rest_data()
print("\t\tIter\t\t Root\t\tFunction Value\t\t Lower Bound\t\t Upper Bound\t\t Time")
records = []
for i, (func, a, b) in enumerate(dataset):
    f = sp.lambdify('x', func)
    for c in range(100):
        t1 = time.perf_counter()
        for j in range(100):
            n, x_val, fx, a_val, b_val = false_position(f, a, b, tol)
        t2 = time.perf_counter()
        t = t2 - t1
        records.append((i+1, method, t))
        print(f"problem{i+1}| \t{n} \t {x_val:.16f} \t {fx:.16f} \t {a_val:.16f} \t {b_val:.16f} \t {t:.20f}")

# Batch insert all records at once
if records:
    record_speeds(records)