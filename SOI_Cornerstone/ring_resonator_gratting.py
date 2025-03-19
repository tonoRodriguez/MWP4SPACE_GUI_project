# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 17:28:55 2025

@author: Antonio
"""

import numpy as np
#import matplotlib.pyplot as plt
import os
import sys
#import imp
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from Data_Structure import DataStructure

sys.path.append("C:/Program Files/Lumerical/v241/api/python/")
sys.path.append(os.path.dirname(__file__))
#lumapi = imp.load_source("lumapi","C:/Program Files/Lumerical/v241/api/python/lumapi.py")
#os.add_dll_directory("C:/Program Files/Lumerical/v241/api/python")

dir_mat="Material_script/LNOI_materials.lsf"

import lumapi
#mode starting
mode1=lumapi.MODE()
materials = open(dir_mat).read()
mode1.eval(materials)

centered_x = 0
centered_y = 0
centered_z = 0
width_film_x =10e-6
width_film_y =10e-6
base_hight= 2e-6
height2=0.12e-6
height1=0.1e-6
angle=90
width = 0.5e-6
m=0.55191502449
radius=50e-6
Lc = 0
x_span=0


theta = np.pi / 4  # 30 grados en radianes


def rotar_puntos(p, angulo):
    """Rota una lista de puntos p en sentido antihorario un 'ángulo' dado."""
    cos_t = np.cos(angulo)
    sin_t = np.sin(angulo)
    R = np.array([[cos_t, -sin_t], [sin_t, cos_t]])  # Matriz de rotación
    return np.dot(p, R.T)  # Rotar todos los puntos

# # Poles for four quarter-circles
# px1  = [(x*radius +  +Lc/2+x_span/2) for x in [0,m,1,1]]
# py1 = [radius*x for x in [1,1,m,0]]
# p1 = np.array([[xi, yi] for xi, yi in zip(px1, py1)])
px1 = [(x * radius + Lc / 2 + x_span / 2) for x in [
    0,  # P0: Inicio en (0,1)
    m * np.sin(theta),  # P1: Primer control
    np.sin(theta) + m * np.cos(theta),  # P2: Segundo control
    np.sin(theta)  # P3: Final
]]

py1 = [radius * y for y in [
    1,  # P0: Inicio en (0,1)
    1 - m * np.cos(theta),  # P1: Primer control
    np.cos(theta) + m * np.sin(theta),  # P2: Segundo control
    np.cos(theta)  # P3: Final
]]

# Crear la matriz de puntos
p1 = np.array([[xi, yi] for xi, yi in zip(px1, py1)])


#p2 = rotar_puntos(p1, theta) 
#p3 = rotar_puntos(p2, theta) 
# Configurar los arcos en Lumerical
mode1.addwaveguide(name="arc1", base_angle=theta, base_height=height2, base_width=width, material="Si_Salzberg")
#mode1.addwaveguide(name="arc2", base_angle=theta, base_height=height2, base_width=width, material="Si_Salzberg")
#mode1.addwaveguide(name="arc3", base_angle=theta, base_height=height2, base_width=width, material="Si_Salzberg")

mode1.setnamed("arc1", "poles", p1)
mode1.setnamed("arc1", "z", centered_z + height2 * 0.5)

#mode1.setnamed("arc2", "poles", p2)
#mode1.setnamed("arc2", "z", centered_z + height2 * 0.5)

#mode1.setnamed("arc3", "poles", p3)
#mode1.setnamed("arc3", "z", centered_z + height2 * 0.5)



# mode1.setnamed("arc4","poles",p4)
# mode1.setnamed("arc4","z",centered_z + height2*0.5)