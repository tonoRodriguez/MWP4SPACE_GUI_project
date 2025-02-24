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

def calc_magnitude_and_phase(S_param):
    magnitude = np.abs(S_param)
    phase = np.unwrap(np.angle(S_param))
    
    return magnitude, phase

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
    LN_hight_sub=height
    
    
    width_film_x = x_span
    width_film_y = radius*2 + gap + base_width +3e-6
    
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
    		 z_max= centered_z +base_hight, material = "SiO2_fusedquartz" )
    centered_z=centered_z +base_hight
    
    mode1.addrect(name="LN_core1",x = centered_x, x_span=width_film_x,
    		 y = centered_y, y_span=width_film_y, z_min = centered_z,
    		 z_max= centered_z+ LN_hight_sub, material = "LN_SE" )
    centered_z=centered_z+LN_hight_sub*1.5
    
    mode1.addwaveguide(name = "outer_top", base_angle = angle, base_height= height, base_width=width, material = "LN_SE")
    mode1.addwaveguide(name = "outer_bottom", base_angle = angle, base_height= height, base_width=width, material = "LN_SE" )
    
    mode1.addwaveguide(name = "inner_top", base_angle = angle, base_height= height, base_width=width, material = "LN_SE" )
    mode1.addwaveguide(name = "inner_bottom", base_angle = angle, base_height= height, base_width=width, material = "LN_SE" )
    
    mode1.addwaveguide(name = "arc1", base_angle = angle, base_height= height, base_width=width, material = "LN_SE" )
    mode1.addwaveguide(name = "arc2" , base_angle = angle, base_height= height, base_width=width, material = "LN_SE")
    mode1.addwaveguide(name = "arc3", base_angle = angle, base_height= height, base_width=width, material = "LN_SE" )
    mode1.addwaveguide(name = "arc4", base_angle = angle, base_height= height, base_width=width, material = "LN_SE" )
    
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
    mode1.set("simulation time", 5e-12)
    
    mode1.addpower(name = "source",monitor_type= "Linear Y",x = 1.5e-6, y = radius+gap+base_width, y_span = base_width, z =centered_z)
    mode1.set("override global monitor settings",1)
    mode1.set("frequency points",1000)
    mode1.addmodesource(injection_axis="x" , x = 1.5e-6, y= radius+gap+base_width,
                        y_span = base_width,wavelength_start=1.4e-6,wavelength_stop=1.6e-6);

    mode1.addprofile(x = x_span/2 , x_span = x_span, y = 0, y_span = width_film_y, z =centered_z )
    mode1.addpower(name = "drop",monitor_type= "Linear Y",x = 1e-6, y = -radius-gap-base_width, y_span = base_width, z =centered_z)
    mode1.set("override global monitor settings",1)
    mode1.set("frequency points",1000)
    #mode1.addmodeexpansion(name = "Drop",monitor_type= "Linear Y",x = 1e-6, y = -radius-gap-base_width, y_span = base_width, z =centered_z)
    mode1.addpower(name = "through",monitor_type= "Linear Y",x = x_span - 1.5e-6, y = radius+gap+base_width,  y_span = base_width, z =centered_z)
    mode1.set("override global monitor settings",1)
    mode1.set("frequency points",1000)
    #mode1.addmodeexpansion(name = "Through",monitor_type= "Linear Y",x = x_span - 1.5e-6, y = radius+gap+base_width,  y_span = base_width, z =centered_z)
    mode1.addpower(name = "drop2",monitor_type= "Linear Y",x = x_span - 1.5e-6, y = radius+gap+base_width,  y_span = base_width, z =centered_z)
    mode1.set("override global monitor settings",1)
    mode1.set("frequency points",1000)
    
    #Mode expansion Monitors
    mode1.addmodeexpansion(name = "expansion",monitor_type= "Linear Y",x = 1.5e-6, y= radius+gap+base_width, y_span = base_width, z =centered_z)
    mode1.setexpansion("input","source")
    mode1.setexpansion("drop","drop")
    mode1.setexpansion("through","through")
    mode1.setexpansion("drop2","drop2")
    mode1.run()
    e_in=mode1.getresult("expansion","expansion for input")
    e_drop=mode1.getresult("expansion","expansion for drop")
    e_through=mode1.getresult("expansion","expansion for through")
    e_drop2=mode1.getresult("expansion","expansion for drop2")
    
    
    # in      = getresult("expansion","expansion for in");
    # through = getresult("expansion","expansion for through");
    # drop    = getresult("expansion","expansion for drop");
    # drop2   = getresult("expansion","expansion for drop2");

    # S11 = S22 = S33 = S44 = in.b/in.a;
    # S21 = S12 = S34 = S43 = drop.b/in.a;
    # S31 = S13 = S24 = S42 = through.a/in.a;
    # S41 = S14 = S23 = S32 = drop2.a/in.a;
    
    
    
    S11 = S22 = S33 = S44 =e_in["b"]/e_in["a"]
    S21 = S12 = S34 = S43 = e_drop["b"]/e_in["a"]
    S31 = S13 = S24 = S42 = e_through["a"]/e_in["a"]
    S41 = S14 = S23 = S32 = e_drop2["a"]/e_in["a"]
    f = e_in["f" ]
    # Aplanar todas las variables
    f_flat = f.ravel()
    #lambda_flat = lambda_values.ravel()
    S11_flat = S11.ravel()
    S21_flat = S21.ravel()
    S31_flat = S31.ravel()
    S41_flat = S41.ravel()
    
    # Recalcular magnitudes y fases con las variables aplanadas
    mag_S11, phase_S11 = calc_magnitude_and_phase(S11_flat)
    mag_S21, phase_S21 = calc_magnitude_and_phase(S21_flat)
    mag_S31, phase_S31 = calc_magnitude_and_phase(S31_flat)
    mag_S41, phase_S41 = calc_magnitude_and_phase(S41_flat)
    # Preparar datos para exportación
    Sdata = np.array([
        f_flat,
        mag_S11, phase_S11,
        mag_S21, phase_S21,
        mag_S31, phase_S31,
        mag_S41, phase_S41
        ]).T
    
    # Nombre del archivo de salida
    filename = "Interconnect/Ring_resonator.txt"
    
    # Guardar en archivo con formato largo
    np.savetxt(filename, Sdata, fmt="%.12e", delimiter="\t", header="f\t|S11|\t∠S11\t|S21|\t∠S21\t|S31|\t∠S31\t|S41|\t∠S41")
    # # export to file for INTERCONNECT
    # Sdata = [S.f, abs(S11), unwrap(angle(S11)), abs(S21), unwrap(angle(S21)), abs(S31), unwrap(angle(S31)), abs(S41), unwrap(angle(S41))];
    
    # if(fileexists(filename)) { rm(filename); }
    # format long;
    # write(filename,num2str(Sdata));
    # format short;



    input("Presiona Enter para finalizar...")
    return e_in,e_drop,e_through,e_drop2

#e_in,e_drop,e_through,e_drop2=Ring_Resonator(75, 0.8e-6, 0.1e-6, 20e-6, 50e-6,2)