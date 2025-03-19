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

angle = 70
height2=0.3e-6
width1=0.6e-6
device.addrect(name = "LiNbO3 Handle", x = 0, x_span = 50e-6,y =0, y_span= 20e-6,z = -9.5e-6, z_span= 9e-6,
               material =  "LiNbO3 semiconductor - X/Y cut (Lithium Niobate)")

device.addrect(name = "SiO2 Substrate", x = 0, x_span = 50e-6,y =0, y_span= 20e-6,z = -1.5e-6, z_span= 7e-6,
               material =  "LiNbO3 semiconductor - X/Y cut (Lithium Niobate)")
device.addrect(name = "LiNbO3 Wg 1", x = 0, x_span = 50e-6,y =0, y_span= 20e-6,z = 2.15e-6, z_span= 0.3e-6,
               material =  "LiNbO3 semiconductor - X/Y cut (Lithium Niobate)")
device.addwaveguide(name = "Left waveguide",base_angle = angle, base_height= height2, base_width=width1,
               material =  "LiNbO3 semiconductor - X/Y cut (Lithium Niobate)")

device.setnamed("Left waveguide","poles",np.array([[0 , -10e-6 ],
                                         [0 , 10e-6 ]]))
device.setnamed("Left waveguide","z",2.3e-6 + height2*0.5)
#addemmaterialproperty("Conductive");
#addhtmaterialproperty("Solid");
#addctmaterialproperty("Insulator");