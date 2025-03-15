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
x_span=120e-6


theta = np.pi / 6  # 30 grados en radianes


def generar_arco(theta, prev_p3=None, prev_angle=0):
    """Genera los puntos de un arco Bézier con continuidad tangencial."""
    
    if prev_p3 is None:
        # Primer arco comienza en (radius, 0)
        P0 = np.array([radius, 0])
        angle = 0  # Primer arco no tiene rotación inicial
    else:
        # Los siguientes arcos comienzan en el punto final del anterior
        P0 = prev_p3
        angle = prev_angle  # Ángulo acumulado del arco anterior

    # Puntos de control alineados con la tangente
    P1 = P0 + radius * m * np.array([-np.sin(angle), np.cos(angle)])  # Control 1
    P2 = P0 + radius * np.array([
        np.cos(angle + theta) + m * np.sin(angle + theta),
        np.sin(angle + theta) - m * np.cos(angle + theta)
    ])  # Control 2
    P3 = P0 + radius * np.array([np.cos(angle + theta), np.sin(angle + theta)])  # Punto final
    
    return np.array([P0, P1, P2, P3]), P3, angle + theta  # Devuelve los nuevos puntos y el nuevo ángulo

# Generamos los arcos sin deformación
p1, last_p3, last_angle = generar_arco(theta)  # 0° a 30°
p2, last_p3, last_angle = generar_arco(theta, last_p3, last_angle)  # 30° a 60°
#p3, last_p3, last_angle = generar_arco(theta, last_p3, last_angle)  # 60° a 90°

# Configurar los arcos en Lumerical
mode1.addwaveguide(name="arc1", base_angle=theta, base_height=height2, base_width=width, material="Si_Salzberg")
mode1.addwaveguide(name="arc2", base_angle=theta, base_height=height2, base_width=width, material="Si_Salzberg")
#mode1.addwaveguide(name="arc3", base_angle=theta, base_height=height2, base_width=width, material="Si_Salzberg")

mode1.setnamed("arc1", "poles", p1)
mode1.setnamed("arc1", "z", centered_z + height2 * 0.5)

mode1.setnamed("arc2", "poles", p2)
mode1.setnamed("arc2", "z", centered_z + height2 * 0.5)

#mode1.setnamed("arc3", "poles", p3)
#mode1.setnamed("arc3", "z", centered_z + height2 * 0.5)
# mode1.setnamed("arc3","poles",p3)
# mode1.setnamed("arc3","z",centered_z + height2*0.5)


# mode1.setnamed("arc4","poles",p4)
# mode1.setnamed("arc4","z",centered_z + height2*0.5)