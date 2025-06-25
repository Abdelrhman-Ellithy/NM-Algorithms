# -*- coding: utf-8 -*-
"""
scipy Brent's Method 
@author: Abdelrahman Ellithy (adapted for comparison)
"""
import sympy as sp
import time
import sqlite3
from scipy import optimize

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
method = '11-Scipy-Brent,R.P-1973'
print(method)
rest_data()
print("Time")
records = []
for c in range(1000):
    for i, (func, a, b) in enumerate(dataset):
        f = sp.lambdify('x', func)
        t1 = time.perf_counter()
        for j in range(100):
            z = optimize.brentq(f=f, a=a, b=b,xtol= tol)
        t2 = time.perf_counter()
        t = t2 - t1
        records.append((i+1, method, t))
        print(f"{t}")
if records:
    record_speeds(records)