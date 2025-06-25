# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 08:54:54 2024
Implements Sabharwal's Blended Algorithm (Bisection + False Position), Algorithm 3, page 11.
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
    
def blendBF(f, a, b, tol, max_iter=1000):
    """
    Implements Sabharwal's Blended Algorithm (Bisection + False Position), Algorithm 3, page 11.
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
    
    # Define the bisection interval [a1, b1]
    a1 = a
    b1 = b
    
    # Define the false-position interval [a2, b2]
    a2 = a
    b2 = b
    
    # Iterate until maximum iterations reached, or |f(x)| <= tol
    while n < max_iter:
        # Increment the iteration counter by 1
        n += 1
        
        # Calculate f(a) and f(b)
        fa = f(a)
        fb = f(b)
        
        # Calculate xB using the bisection method
        xB = (a + b) / 2
        fxB = f(xB)
        
        # Calculate xF using the false-position method
        xF = (a*fb - b*fa) / (fb - fa)
        fxF = f(xF)
        
        # Choose the root with the smaller error
        if abs(fxB) < abs(fxF):
            x = xB
            fx = fxB
        else:
            x = xF
            fx = fxF
        
        # Check if the absolute value of f(x) is smaller than the tolerance
        if abs(fx) <= tol:
            break
        
        # Determine the new bisection interval [a1, b1]
        if fa*fxB < 0:
            b1 = xB
        else:
            a1 = xB
        
        # Determine the new false-position interval [a2, b2]
        if fa*fxF < 0:
            b2 = xF
        else:
            a2 = xF
        
        # Take the intersection between [a1, b1] and [a2, b2]
        a = max(a1, a2)
        b = min(b1, b2)
        
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
method='05-Sabharwal-2019-Hybrid-Blend-Bisection-Falseposition'
print(method)
rest_data()
print("\t\tIter\t\t Root\t\tFunction Value\t\t Lower Bound\t\t Upper Bound\t\t Time")
records = []
for c in range(1000):
    for i, (func, a, b) in enumerate(dataset):
        f = sp.lambdify('x', func)
        t1 = time.perf_counter()
        for j in range(100):
            n, x_val, fx, a_val, b_val = blendBF(f, a, b, tol)
        t2 = time.perf_counter()
        t = t2 - t1
        records.append((i+1, method, t))
        print(f"problem{i+1}| \t{n} \t {x_val:.16f} \t {fx:.16f} \t {a_val:.16f} \t {b_val:.16f} \t {t:.20f}")

if records:
    record_speeds(records)