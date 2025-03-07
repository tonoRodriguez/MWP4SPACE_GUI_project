# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 11:23:19 2025

@author: Antonio
"""
import numpy as np


m=[655,657,659]

R=[]
FSR=[]
# m*1.3e-6 /*2.71* 2 *pi=r
wl=1.3e-6
neff=2.71
c=3e8
ng= 4.5  # 4 or 5
for cons in m:
    Rad = cons*wl/(neff*2*np.pi)
    R.append(Rad)
    L= 2 * np.pi * Rad
    FSR.append(c/(ng*L))
    
print(R)
print(FSR)



# m=[505,510,511]

# R=[]
# FSR=[]

# # m*1.3e-6 /*2.71* 2 *pi=r

# wl=1.5e-6
# neff=2.65
# c=3e8
# ng= 4.2  # 4 or 5
# for cons in m:
#     Rad = cons*wl/(neff*2*np.pi)
#     R.append(Rad)
#     L= 2 * np.pi * Rad
#     FSR.append(c/(ng*L))
# print(R)
# print(FSR)
