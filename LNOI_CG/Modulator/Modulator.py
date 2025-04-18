# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 15:13:18 2025

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


sys.path.append("C:/Program Files/Lumerical/v241/api/python/")
sys.path.append(os.path.dirname(__file__))
#lumapi = imp.load_source("lumapi","C:/Program Files/Lumerical/v241/api/python/lumapi.py")
#os.add_dll_directory("C:/Program Files/Lumerical/v241/api/python")

import lumapi
#mode starting
device=lumapi.DEVICE()

device.addmodelmaterial(name = "SiO2 (Glass) - Sze")
color = np.array([1.0, 0.6, 0.2, 1.0])  # RGBA values for yellow
device.set("color", color)
device.addmaterialproperties("CT","SiO2 (Glass) - Sze")
device.select("SiO2 (Glass) - Sze")
device.addmaterialproperties("HT","SiO2 (Glass) - Sze")
device.select("SiO2 (Glass) - Sze")
device.addmaterialproperties("EM","SiO2 (Glass) - Palik")

device.addmodelmaterial(name = "Au (Gold) - CRC")
color = np.array([1.0, 1.0, 0.0, 1.0])  # RGBA values for yellow
device.set("color", color)
device.addmaterialproperties("CT","Au (Gold) - CRC")
device.select("Au (Gold) - CRC")
device.addmaterialproperties("HT","Au (Gold) - CRC")
device.select("Au (Gold) - CRC")
device.addmaterialproperties("EM","Au (Gold) - CRC")

device.addmodelmaterial(name = "LiNbO3 semiconductor - X/Y cut (Lithium Niobate)")
color = np.array([0, 1.0, 0.0, 1.0])  # RGBA values for yellow
device.set("color", color)
device.addmaterialproperties("CT","LiNbO3 semiconductor - X/Y cut (Lithium Niobate)")
device.select("LiNbO3 semiconductor - X/Y cut (Lithium Niobate)")
device.addmaterialproperties("HT","LiNbO3 semiconductor - X/Y cut (Lithium Niobate)")
device.select("LiNbO3 semiconductor - X/Y cut (Lithium Niobate)")
device.addemmaterialproperty("Dielectric")
device.set("name","LiNbO3 Opt X cut (Lithium Niobate)")
device.set("refractive index",2.21)

device.addmodelmaterial(name = "UV15")
color = np.array([0.5, 0.0, 0.5, 1.0])  # RGBA values for yellow
device.set("color", color)
device.addctmaterialproperty("Insulator");
device.set("relative dielectric permittivity",3)
device.set("name","UV15")
device.select("UV15")
device.addemmaterialproperty("Dielectric")
device.set("refractive index",1.504)
device.set("name","UV15")
device.select("UV15")
device.addhtmaterialproperty("Solid");
device.set("name","UV15")


x_span = 50e-6
y_span = 20e-6

angle = 70
height2=0.3e-6
waveguide_w=0.8e-6
Gap= 6.5e-6

h1 = 0.3e-6
h2=0.3e-6
Si_Base= 12e-6
SiO2_base = 3e-6
angle_in_rad = angle/180 *np.pi
electrode_hight = 2e-6
electrode_width = 6.5e-6
#angle width is the middle
lx_up = waveguide_w - h2 / np.tan(angle_in_rad)
lx_down =waveguide_w + h2 / np.tan(angle_in_rad)
c_x= - electrode_width/2 - Gap/2
c_y= 3e-6


V = np.zeros((8, 2))

# Asignar valores a la matriz V
# Va desde el -25 hasta el 25
# el numero 2 representa las diferentes alturas 2 -> 2.7 -> 2.86
# Deberia ser 2 -> 2.3 y 2.6
# ancho de la parte de abajo vendria siendo -8.15 - -6.35 = 1.8
# ancho de la parte de arriba vendria siendo -7.8 - - 6.7 = 1.width




V[0, 0:2] = [c_x + lx_down /2, c_y +h1]
V[1, 0:2] = [c_x + lx_up /2, c_y + h1 +h2]
V[2, 0:2] = [c_x - lx_up /2, c_y + h1 +h2]
V[3, 0:2] = [c_x - lx_down /2, c_y + h1]
V[4, 0:2] = [-x_span/2, c_y + h1]
V[5, 0:2] = [-x_span/2, c_y]
V[6, 0:2] = [x_span/2, c_y]
V[7, 0:2] = [x_span/2, c_y +h1]


device.addrect(name = "LiNbO3 Handle", x = 0, x_span = x_span,y =0, y_span= 20e-6,z = -6e-6, z_span= Si_Base,
               material =  "LiNbO3 semiconductor - X/Y cut (Lithium Niobate)")

device.addrect(name = "SiO2 Substrate", x = 0, x_span =x_span,y =0, y_span= 20e-6,z = 1.5e-6, z_span= SiO2_base,
               material =  "SiO2 (Glass) - Sze")
# device.addrect(name = "LiNbO3 Wg 1", x = 0, x_span = 50e-6,y =0, y_span= 20e-6,z = 2.15e-6, z_span= 0.3e-6,
#                material =  "LiNbO3 semiconductor - X/Y cut (Lithium Niobate)")

device.addpoly(name = "LiNbO3 WG",x = 0, y =0, z = 0, first_axis = "x"
		, rotation_1 =90, z_span = 20e-6, vertices = V, material = "LiNbO3 semiconductor - X/Y cut (Lithium Niobate)")



device.addrect(name = "Ground Electrode Left", x = -electrode_width - Gap , x_span = electrode_width,y =0, y_span= 20e-6,z = c_y +electrode_hight/2 + h1, z_span= electrode_hight,
               material =  "Au (Gold) - CRC")

device.addrect(name = "Signal Electrode", x = 0, x_span = electrode_width,y =0, y_span= 20e-6,z = c_y +electrode_hight/2 +h1, z_span= electrode_hight,
               material =  "Au (Gold) - CRC")

device.addrect(name = "Ground Electrode Right", x = electrode_width + Gap, x_span = electrode_width,y =0, y_span= 20e-6,z = c_y +electrode_hight/2 + h1, z_span= electrode_hight,
               material =  "Au (Gold) - CRC")

device.select("simulation region")

device.set("x", c_x)
device.set("x span", 20e-6)

device.set("z", c_y)
device.set("z span", 7e-6)

device.set("background material", "UV15")

device.addchargesolver(solver_mode = "steady state", temperature_dependence = "isothermal", norm_length = 10000e-6,min_edge_length = 0.01e-6, max_edge_length = 4e-6 )

device.addelectricalcontact(name = "Signal" , sweep_type = "range", range_start  = 0 , range_stop = 5, range_num_points = 17,
                             surface_type = "solid" , solid = "Signal Electrode")
device.set("bc mode" , "steady state")
device.set("force ohmic" , True )

device.addelectricalcontact(name = "Ground" , sweep_type = "single", voltage = 0, range_num_points = 17,
                             surface_type = "solid" , solid = "Ground Electrode Left")
device.set("bc mode" , "steady state")
device.set("force ohmic" , True )

device.addefieldmonitor(name = "monitor" , record_electric_field = 1)
device.set( "monitor type" , "2D y-normal")
device.set( "x" , c_x)
device.set( "x span" , 32e-6)
device.set( "y" , 0)
device.set( "z", c_y + h2)
device.set("z span",2e-6 )

device.addmesh()
device.set("geometry type" , "volume")
device.set("volume type" , "solid")
device.set("volume solid" ,"LiNbO3 WG")
device.set("max edge length", 0.01e-6)

charge = open("LN_phase_modulator_CHARGE.lsf").read()
device.eval(charge)


device.switchtolayout()

device.addfeemsolver(number_of_trial_modes = 20, wavelength = 1.55e-6, edges_per_wavelength = 4,
                     polynomial_order= 2,use_max_index = 0, n = 2.02)

device.addpml( sigma = 5)
device.addpec( surface_type = "simulation region",x_min = 1, x_max = 1 , y_min = 1 , y_max= 1 ,
              z_min = 1 , z_max = 1)
device.addimportnk(name= "nk import",volume_type = "solid", volume_solid = "LNOI waveguide")

device.select("simulation region")

device.set("x span", 8e-6 + lx_down)


device.set("z span", 5e-6)
feem = open("LN_phase_modulator_FEEM.lsf").read()
device.eval(feem)

