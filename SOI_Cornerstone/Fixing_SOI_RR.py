# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 10:33:39 2025

@author: Antonio
"""

import numpy as np
#import matplotlib.pyplot as plt
import os
import sys
#import imp

sys.path.append("C:/Program Files/Lumerical/v241/api/python/")
sys.path.append(os.path.dirname(__file__))
#lumapi = imp.load_source("lumapi","C:/Program Files/Lumerical/v241/api/python/lumapi.py")
#os.add_dll_directory("C:/Program Files/Lumerical/v241/api/python")

dir_mat="Material_script/LNOI_materials.lsf"
import lumapi

#angle = 90
height=0.22e-6
#width=0.7e-6
m=0.55191502449
centered_z=0
#radius=50e-6
Lc =0

x_span=10e-6
#gap = 0.25e-6
base_width=0.5e-6
base_hight= 2e-6
LN_hight_sub=height
angle = 90
width = 0.5e-6
width_film_x = 10e-6
radius =10e-6
gap=0.1e-6
width_film_y = radius*2 + gap + base_width + radius/5
centered_x = width_film_x/2
centered_y = 0
centered_z = 0
mode1=lumapi.MODE()

materials = open(dir_mat).read()
mode1.eval(materials)


mode1.addrect(name="Si_substrate",x = centered_x, x_span=width_film_x,
               y = centered_y, y_span=width_film_y, z_min = centered_z, z_max= base_hight, material = "Si_Salzberg" )

centered_z=base_hight;

mode1.addrect(name="SiO2_cladding",x = centered_x, x_span=width_film_x,
		 y = centered_y, y_span=width_film_y, z_min = centered_z,
		 z_max= centered_z +base_hight + 0.5e-6, material = "SiO2_fusedquartz",alpha =0.4 )
centered_z=centered_z +base_hight+LN_hight_sub*0.5

mode1.addwaveguide(name = "outer_top", base_angle = angle, base_height= height, base_width=width, material = "Si_Salzberg")

mode1.setnamed("outer_top","poles",np.array([[0,radius+gap+base_width],
                                             [x_span,radius+gap+base_width]]))
mode1.setnamed("outer_top","z",centered_z)





mode1.addvarfdtd(x = x_span/2 , x_span = x_span, y = 0, y_span = width_film_y, z =centered_z ,z_span = 1e-6)
mode1.set("simulation time", 5e-12)
mode1.addpower(name = "source",monitor_type= "Linear Y",x = 1.5e-6, y = radius+gap+base_width, y_span = base_width, z =centered_z)
mode1.set("override global monitor settings",1)
mode1.set("frequency points",1000)
mode1.addmodesource(injection_axis="x" , x = 1.5e-6, y= radius+gap+base_width,
                    y_span = base_width,wavelength_start=1.4e-6,wavelength_stop=1.6e-6)

mode1.addpower(name = "through",monitor_type= "Linear Y",x = x_span - 1.5e-6, y = radius+gap+base_width,  y_span = base_width, z =centered_z)
mode1.set("override global monitor settings",1)
mode1.set("frequency points",1000)
mode1.addprofile(x = x_span/2 , x_span = x_span, y = 0, y_span = width_film_y, z =centered_z )