# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 12:54:21 2025

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

# Lw: length of the three individual straight waveguide sections
#     at the input and output ports
# Ls: x span of the s-bend sections
# base angle: sidewall angle of the waveguide
# base height: height of the waveguide
# base width: width of the waveguide base
# y span: Center-to-center distance between the two input ports

def y_splitter(base_angle, base_width, y_span, Lw, Ls):
    mode1=lumapi.MODE()

    
    #base_angle = 70;
    #base_width = 0.5e-6;
    base_height = 0.3e-6
    #y_span = 6e-6;
    #Lw = 4e-6
    #Ls = 6e-6
    width_film_y= y_span + 2e-6
    width_film_x= 2*Lw + Ls
    centered_x = width_film_x/2
    centered_y = 0
    centered_z = 0
    base_hight= 3e-6
    LN_hight_sub=0.3e-6
        
    materials = open(dir_mat).read()
    
    mode1.eval(materials)
    
    mode1.addwaveguide(name = "straight_in" )
    mode1.addwaveguide(name = "straight_out1" )
    mode1.addwaveguide(name = "straight_out2")
    mode1.addwaveguide(name = "s_bend_1")
    mode1.addwaveguide(name = "s_bend_2")
    
    mode1.selectall()
    mode1.set("detail",0.5)
    mode1.set("material","LN_SE");
    mode1.set("base angle",base_angle)
    mode1.set("base height",base_height)
    mode1.set("base width",base_width)
    mode1.unselectall()
    
    
    mode1.addrect(name="Si_substrate",x = centered_x, x_span=width_film_x,
                   y = centered_y, y_span=width_film_y, z_min = centered_z, z_max= base_hight, material = "Si_Salzberg" )
    
    centered_z=base_hight;
    
    mode1.addrect(name="SiO2_cladding",x = centered_x, x_span=width_film_x,
    		 y = centered_y, y_span=width_film_y, z_min = centered_z,
    		 z_max= centered_z +base_hight, material = "SiO2_fusedquartz" )
    centered_z=centered_z +base_hight
    
    mode1.addrect(name="LN_core1",x = centered_x, x_span=width_film_x,
    		 y = centered_y, y_span=width_film_y, z_min = centered_z,
    		 z_max= centered_z+ LN_hight_sub, material = "LN_SE" )
    centered_z=centered_z+LN_hight_sub*1.5
    
    
    mode1.setnamed("straight_in","poles",np.array([[0,0],[Lw,0]]))
    mode1.setnamed("straight_in","z",centered_z)
    
    mode1.setnamed("straight_out1","poles",np.array([[Lw+Ls,y_span/2],[2*Lw+Ls,y_span/2]]))
    mode1.setnamed("straight_out1","z",centered_z)
    
    mode1.setnamed("straight_out2","poles",np.array([[Lw+Ls,-y_span/2],[2*Lw+Ls,-y_span/2]]))
    mode1.setnamed("straight_out2","z",centered_z)
    
    mode1.setnamed("s_bend_1","poles",np.array([[Lw,0],[Lw+Ls/2,0],[Lw+Ls/2,y_span/2],[Lw+Ls,y_span/2]]))
    mode1.setnamed("s_bend_1","z",centered_z)
    
    mode1.setnamed("s_bend_2","poles",np.array([[Lw,0],[Lw+Ls/2,0],[Lw+Ls/2,-y_span/2],[Lw+Ls,-y_span/2]]))
    mode1.setnamed("s_bend_2","z",centered_z)
    
    mode1.addvarfdtd(x = centered_x, x_span =width_film_x, y = centered_y, y_span= width_film_y ,z=centered_z, z_span= 0.5e-6 )        
    mode1.addprofile(x = centered_x, x_span = width_film_x, y = centered_y, y_span= width_film_y ,z=centered_z)
    mode1.addmodesource(injection_axis="x" , x = 0 , y= 0 ,
                        y_span = base_width,wavelength_start=1.5e-6,wavelength_stop=1.9e-6);
    
    mode1.addpower(name = "Up",monitor_type= "Linear Y",x = 2*Lw+Ls, y = y_span/2, y_span = base_width, z =centered_z)
    mode1.addpower(name = "Down",monitor_type= "Linear Y",x = 2*Lw+Ls, y = - y_span/2,  y_span = base_width, z =centered_z)    
   
    mode1.run()

    input("Presiona Enter para finalizar...")
    
    return 0

def PowerCoupler(base_angle, base_width, y_span, Lw, Ls, gap,Lc):
    mode1=lumapi.MODE()
    
    #constants 

    
    #base_angle = 70;
    #base_width = 0.65e-6;
    base_height = 0.3e-6
    #y_span = 8e-6;
    #Lw = 3e-6
    #Ls = 5e-6
    
    #gap = 0.2e-6
    #Lc =3e-6
    width_film_y= y_span + 2e-6
    width_film_x= Lc + 2*Lw + 2*Ls
    centered_x = width_film_x/2
    centered_y = 0
    centered_z = 0
    base_hight= 3e-6
    LN_hight_sub=0.3e-6
    
    
    
    materials = open(dir_mat).read()
    
    mode1.eval(materials)
    
    mode1.addwaveguide(name = "wg_top_left" )
    mode1.addwaveguide(name = "wg_top_right")
    mode1.addwaveguide(name = "wg_bottom_left")
    mode1.addwaveguide(name = "wg_bottom_right")
    mode1.addwaveguide(name = "bend_top_left")
    mode1.addwaveguide(name = "bend_top_right")
    mode1.addwaveguide(name = "bend_bottom_left")
    mode1.addwaveguide(name = "bend_bottom_right")
    mode1.addwaveguide(name = "couple_top")
    mode1.addwaveguide(name = "couple_bottom")
    
    mode1.selectall()
    mode1.set("detail",0.5)
    mode1.set("material","LN_SE")
    mode1.set("base angle",base_angle)
    mode1.set("base height",base_height)
    mode1.set("base width",base_width)
    mode1.unselectall()
    
    mode1.addrect(name="Si_substrate",x = centered_x, x_span=width_film_x,
                   y = centered_y, y_span=width_film_y, z_min = centered_z, z_max= base_hight, material = "Si_Salzberg" )
    
    centered_z=base_hight;
    
    mode1.addrect(name="SiO2_cladding",x = centered_x, x_span=width_film_x,
    		 y = centered_y, y_span=width_film_y, z_min = centered_z,
    		 z_max= centered_z +base_hight, material = "SiO2_fusedquartz" )
    centered_z=centered_z +base_hight
    
    mode1.addrect(name="LN_core1",x = centered_x, x_span=width_film_x,
    		 y = centered_y, y_span=width_film_y, z_min = centered_z,
    		 z_max= centered_z+ LN_hight_sub, material = "LN_SE" )
    centered_z=centered_z+LN_hight_sub*1.5
    
    
    
    #Upper half
    mode1.setnamed("wg_top_left","poles",np.array([[0,y_span/2],[Lw,y_span/2]]))
    mode1.setnamed("wg_top_left","z",centered_z)
    
    mode1.setnamed("bend_top_left","poles",np.array([[Lw,y_span/2],[Lw+Ls/2,y_span/2],[Lw+Ls/2,(gap+base_width)/2],[Lw+Ls,(gap+base_width)/2]]))
    mode1.setnamed("bend_top_left","z",centered_z)
    
    mode1.setnamed("couple_top","poles",np.array([[Lw+Ls,(gap+base_width)/2],[Lw+Ls+Lc,(gap+base_width)/2]]))
    mode1.setnamed("couple_top","z",centered_z)
    
    mode1.setnamed("bend_top_right","poles",np.array([[Lw+Ls+Lc,(gap+base_width)/2],
    			    [Lw+3*Ls/2+Lc,(gap+base_width)/2],
    			    [Lw+3*Ls/2+Lc,y_span/2],
    			    [Lw+2*Ls+Lc,y_span/2]]))
    mode1.setnamed("bend_top_right","z",centered_z)
    
    mode1.setnamed("wg_top_right","poles",np.array([[Lw+2*Ls+Lc,y_span/2],[2*Lw+2*Ls+Lc,y_span/2]]))
    mode1.setnamed("wg_top_right","z",centered_z)
    
    #Lower half
    mode1.setnamed("wg_bottom_left","poles",np.array([[0,-y_span/2],[Lw,-y_span/2]]))
    mode1.setnamed("wg_bottom_left","z",centered_z)
    
    mode1.setnamed("bend_bottom_left","poles",np.array([[Lw,-y_span/2],[Lw+Ls/2,-y_span/2],[Lw+Ls/2,-(gap+base_width)/2],[Lw+Ls,-(gap+base_width)/2]]))
    mode1.setnamed("bend_bottom_left","z",centered_z)
    
    mode1.setnamed("couple_bottom","poles",np.array([[Lw+Ls,-(gap+base_width)/2],[Lw+Ls+Lc,-(gap+base_width)/2]]))
    mode1.setnamed("couple_bottom","z",centered_z)
    
    mode1.setnamed("bend_bottom_right","poles",np.array([[Lw+Ls+Lc,-(gap+base_width)/2],
    			    [Lw+3*Ls/2+Lc,-(gap+base_width)/2],
    			    [Lw+3*Ls/2+Lc,-y_span/2],
    			    [Lw+2*Ls+Lc,-y_span/2]]))
    mode1.setnamed("bend_bottom_right","z",centered_z)
    
    mode1.setnamed("wg_bottom_right","poles",np.array([[Lw+2*Ls+Lc,-y_span/2],[2*Lw+2*Ls+Lc,-y_span/2]]))
    mode1.setnamed("wg_bottom_right","z",centered_z)
    
    mode1.addvarfdtd(x = centered_x, x_span =width_film_x, y = centered_y, y_span= width_film_y ,z=centered_z, z_span= 0.5e-6 )        
    mode1.addprofile(x = centered_x, x_span = width_film_x, y = centered_y, y_span= width_film_y ,z=centered_z)
    mode1.addmodesource(injection_axis="x" , x = 0 , y= y_span/2 ,
                        y_span = base_width,wavelength_start=1.5e-6,wavelength_stop=1.9e-6);
    
    mode1.addpower(name = "transmited",monitor_type= "Linear Y",x = 2*Lw+2*Ls+Lc, y = y_span/2, y_span = base_width, z =centered_z)
    mode1.addpower(name = "isolation",monitor_type= "Linear Y",x = 0, y = - y_span/2,  y_span = base_width, z =centered_z)
    mode1.addpower(name = "coupled",monitor_type= "Linear Y",x = 2*Lw+2*Ls+Lc, y = - y_span/2,  y_span = base_width, z =centered_z)

    
    mode1.run()
    
    input("Presiona Enter para finalizar...")

#base_angle = 70;
#base_width = 0.5e-6;
#y_span = 6e-6;
#Lw = 4e-6
#Ls = 6e-6
#y_splitter(90, 0.6e-6, 6e-6, 4e-6, 6e-6)
    #y_span = 8e-6;
    #Lw = 3e-6
    #Ls = 5e-6
    
    #gap = 0.2e-6
    #Lc =3e-6
#PowerCoupler(90, 0.65e-6, 8e-6, 3e-6, 5e-6, 0.2e-6,3e-6)
#Aco hago la y





