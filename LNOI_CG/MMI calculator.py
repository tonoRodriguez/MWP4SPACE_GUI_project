# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 16:46:16 2025

@author: Antonio
"""
import numpy as np

neff = 1.870493786 # effective index
w = 6
We = w
lambda0 = 1.55
N = 2
p = np.linspace(1,10 , 10)


Lpi=(4/3)*neff*(We**2)/lambda0

Lsi=p*3*Lpi/N;
L=p*(3*Lpi)/(N*4);
M = (2 * We / lambda0) * np.sqrt(neff**2 - 1.5**2)
xm = N*We/M
