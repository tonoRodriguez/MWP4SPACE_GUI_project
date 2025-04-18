# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 11:50:44 2025

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

width = 0.8e-6
angle = 70
height=0.3e-6
#width=0.7e-6
m=0.55191502449
centered_z=0
radius=60e-6
Lc =0
x_span=140e-6
gap = 0.25e-6
base_width=width
base_hight= 3e-6
LN_hight_sub=height


width_film_x = x_span
width_film_y = radius*2 + gap + base_width +10e-6

centered_x = width_film_x/2
centered_y = 0
centered_z = 0


n_ordinary = 2.2111
n_extraordinary = 2.13755
n_matrix = np.array([n_ordinary,n_extraordinary,n_ordinary])
FDTD = lumapi.FDTD()
mymaterial =FDTD.addmaterial("(n,k) Material")
FDTD.setmaterial(mymaterial,"name","LN_anisotropic")
FDTD.setmaterial("LN_anisotropic", "Anisotropy", 1); # enable diagonal anisotropy
FDTD.setmaterial("LN_anisotropic","Refractive Index",n_matrix)

# Poles for four quarter-circles
px2 = [(x*radius+Lc/2+x_span/2) for x in [0,m,1,1]]
py2 = [x*radius for x in [-1,-1,-m,0]]
p2 = np.array([[xi, yi] for xi, yi in zip(px2, py2)])

materials = open(dir_mat).read()
FDTD.eval(materials)

FDTD.addrect(name="Si_substrate",x = centered_x, x_span=width_film_x,
               y = centered_y, y_span=width_film_y, z_min = centered_z, z_max= base_hight, material = "Si_Salzberg" )

centered_z=base_hight;

FDTD.addrect(name="SiO2_cladding",x = centered_x, x_span=width_film_x,
		 y = centered_y, y_span=width_film_y, z_min = centered_z,
		 z_max= centered_z +base_hight, material = "SiO2_fusedquartz" )
centered_z=centered_z +base_hight

FDTD.addrect(name="LN_core1",x = centered_x, x_span=width_film_x,
		 y = centered_y, y_span=width_film_y, z_min = centered_z,
		 z_max= centered_z+ LN_hight_sub, material = "LN_anisotropic" )
centered_z=centered_z+LN_hight_sub*1.5

FDTD.addwaveguide(name = "arc1", base_angle = angle, base_height= height, base_width=width, material = "LN_anisotropic" )

FDTD.setnamed("arc1","poles",p2)
FDTD.setnamed("arc1","z",centered_z)
FDTD.addfdtd(x_min = p2[0][0]  - 3*width , x_max = p2[3][0] + 3*width , y_min = p2[0][1] - 3*width ,y_max = p2[3][1] +3*width , z =  centered_z , z_span = 4e-6,
             set_simulation_bandwidth = 1 , simulation_wavelength_min = 1.55e-6 , simulation_wavelength_max = 1.56e-6)
FDTD.addport( ) 
FDTD.set("x", p2[0][0] + 0.5e-6)
FDTD.set( "y", p2[0][1])
FDTD.set("y span" , width + 4e-6)
FDTD.set( "z", centered_z - LN_hight_sub/2)
FDTD.set("z span" , 3e-6)
#FDTD.addmodeexpansion(monitor_type= "2D X-normal",x = p2[0][0],y = p2[0][1], y_span  =width + 0.5e-6 , z = centered_z - LN_hight_sub/2 , z_span = 0.65e-6)
#FDTD.addmodeexpansion(monitor_type= "2D Y-normal",x = p2[3][0],y = p2[3][1], x_span  =width + 0.5e-6 , z = centered_z - LN_hight_sub/2 , z_span = 0.65e-6)
FDTD.addport( )
FDTD.set("injection axis" , "y-axis");
FDTD.set("x", p2[3][0])
FDTD.set( "y", p2[3][1] - 0.5e-6)
FDTD.set("x span" , width + 4e-6)
FDTD.set( "z", centered_z - LN_hight_sub/2)
FDTD.set("z span" , 3e-6)
FDTD.set("direction", "backward")

FDTD.addprofile(x_min = p2[0][0] - 3*width  , x_max = p2[3][0] + 3*width , y_min = p2[0][1] - 3*width  ,y_max = p2[3][1] + 3*width , z =  centered_z )
