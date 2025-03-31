# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 23:23:31 2024

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
import matplotlib.pyplot as plt

sys.path.append("C:/Program Files/Lumerical/v241/api/python/")
sys.path.append(os.path.dirname(__file__))
#lumapi = imp.load_source("lumapi","C:/Program Files/Lumerical/v241/api/python/lumapi.py")
#os.add_dll_directory("C:/Program Files/Lumerical/v241/api/python")

dir_mat="Material_script/LNOI_materials.lsf"
import lumapi

def num_of_modes(S):
    g=np.gradient(np.gradient(S))
    mode=np.argmin(np.abs(g))
    return mode
def SSC_sim(length,angle_side,wg_max,wg_min,cell_points, wl, # basic tapper simulation
            length_analysis,length_span, # length optimization
            wl_analysis, wl_span  #wavelength s parameters
            ):
    # def mode_analysis(waveguide_w,angle,boundry,rad):
    mode1=lumapi.MODE()
    thickness=0.3e-6
    width_l=wg_max
    width_r=wg_min
    delta_w = 2*thickness*np.tan((90-angle_side)*np.pi/180);

    

    
    centered_x = 0
    centered_y = 0
    centered_z = 0
    # width_film_x =length_x + 10e-6 # el largo total de la base es el largo total del SSC + 10um
    # width_film_y =15e-6
    base_hight= 3e-6
    LN_hight_sub=0.3e-6
    # LN_hight_wg=0.3e-6
    
    delta_w = 2*thickness*np.tan((90-angle_side)*np.pi/180);

    hfrac_ref = 0

    width_top_l = width_l - (1-hfrac_ref)*delta_w
    width_top_r = width_r - (1-hfrac_ref)*delta_w

    width_bot_l = width_l + hfrac_ref*delta_w;
    width_bot_r = width_r + hfrac_ref*delta_w;

    zmin = -thickness/2; #altura maxima
    zmax = thickness/2; #altura minima
    
    xmin = -length/2;
    xmax = length/2;
    
    ymin_bot_l = -width_bot_l/2; # ancho minimo en el lado izquierdo abajo
    ymax_bot_l = width_bot_l/2; #ancho max en el lado izquiero abajo


    ymin_bot_r = -width_bot_r/2; #ancho min en el lado derecho abajo
    ymax_bot_r = width_bot_r/2; #ancho min en el lado derecho abajo


    ymin_top_l = -width_top_l/2; #ancho min en el lado izquiero arriba
    ymax_top_l = width_top_l/2; #ancho max en el lado izquierdo arriba


    ymin_top_r = -width_top_r/2; # ancho min en el lado derecho arriba
    ymax_top_r = width_top_r/2; # ancho max en el lado derecho arriba
    
    materials = open(dir_mat).read()
    
    mode1.eval(materials)
    
    width_film_y =  width_bot_l*1.5
    
    #print(width_film_y)
    
    mode1.addrect(name="Si_substrate",x_min = xmin- length/2 -centered_x , x_max=xmax,
                   y = centered_y, y_span=width_film_y, z_min = centered_z, z_max= base_hight, material = "Si_Salzberg" )
    
    centered_z=base_hight;
    
    mode1.addrect(name="SiO2_cladding",x_min = xmin- length/2 -centered_x , x_max=xmax,
    		 y = centered_y, y_span=width_film_y, z_min = centered_z,
    		 z_max= centered_z +base_hight, material = "SiO2_fusedquartz" )
    centered_z=centered_z +base_hight
    
    mode1.addrect(name="LN_core1",x_min = xmin- length/2 -centered_x , x_max=xmax,
    		 y = centered_y, y_span=width_film_y, z_min = centered_z,
    		 z_max= centered_z+ LN_hight_sub, material = "LN_SE" )
    centered_z=centered_z+LN_hight_sub*1.5
    
    
    
    vtx=[
        [xmin,ymin_bot_l,zmin],    #1
        [xmax,ymin_bot_r,zmin],     #2
        [xmax,ymax_bot_r,zmin],     #3
        [xmin,ymax_bot_l,zmin],     #4  
        [xmin,ymin_top_l,zmax],     #5
        [xmax,ymin_top_r,zmax],     #6
        [xmax,ymax_top_r,zmax],     #7  
        [xmin,ymax_top_l,zmax] #8
             ]
    vtx_input=[
        [xmin - length/2,ymin_bot_l,zmin],    #1
        [xmin,ymin_bot_l,zmin],     #2
        [xmin,ymax_bot_l,zmin],     #3
        [xmin - length/2,ymax_bot_l,zmin],     #4  
        [xmin - length/2,ymin_top_l,zmax],     #5
        [xmin,ymin_top_l,zmax],     #6
        [xmin,ymax_top_l,zmax],     #7  
        [xmin - length/2,ymax_top_l,zmax] #8
             ]
    # Multiplicar cada coordenada por 1e-6
    vtx = np.array(vtx)
    vtx_input = np.array(vtx_input)
    
    
    # Definir las facetas directamente en formato de matriz
    b = np.zeros((4, 1, 6), dtype=int)
        
    b[:, 0, 0] = [1, 4, 3, 2]   # Faceta inferior (plano XY)
    b[:, 0, 1] = [1, 2, 6, 5]   # Faceta superior (plano XY)
    b[:, 0, 2] = [2, 3, 7, 6]   # Faceta lateral izquierda (plano YZ)
    b[:, 0, 3] = [3, 4, 8, 7]   # Faceta lateral derecha (plano YZ)
    b[:, 0, 4] = [1, 5, 8, 4]   # Faceta lateral arriba (plano XZ)
    b[:, 0, 5] = [5, 6, 7, 8]   # Faceta lateral abajo (plano XZ)
    
    
    
    mode1.addplanarsolid(name="SSC",x = centered_x,y = centered_y, z= centered_z, material = "LN_SE")
    mode1.set('vertices',vtx)
    mode1.set('facets',b)
    
    mode1.addplanarsolid(name="Input",x = centered_x ,y = centered_y, z= centered_z, material = "LN_SE")
    mode1.set('vertices',vtx_input)
    mode1.set('facets',b)
    
    mode1.addmesh(name = "mesh_waveguide", x_min = -length/2 , x_max = length/2,
      		y = 0 , y_span= 1e-6, z = centered_z, z_span = 0.3e-6,
      		override_x_mesh = 0, override_y_mesh = 1,
      		override_z_mesh = 1, set_maximum_mesh_step = 1,
      		dy = 15e-9, dz = 15e-9)
    
    mode1.addeme(x_min = xmin- length/2 -centered_x, y = centered_y, y_span= width_bot_l,z=centered_z, z_span= 0.3e-6 )
    mode1.set("number of cell groups",3)
    mode1.set("group spans",np.array([[length/2], [length], [0]]))
    mode1.set("cells",np.array([[1],[ cell_points],[ 1]]))
    mode1.set("subcell method",np.array([[0],[ 1], [0]]))
    mode1.set("number of modes for all cell groups" , 35);
    
    # set up ports: port 1
    mode1.select("EME::Ports::port_1")
    mode1.set("use full simulation span",1)
    mode1.set("y",0)
    mode1.set("y span",width_film_y)
    mode1.set("z",0)
    mode1.set("z span",0.3e-6)
    mode1.set("mode selection","fundamental mode")
    # set up ports: port 2
    mode1.select("EME::Ports::port_2")
    mode1.set("use full simulation span",1)
    mode1.set("y",0)
    mode1.set("y span",width_film_y)
    mode1.set("z",0)
    mode1.set("z span",0.3e-6)
    mode1.set("mode selection","fundamental mode")
    
    mode1.setactivesolver("EME")
    mode1.addemeprofile(x_min = xmin - length/2, x_max= xmax, y = centered_y, y_span = width_film_y, z =centered_z)
    mode1.run()
    
    #Get a fair number of modes
    # mode1.setemeanalysis("mode convergence sweep",1)
    # mode1.setemeanalysis("start mode",1)
    # mode1.setemeanalysis("mode interval",1)
    # mode1.emesweep("mode convergence sweep");
    # S_mode_p=mode1.getemesweep("S_mode_convergence_sweep")
    # n_mode= num_of_modes(np.abs(S_mode_p["s21"]))
    # print( n_mode)
    
    if length_analysis == 1:
        # #set propagation sweep settings
        mode1.setemeanalysis("propagation sweep",1);
        mode1.setemeanalysis("parameter","group span 2");
        mode1.setemeanalysis("start", length - length_span/2);
        mode1.setemeanalysis("stop",length + length_span/2);
        mode1.setemeanalysis("number of points",201);
        # # run propagation sweep tool
        mode1.emesweep("propagation sweep");
        
        S = mode1.getemesweep('S');
        a=plt.plot(S["group_span_2"],np.abs(S["s21"]))
        plt.show(a)
        #print(S)
    if wl_analysis ==1:
        mode1.setemeanalysis("wavelength sweep",1);
        mode1.setemeanalysis("start wavelength", wl - wl_span/2);
        mode1.setemeanalysis("stop wavelength",wl + wl_span/2);
        mode1.setemeanalysis("number of wavelength points", 200);
        mode1.emesweep("wavelength sweep");
        mode1.exportemesweep("Interconnect/s_param_tapper", "lumerical");
        print("Salio Bien")
        
    
    #mode1.emepropagate()
    input("Presiona Enter para finalizar...")
    return 0
def mmi_sim(ssc_length,angle_side,wg_max,wg_min,cell_points,MMi_width,MMi_length,distance,wl, # basic tapper simulation
            length_analysis,length_span, # length optimization
            wl_analysis, wl_span  #wavelength s parameters
            ):


    #mode1=lumapi.MODE()
    
    length=ssc_length
    
    #MMi_width =3e-6
    #MMi_length= 4e-6
    
    mode1=lumapi.MODE()
    thickness=0.3e-6
    width_l=wg_max
    width_r=wg_min
    delta_w = 2*thickness*np.tan((90-angle_side)*np.pi/180);
    
    hfrac_ref = 0
    
    width_top_l = width_l - (1-hfrac_ref)*delta_w
    width_top_r = width_r - (1-hfrac_ref)*delta_w

    width_bot_l = width_l + hfrac_ref*delta_w;
    width_bot_r = width_r + hfrac_ref*delta_w;
    
    width_bot_l = width_l + hfrac_ref*delta_w;
    width_bot_r = width_r + hfrac_ref*delta_w;
    
    ## MMi tengo que arreglar esto
    width_bot_l_MMi = MMi_width + hfrac_ref*delta_w;
    width_bot_r_MMi = MMi_width + hfrac_ref*delta_w;
    
    width_top_l_MMi = MMi_width - (1-hfrac_ref)*delta_w
    width_top_r_MMi = MMi_width - (1-hfrac_ref)*delta_w
    
    ###
    zmin = -thickness/2; #altura maxima
    zmax = thickness/2; #altura minima


    xmin = -length/2;
    xmax = length/2;
    #for MMi
    xmin_mmi = -MMi_length/2;
    xmax_mmi = MMi_length/2;

    #left
    ymin_bot_l_l = -width_bot_r/2; # ancho minimo en el lado izquierdo abajo
    ymax_bot_l_l = width_bot_r/2; #ancho max en el lado izquiero abajo


    ymin_bot_r_l = -width_bot_l/2; #ancho min en el lado derecho abajo
    ymax_bot_r_l = width_bot_l/2; #ancho min en el lado derecho abajo


    ymin_top_l_l = -width_top_r/2; #ancho min en el lado izquiero arriba
    ymax_top_l_l = width_top_r/2; #ancho max en el lado izquierdo arriba


    ymin_top_r_l = -width_top_l/2; # ancho min en el lado derecho arriba
    ymax_top_r_l = width_top_l/2; # ancho max en el lado derecho arriba
    
    #right

    ymin_bot_l_r = -width_bot_l/2; # ancho minimo en el lado izquierdo abajo
    ymax_bot_l_r = width_bot_l/2; #ancho max en el lado izquiero abajo


    ymin_bot_r_r = -width_bot_r/2; #ancho min en el lado derecho abajo
    ymax_bot_r_r = width_bot_r/2; #ancho min en el lado derecho abajo


    ymin_top_l_r = -width_top_l/2; #ancho min en el lado izquiero arriba
    ymax_top_l_r = width_top_l/2; #ancho max en el lado izquierdo arriba


    ymin_top_r_r = -width_top_r/2; # ancho min en el lado derecho arriba
    ymax_top_r_r = width_top_r/2; # ancho max en el lado derecho arriba    
    
    #MMI
    
    ymin_bot_l_mmi = -width_bot_l_MMi/2; # ancho minimo en el lado izquierdo abajo
    ymax_bot_l_mmi = width_bot_l_MMi/2; #ancho max en el lado izquiero abajo


    ymin_bot_r_mmi = -width_bot_r_MMi/2; #ancho min en el lado derecho abajo
    ymax_bot_r_mmi = width_bot_r_MMi/2; #ancho min en el lado derecho abajo


    ymin_top_l_mmi = -width_top_l_MMi/2; #ancho min en el lado izquiero arriba
    ymax_top_l_mmi = width_top_l_MMi/2; #ancho max en el lado izquierdo arriba


    ymin_top_r_mmi = -width_top_r_MMi/2; # ancho min en el lado derecho arriba
    ymax_top_r_mmi = width_top_r_MMi/2; # ancho max en el lado derecho arriba   
    
    #
    centered_x = 0
    centered_y = 0
    centered_z = 0

    #width_film_y =15e-6
    base_hight= 3e-6
    LN_hight_sub=0.3e-6

    
        

    vtx_l=[
        [xmin,ymin_bot_l_l,zmin],    #1
        [xmax,ymin_bot_r_l,zmin],     #2
        [xmax,ymax_bot_r_l,zmin],     #3
        [xmin,ymax_bot_l_l,zmin],     #4  
        [xmin,ymin_top_l_l,zmax],     #5
        [xmax,ymin_top_r_l,zmax],     #6
        [xmax,ymax_top_r_l,zmax],     #7  
        [xmin,ymax_top_l_l,zmax] #8
             ]    
    vtx_r=[
        [xmin,ymin_bot_l_r,zmin],    #1
        [xmax,ymin_bot_r_r,zmin],     #2
        [xmax,ymax_bot_r_r,zmin],     #3
        [xmin,ymax_bot_l_r,zmin],     #4  
        [xmin,ymin_top_l_r,zmax],     #5
        [xmax,ymin_top_r_r,zmax],     #6
        [xmax,ymax_top_r_r,zmax],     #7  
        [xmin,ymax_top_l_r,zmax] #8
             ]
    
    vtx_mmi=[
        [xmin_mmi,ymin_bot_l_mmi,zmin],    #1
        [xmax_mmi,ymin_bot_r_mmi,zmin],     #2
        [xmax_mmi,ymax_bot_r_mmi,zmin],     #3
        [xmin_mmi,ymax_bot_l_mmi,zmin],     #4  
        [xmin_mmi,ymin_top_l_mmi,zmax],     #5
        [xmax_mmi,ymin_top_r_mmi,zmax],     #6
        [xmax_mmi,ymax_top_r_mmi,zmax],     #7  
        [xmin_mmi,ymax_top_l_mmi,zmax] #8
             ]
        
    vtx_l = np.array(vtx_l)
        
    # Multiplicar cada coordenada por 1e-6
    vtx_r = np.array(vtx_r)
    vtx_mmi = np.array(vtx_mmi)
    # vtx_MMi=np.array(vtx_MMi)
    # vtx_input_dual=np.array(vtx_input_dual)
    
    # Definir las facetas directamente en formato de matriz
    b = np.zeros((4, 1, 6), dtype=int)
        
    b[:, 0, 0] = [1, 4, 3, 2]   # Faceta inferior (plano XY)
    b[:, 0, 1] = [1, 2, 6, 5]   # Faceta superior (plano XY)
    b[:, 0, 2] = [2, 3, 7, 6]   # Faceta lateral izquierda (plano YZ)
    b[:, 0, 3] = [3, 4, 8, 7]   # Faceta lateral derecha (plano YZ)
    b[:, 0, 4] = [1, 5, 8, 4]   # Faceta lateral arriba (plano XZ)
    b[:, 0, 5] = [5, 6, 7, 8]   # Faceta lateral abajo (plano XZ)
    
    
    materials = open(dir_mat).read()
    
    mode1.eval(materials)
    
    
    mode1.addrect(name="Si_substrate",x = centered_x, x_span = 2*length + MMi_length,
                 y = centered_y, y_span=width_bot_r_MMi*1.5, z_min = centered_z, z_max= base_hight , material = "Si_Salzberg" )
    
    centered_z=base_hight;
    
    mode1.addrect(name="SiO2_cladding",x = centered_x, x_span=2*length + MMi_length,
    		 y = centered_y, y_span=width_bot_r_MMi*1.5, z_min = centered_z,
    		 z_max= centered_z +base_hight , material = "SiO2_fusedquartz")
    centered_z=centered_z +base_hight
    
    mode1.addrect(name="LN_core1",x = centered_x, x_span=2*length + MMi_length,
    		 y = centered_y, y_span=width_bot_r_MMi*1.5, z_min = centered_z,
    		 z_max= centered_z+ LN_hight_sub, material = "LN_SE" )
    centered_z=centered_z+LN_hight_sub
    
    #input output
    
    mode1.addplanarsolid(name="SSC_l",x = centered_x - MMi_length/2 -length/2,y = centered_y, z= centered_z + thickness/2, material = "LN_SE")
    mode1.set('vertices',vtx_l)
    mode1.set('facets',b)
    
    mode1.addplanarsolid(name="SSC_r_down",x = centered_x + MMi_length/2 + length/2,y = centered_y + distance/2 +width_l/2, z= centered_z + thickness/2, material = "LN_SE")
    mode1.set('vertices',vtx_r)
    mode1.set('facets',b)
    
    mode1.addplanarsolid(name="SSC_r_up",x = centered_x + MMi_length/2 + length/2,y = centered_y - distance/2 - width_l/2, z= centered_z + thickness/2, material = "LN_SE")
    mode1.set('vertices',vtx_r)
    mode1.set('facets',b)
    
    #output
    
    mode1.addplanarsolid(name="MMi",x = centered_x ,y = centered_y , z= centered_z + thickness/2, material = "LN_SE")
    mode1.set('vertices',vtx_mmi)
    mode1.set('facets',b)
    
    

    
    # port_length=Sizeinput + length_x
    mode1.addeme(x_min =  -MMi_length/2 - length, y = 0, y_span= width_bot_r_MMi*1.5,z=centered_z + LN_hight_sub/2, z_span= LN_hight_sub +0.5e-6 )
    mode1.set("number of cell groups",3)
    mode1.set("group spans",np.array([[length], [MMi_length], [length]]))
    mode1.set("cells",np.array([[cell_points],[ 1],[ cell_points]]))
    mode1.set("subcell method",np.array([[1],[ 0], [1]]))
    
    # set up ports: port 1
    mode1.select("EME::Ports::port_1")
    mode1.set("use full simulation span",1)
    mode1.set("y",0)
    mode1.set("y span",width_bot_r)
    mode1.set("z",0)
    mode1.set("z span", 2*LN_hight_sub)
    mode1.set("mode selection","fundamental mode")
    # set up ports: port 2
    mode1.select("EME::Ports::port_2")
    mode1.set("use full simulation span",1)
    mode1.set("y",centered_y - distance/2 - width_l/2)
    mode1.set("y span",width_bot_r)
    mode1.set("z",0)
    mode1.set("z span", 2*LN_hight_sub)
    mode1.set("mode selection","fundamental mode")
    
    mode1.addemeport()
    mode1.select("EME::Ports::port_3")
    mode1.set("use full simulation span",1)
    mode1.set("y", centered_y + distance/2 + width_l/2)
    mode1.set("y span",width_bot_r)
    mode1.set("z",0)
    mode1.set("z span", 2*LN_hight_sub)
    mode1.set("mode selection","fundamental mode")
    mode1.set("port location","right")
    
    mode1.setactivesolver("EME")
    mode1.addemeprofile(x = centered_x, y = centered_y, x_span = MMi_length + 2*length,y_span =width_bot_r_MMi*1.5, z =centered_z + LN_hight_sub/2)
    mode1.addmesh(name = "mesh_waveguide", x_min = centered_x - MMi_length/2 -length/2 + xmin , x_max = centered_x - MMi_length/2 -length/2 +xmax,
      		y = centered_y , y_span= width_bot_l, z = centered_z + thickness/2, z_span = thickness,
      		override_x_mesh = 0, override_y_mesh = 1,
      		override_z_mesh = 1, set_maximum_mesh_step = 1,
      		dy = 15e-9, dz = 15e-9)

    mode1.addmesh(name = "mesh_waveguide", x_min = centered_x + MMi_length/2 + length/2 + xmin , x_max = centered_x + MMi_length/2 + length/2 +xmax,
      		y = centered_y + distance/2 +width_l/2 , y_span= width_bot_l, z = centered_z + thickness/2, z_span = thickness,
      		override_x_mesh = 0, override_y_mesh = 1,
      		override_z_mesh = 1, set_maximum_mesh_step = 1,
      		dy = 15e-9, dz = 15e-9)
    
    mode1.addmesh(name = "mesh_waveguide", x_min = centered_x + MMi_length/2 + length/2 + xmin , x_max = centered_x + MMi_length/2 + length/2 +xmax,
      		y = centered_y - distance/2 - width_l/2 , y_span= width_bot_l, z = centered_z + thickness/2, z_span = thickness,
      		override_x_mesh = 0, override_y_mesh = 1,
      		override_z_mesh = 1, set_maximum_mesh_step = 1,
      		dy = 15e-9, dz = 15e-9)
    
    mode1.run()
    
    if length_analysis == 1:
        # #set propagation sweep settings
        mode1.setemeanalysis("propagation sweep",1);
        mode1.setemeanalysis("parameter","group span 1");
        mode1.setemeanalysis("start", length - length_span/2);
        mode1.setemeanalysis("stop",length + length_span/2);
        mode1.setemeanalysis("number of points",201);
        # # run propagation sweep tool
        mode1.emesweep("propagation sweep");
        
        S = mode1.getemesweep('S');
        a=plt.plot(S["group_span_1"],np.abs(S["s21"]))
        plt.show(a)
        
        mode1.setemeanalysis("parameter","group span 3");
        mode1.setemeanalysis("start", length - length_span/2);
        mode1.setemeanalysis("stop",length + length_span/2);
        mode1.setemeanalysis("number of points",201);
        # # run propagation sweep tool
        mode1.emesweep("propagation sweep");
        
        S = mode1.getemesweep('S');
        a=plt.plot(S["group_span_3"],np.abs(S["s21"]))
        plt.show(a)
        #print(S)
    if wl_analysis ==1:
        mode1.setemeanalysis("wavelength sweep",1);
        mode1.setemeanalysis("start wavelength", wl - wl_span/2);
        mode1.setemeanalysis("stop wavelength",wl + wl_span/2);
        mode1.setemeanalysis("number of wavelength points", 200);
        mode1.emesweep("wavelength sweep");
        mode1.exportemesweep("Interconnect/s_param_MMI", "lumerical");
        print("Salio Bien")
    mode1.emepropagate()
    
    input("preciona para apagar....")
    return 0


#mmi_sim(ssc_length,angle,wg_max,wg_min,space,MMi_width,MMi_length,distance)
#mmi_sim(1e-6,80,0.8e-6,0.6e-6,19,2e-6,2e-6,0.3e-6,1.55e-6,0,0,0,0)
#SSC_sim(5e-6,80,1e-6,0.5e-6,0)
    
    




