# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 12:48:11 2025

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


def Ring_Resonator(angle, width, gap, radius, x_span,b):
    

    #angle = 90
    height=0.3e-6
    #width=0.7e-6
    m=0.55191502449
    centered_z=0
    #radius=50e-6
    Lc =0
    #x_span=120e-6
    #gap = 0.25e-6
    base_width=width
    base_hight= 3e-6
    top_cladding = 2e-6
    LN_hight_sub=height
    
    
    width_film_x = x_span
    width_film_y = radius*2 + gap + base_width + radius/5
    
    centered_x = width_film_x/2
    centered_y = 0
    centered_z = 0
    mode1=lumapi.MODE()
    materials = open(dir_mat).read()
    mode1.eval(materials)
    
    # Poles for four quarter-circles
    px1  = [(x*radius +  +Lc/2+x_span/2) for x in [0,m,1,1]]
    py1 = [radius*x for x in [1,1,m,0]]
    p1 = np.array([[xi, yi] for xi, yi in zip(px1, py1)])
    px2 = [(x*radius+Lc/2+x_span/2) for x in [0,m,1,1]]
    py2 = [x*radius for x in [-1,-1,-m,0]]
    p2 = np.array([[xi, yi] for xi, yi in zip(px2, py2)])
    px3 = [x*radius-Lc/2+x_span/2 for x in [-1,-1,-m,0]]
    py3 = [x*radius for x in [0,-m,-1,-1]]
    p3 = np.array([[xi, yi] for xi, yi in zip(px3, py3)])
    px4 = [radius*x -Lc/2+x_span/2 for x in  [-1,-1,-m,0]]
    py4 = [x*radius for x in [0,m,1,1]]
    p4 = np.array([[xi, yi] for xi, yi in zip(px4, py4)])
    
    mode1.addrect(name="Si_substrate",x = centered_x, x_span=width_film_x,
                   y = centered_y, y_span=width_film_y, z_min = centered_z, z_max= base_hight, material = "Si_Salzberg" )
    
    centered_z=base_hight;
    
    mode1.addrect(name="SiO2_cladding",x = centered_x, x_span=width_film_x,
    		 y = centered_y, y_span=width_film_y, z_min = centered_z,
    		 z_max= centered_z +base_hight + top_cladding, material = "SiO2_fusedquartz" ,alpha = 0.5)
    centered_z=centered_z +base_hight + height*0.5
    
    
    mode1.addwaveguide(name = "outer_top", base_angle = angle, base_height= height, base_width=width, material = "Si3N4_Luke")
    mode1.addwaveguide(name = "outer_bottom", base_angle = angle, base_height= height, base_width=width, material = "Si3N4_Luke" )
    
    mode1.addwaveguide(name = "inner_top", base_angle = angle, base_height= height, base_width=width, material = "Si3N4_Luke" )
    mode1.addwaveguide(name = "inner_bottom", base_angle = angle, base_height= height, base_width=width, material = "Si3N4_Luke" )
    
    mode1.addwaveguide(name = "arc1", base_angle = angle, base_height= height, base_width=width, material = "Si3N4_Luke" )
    mode1.addwaveguide(name = "arc2" , base_angle = angle, base_height= height, base_width=width, material = "Si3N4_Luke")
    mode1.addwaveguide(name = "arc3", base_angle = angle, base_height= height, base_width=width, material = "Si3N4_Luke" )
    mode1.addwaveguide(name = "arc4", base_angle = angle, base_height= height, base_width=width, material = "Si3N4_Luke" )
    
    mode1.setnamed("inner_top","poles",np.array([[-Lc/2+x_span/2,radius],
                                        [Lc/2+x_span/2,radius]]))
    mode1.setnamed("inner_top","z",centered_z)
    
    mode1.setnamed("inner_bottom","poles",np.array([[-Lc/2+x_span/2,-radius],
                                                    [Lc/2+x_span/2,-radius]]))
    mode1.setnamed("inner_bottom","z",centered_z)
    
    mode1.setnamed("outer_top","poles",np.array([[0,radius+gap+base_width],
                                                 [x_span,radius+gap+base_width]]))
    mode1.setnamed("outer_top","z",centered_z)
    
    mode1.setnamed("outer_bottom","poles", np.array([[0,-(radius+gap+base_width)],
                                                     [x_span,-(radius+gap+base_width)]]))
    mode1.setnamed("outer_bottom","z",centered_z)
    
    
    mode1.setnamed("arc1","poles",p1)
    mode1.setnamed("arc1","z",centered_z)
    
    mode1.setnamed("arc2","poles",p2)
    mode1.setnamed("arc2","z",centered_z)
    
    mode1.setnamed("arc3","poles",p3)
    mode1.setnamed("arc3","z",centered_z)
    
    
    mode1.setnamed("arc4","poles",p4)
    mode1.setnamed("arc4","z",centered_z)
    
    
    if (Lc==0 ):
       mode1.setnamed("inner_top","enabled",0)
       
       mode1.setnamed("inner_bottom","enabled",0)
       
    else:
       mode1.setnamed("inner_top","enabled",1)
       mode1.setnamed("inner_bottom","enabled",1)
    if (b==1):
        mode1.setnamed("outer_bottom","enabled",0)
       
    
       
    mode1.addvarfdtd(x = x_span/2 , x_span = x_span, y = 0, y_span = width_film_y, z =centered_z ,z_span = 1e-6)
    
    mode1.addmodesource(injection_axis="x" , x = 1e-6, y= radius+gap+base_width,
                        y_span = base_width,wavelength_start=1.5e-6,wavelength_stop=1.6e-6);
    
    mode1.addprofile(x = x_span/2 , x_span = x_span, y = 0, y_span = width_film_y, z =centered_z )

    mode1.addeffectiveindex(x = x_span/2 , x_span = x_span, y = 0, y_span = width_film_y)
    mode1.addpower(name = "drop",monitor_type= "Linear Y",x =0, y = -radius-gap-base_width, y_span = base_width, z =centered_z)
    mode1.addpower(name = "through",monitor_type= "Linear Y",x = x_span , y = radius+gap+base_width,  y_span = base_width, z =centered_z)
    #mode1.findmodes()
    mode1.run()
    
    input("Presiona Enter para finalizar...")
    return 0
Ring_Resonator(90, 1e-6, 0.1e-6, 50e-6, 120e-6,0)