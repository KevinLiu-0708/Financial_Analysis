# -*- coding: utf-8 -*-
"""
Created on Thu May 12 13:21:44 2022

@author: 111036
"""

from sympy import *
from sympy.plotting import plot
import random
import numpy as np
from numpy.linalg import inv

x = symbols('x')

#expr = x ** 2 - x + 3
#expr = sin(x)



x_arr = [0.02, 0.08, 0.34, 0.45, 0.58, 0.70, 0.82, 1.07, 1.38, 1.68, 1.80, \
         1.93, 2.23, 2.50, 2.71, 2.86, 3.14, 3.40, 3.62, 3.88, 4.21, 4.45, \
             4.53, 4.71, 5.03, 5.18, 5.31, 5.43, 5.54, 5.80, 6.03, 6.16, 6.32, \
                 6.45, 6.75, 6.95, 7.11, 7.25, 7.51, 7.73, 8.02, 8.16, 8.38, \
                     8.61, 8.75]
y_arr = [1, 1.0953, 1.4789, 1.6515, 1.8474, 1.9642, 2.0925, 2.0864, 1.6978, \
         1.1256, 0.8946, 0.7072, 0.5426, 0.7396, 1.0428, 1.2799, 1.6624, 1.8177, \
             1.7875, 1.6336, 1.4453, 1.3483, 1.3380, 1.3333, 1.3089, 1.2579, \
                 1.1916, 1.1165, 1.0414, 0.8835, 0.8490, 0.8983, 1.0416, 1.2037, \
                     1.6859, 1.9622, 2.0929, 2.1259, 1.9403, 1.5788, 1.0083, 0.7795, \
                         0.5662, 0.5793, 0.6747]
'''
#x_arr = [-3,-1,0,2,3]
#y_arr = [15,5,3,5,9]

x_arr = [0,0.5,1,1.5,2,2.5]
y_arr = [0,0.2,0.27,0.3,0.32,0.33]

x_arr = []
y_arr = []

random_numbers = int(input('random_numbers: '))
for i in range(random_numbers):
    num = round(random.uniform(0,10),2)
    x_arr.append(num)
    y_arr.append(float(expr.subs(x,num)))
'''
#n = int(input('n: '))
least_error = 0
least_error_equ = 0
least_error_degree = 0

for n in range(1, len(x_arr)):
    Coef_arr = np.zeros((n+1,n+1))
    ans_arr = np.zeros((n+1,1))
    
    # 係數矩陣
    for j in range (0,n+1):
        for k in range(0,n+1):
            if j == 0 and k == 0:
                Coef_arr[j][k] = len(x_arr)
            else:
                #print(j,k)
                tmp = [number ** (j+k) for number in x_arr]
                Coef_arr[j][k] = sum(tmp)
        
    # 右矩陣
    for j in range(n+1):
        if j == 0:
            ans_arr[j][0] = sum(y_arr)
        else:
            tmp = [number ** j for number in x_arr]
            ans_arr[j][0] = sum(np.array(tmp) * np.array(y_arr))
    
    # 反矩陣
    inverse = inv(Coef_arr)
    result = np.dot(inverse, ans_arr)
    
    # 近似equation
    final_eq = 0
    for i in range(n+1):
        tmp2 = result[i][0] * (x ** i)
        final_eq = final_eq + tmp2
    
    #print('Final Equation: ', final_eq)
    
    # error
    #error_arr = np.zeros((random_numbers,1))
    error_arr = np.zeros((len(x_arr),1))
    approx_arr = np.zeros((len(x_arr),1))
    for h in range(len(x_arr)):
        approx_arr[h][0] = round(float(final_eq.subs(x,x_arr[h])),4)
        error_arr[h][0] = abs(approx_arr[h][0] - y_arr[h])
        
    error = [number ** 2 for number in error_arr]
    
    # 課本least square
    #error = sum(error)
    
    # 老師的方法
    error = sum(error) / (len(x_arr) - n)
    root_error = error ** (1/2)
    
    if n == 1:
        least_error = root_error
        least_error_coef = Coef_arr
        least_error_equ = final_eq
        least_error_degree = n
    
    if n != 1 and least_error > root_error:
        least_error = root_error
        least_error_coef = Coef_arr
        least_error_equ = final_eq
        least_error_degree = n
    
    '''
    print('degree: ',n)
    print('error: ', error)
    print('root error: ', root_error)
    #print('Coef: ', Coef_arr)
    print('Equation: ',final_eq)
    print('approximation: ',approx_arr)
    print()
    '''
print('least_root_error: ', least_error)
#print('Coef: ', least_error_coef)
print('degree: ', least_error_degree)
print('Equation: ', least_error_equ)

# plot
p1 = plot(least_error_equ)
'''
p2 = plot(expr)
p1.append(p2[0])
'''
p1.show()
