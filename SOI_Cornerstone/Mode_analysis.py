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

def borders_analysis(S):
    Ex = S["E"][0][:, :, :, 0]  # Extrae la primera componente (E_x)
    Ey = S["E"][0][:, :, :, 1]  # Extrae la segunda componente (E_y)
    Ez = S["E"][0][:, :, :, 2]  # Extrae la tercera componente (E_z)
    Ex_left = np.abs(Ex[0, :, :])  # Campo en el borde izquierdo (x = 0)
    Ex_right = np.abs(Ex[-1, :, :])  # Campo en el borde derecho (x = xmax)
    Ex_bottom = np.abs(Ex[:, 0, :])  # Campo en el borde inferior (y = 0)
    Ex_top = np.abs(Ex[:, -1, :])  # Campo en el borde superior (y = ymax)
    
    Ey_left = np.abs(Ey[0, :, :])  # Campo en el borde izquierdo (x = 0)
    Ey_right = np.abs(Ey[-1, :, :])  # Campo en el borde derecho (x = xmax)
    Ey_bottom = np.abs(Ey[:, 0, :])  # Campo en el borde inferior (y = 0)
    Ey_top = np.abs(Ey[:, -1, :])  # Campo en el borde superior (y = ymax)
    
    Ez_left = np.abs(Ez[0, :, :])  # Campo en el borde izquierdo (x = 0)
    Ez_right = np.abs(Ez[-1, :, :])  # Campo en el borde derecho (x = xmax)
    Ez_bottom = np.abs(Ez[:, 0, :])  # Campo en el borde inferior (y = 0)
    Ez_top = np.abs(Ez[:, -1, :])  # Campo en el borde superior (y = ymax)
    
    Ex_res= max(Ex_right)>0.5 or max(Ex_left)>0.5 or max(Ex_bottom) >0.5 or max(Ex_top)>0.5
    Ey_res= max(Ey_right)>0.5 or max(Ey_left)>0.5 or max(Ey_bottom) >0.5 or max(Ey_top)>0.5
    Ez_res= max(Ez_right)>0.5 or max(Ez_left)>0.5 or max(Ez_bottom) >0.5 or max(Ez_top)>0.5

    if Ex_res or Ey_res or Ez_res:
        return False
    else:
        return True

def mode_analysis(waveguide_w,angle,boundry,rad,wl):
    
    #Parameter definition
    centered_x = 0
    centered_y = 0
    centered_z = 0
    width_film_x =10e-6
    width_film_y =10e-6
    base_hight= 2e-6
    height2=0.12e-6
    height1=0.1e-6

    

    
    #Start Lumerical Mode
    #mode1=lumapi.MODE(hide = True)
    mode1=lumapi.MODE() 
    
    #Material Definition in Lumerical Mode
    materials = open(dir_mat).read()   
    mode1.eval(materials)
    
    
    #Add base
    mode1.addrect(name="Si_substrate",x = centered_x, x_span=width_film_x,
    		 y = centered_x, y_span=width_film_y, z_min = centered_z, z_max= base_hight, material = "Si_Salzberg" )
    
    centered_z=base_hight;
    
    #Add down cladding
    
    mode1.addrect(name = "SiO2 Clad" ,x = centered_x, x_span=width_film_x,
    		 y = centered_x, y_span=width_film_y, z_min = centered_z, z_max= base_hight + centered_z , material = "SiO2_fusedquartz" ,alpha = 0.3)
    centered_z=centered_z + base_hight;
    
    #Add upper core
    
    mode1.addrect(name = "Si Core 1" ,x = centered_x, x_span=width_film_x,
    		 y = centered_x, y_span=width_film_y, z_min = centered_z, z_max= centered_z + height1, material = "Si_Salzberg" )
    
    mode1.addrect(name = "SiO2 Clad" ,x = centered_x, x_span=width_film_x,
    		 y = centered_x, y_span=width_film_y, z_min = centered_z + height1, z_max= height1 + centered_z + 0.5e-6, material = "SiO2_fusedquartz" ,alpha = 0.3)
    
    
    mode1.addwaveguide(name = "Si", base_angle = angle, base_height= height2, base_width=waveguide_w, material = "Si_Salzberg")
    mode1.setnamed("Si","poles",np.array([[-width_film_x/2,centered_y],
                                                 [width_film_x/2,centered_y]]))
    mode1.setnamed("Si","z",centered_z + height1 + height2/2)
    

    
    mode1.addmesh(name = "mesh_waveguide", x_min = centered_x - 0.1e-6, x_max = centered_x+ 0.1e-6,
    		y = 0 , y_span= waveguide_w+0.5e-6, z = centered_z + height1, z_span = 0.5e-6,
    		override_x_mesh = 0, override_y_mesh = 1,
    		override_z_mesh = 1, set_maximum_mesh_step = 1,
    		dy = 15e-9, dz = 15e-9)
    if rad !=0:
        #print("rad distinto de 0")
        mode1.addfde(solver_type = "2D X normal" , x = centered_x, y = 0, y_span = waveguide_w + 1e-6,
        		z = centered_z + height1 , z_span = 1e-6, z_min_bc = boundry , z_max_bc = boundry ,
        		y_min_bc = boundry, y_max_bc = boundry, min_mesh_step = 5e-9,
        		define_y_mesh_by = "maximum mesh step", dy = 50e-9,
        		define_z_mesh_by = "maximum mesh step", dz = 50e-9,
        		wavelength = wl, number_of_trial_modes = 40, search = "in range",
        		n1 = 3.2, n2 = 1.7, bent_waveguide = 1, bend_radius = rad )
        #mode1.set("wavelength")
        
    else:
        #print("rad igual de 0")
        mode1.addfde(solver_type = "2D X normal" , x = centered_x, y = 0, y_span = waveguide_w + 1e-6,
        		z = centered_z + height1,z_span = 1e-6, z_min_bc = boundry , z_max_bc = boundry ,
        		y_min_bc = boundry, y_max_bc = boundry, min_mesh_step = 5e-9,
        		define_y_mesh_by = "maximum mesh step", dy = 50e-9,
        		define_z_mesh_by = "maximum mesh step", dz = 50e-9,
        		wavelength = wl, number_of_trial_modes = 40, search = "in range",
        		n1 = 3.2, n2 = 1.7, bent_waveguide = 0)
        
    mode1.run()
    data = mode1.findmodes()
    Mode_results=[]
    te=0
    tm=0
    #Ef = []
    for i in range(0,int(data)):
        neff= np.real(mode1.getresult("mode{}".format(i + 1),"neff")[0][0])
        loss= mode1.getresult("mode{}".format(i + 1),"loss")
        polarization=mode1.getresult("mode{}".format(i + 1),"TE polarization fraction")
        ng = np.real(mode1.getresult("mode{}".format(i + 1),"ng"))[0][0]
        #Ef = Ef +[ mode1.getresult(("mode{}".format(i + 1),"E"))]
        Existance = borders_analysis(mode1.getresult("mode{}".format(i + 1),"E"))
        #print(Existance)
        if(polarization> 0.5) and Existance:    
            Mode_results = Mode_results + [["TE{}".format(te),1.55e-6,neff,loss,polarization, ng]]
            te = te +1
        elif (polarization<= 0.5) and Existance:
            Mode_results = Mode_results + [["TM{}".format(tm),1.55e-6,neff,loss,polarization, ng]]
            tm = tm+1
    input("Presiona Enter para finalizar...")
    mode1.close();
    return Mode_results



def rad_analysis(rad_min,rad_max,points, angle,boundry,width,wl):
    centered_x = 0
    centered_y = 0
    centered_z = 0
    width_film_x =10e-6
    width_film_y =10e-6
    base_hight= 2e-6
    LN_hight_sub=0.22e-6
    LN_hight_wg=0.22e-6
    
    angle_in_rad = angle/180 *np.pi
    
    lx_up = width
    lx_down =width + 2 *LN_hight_wg * np.cos(angle_in_rad) / np.sin(angle_in_rad)
    
    mode1=lumapi.MODE(hide = True)
    #mode1=lumapi.MODE() 
    
    materials = open(dir_mat).read()
        
    mode1.eval(materials)
    
    mode1.addrect(name="Si_substrate",x = centered_x, x_span=width_film_x,
    		 y = centered_x, y_span=width_film_y, z_min = centered_z, z_max= base_hight, material = "Si_Salzberg" )
    
    centered_z=base_hight;
    
    mode1.addrect(name="SiO2_cladding",x = centered_x, x_span=width_film_x,
    		 y = centered_x, y_span=width_film_y, z_min = centered_z,
    		 z_max= centered_z +base_hight + 0.5e-6, material = "SiO2_fusedquartz" )
    centered_z=centered_z +base_hight
    
    
    
    V = np.zeros((4, 2))
    

    # Asignar valores a la matriz V
    V[0, 0:2] = [0, -lx_down / 2]
    V[1, 0:2] = [LN_hight_wg / 2, -lx_up / 2]
    V[2, 0:2] = [LN_hight_wg / 2, lx_up / 2]
    V[3, 0:2] = [0, lx_down / 2]
    
    mode1.addpoly(x = 0, y =0, z = centered_z, first_axis = "y"
    		, rotation_1 =-90, z_span = width_film_y, material = "SiO2_fusedquartz" , vertices = V ,name ='Si_core')
    
    mode1.addmesh(name = "mesh_waveguide", x_min = 0 , x_max = 2e-6,
    		y = 0 , y_span= 1e-6, z = centered_z, z_span = 0.5e-6,
    		override_x_mesh = 0, override_y_mesh = 1,
    		override_z_mesh = 1, set_maximum_mesh_step = 1,
    		dy = 15e-9, dz = 15e-9)
    
    mode1.addfde(solver_type = "2D X normal" , x = centered_x, y = 0, y_span = 2.5e-6,
    		z = centered_z,z_span = 2e-6, z_min_bc = boundry , z_max_bc = boundry ,
    		y_min_bc = boundry, y_max_bc = boundry, min_mesh_step = 5e-9,
    		define_y_mesh_by = "maximum mesh step", dy = 40e-9,
    		define_z_mesh_by = "maximum mesh step", dz = 40e-9,
    		wavelength = wl, number_of_trial_modes = 50, search = "in range",
    		n1 = 3.4, n2 = 1.7, bent_waveguide = 0)
    
    mode1.run()
    data = mode1.findmodes()
    r0=[]
    for n in range(0,int(data)):
        r0 =r0+ [mode1.copydcard("mode{}".format(n+1),"test_moder{}".format(n+1))]
    


    #sheet1.title = "Plot"
    rads=np.linspace(rad_max,rad_min,points)
    neff_df=DataStructure()
    losses_df=DataStructure()
    gindex_df=DataStructure()
    out_df=DataStructure()
    shifty_df=DataStructure()
    for j in range(0,points):
    
        mode1.switchtolayout()
        
        mode1.select("FDE")
        
        mode1.set("bent waveguide" ,1)
        mode1.set("bend radius", rads[j])
        

        
        mode1.run()
        #sheet2 = workbook.create_sheet(title="radius = {}".format(rads[j]))
        data = mode1.findmodes()
        Mode_results=[]
        te=0
        tm=0
#column_names = ["PMode", "wavelength", "effective index","loss","polarization","group index","large up","large down","out","offest y"]
#?out(1);  # overlap
#?out(2);  # power coupling        
        for i in range(0,int(data)):
            out = mode1.overlap("mode{}".format(i+1),r0[i])            
            mode1.setanalysis("shift d-card center",1);           
            shift = mode1.optimizeposition(i+1,i+1);
            neff= np.real(mode1.getresult("mode{}".format(i + 1),"neff")[0][0])
            loss= mode1.getresult("mode{}".format(i + 1),"loss")
            polarization=mode1.getresult("mode{}".format(i + 1),"TE polarization fraction")
            ng = np.real(mode1.getresult("mode{}".format(i + 1),"ng"))[0][0]
            name=""
            print(out)
            print(shift)
            if(polarization> 0.5):    
                Mode_results = Mode_results + [["TE{}".format(te),wl,neff,loss,polarization, ng, lx_up,lx_down,float(out[0]),float(shift[1])]]
                te = te +1
                name="TE{}".format(te)
            else:
                Mode_results = Mode_results + [["TM{}".format(tm),wl,neff,loss,polarization, ng, lx_up,lx_down,float(out[0]),float(shift[1])]]
                tm = tm+1
                name="TM{}".format(tm)
            neff_df.add(name, r0[j], neff)
            losses_df.add(name,r0[j],loss)
            gindex_df.add(name,r0[j],ng)
            out_df.add(name,r0[j],float(out[0]))
            shifty_df.add(name,r0[j],float(shift[1]))
    #x=Mode_results
    neff_df.to_excel('Rad{}.xlsx'.format(str(int(wl*1e9))),'Effective Index')
    losses_df.to_excel('Rad{}.xlsx'.format(str(int(wl*1e9))),'Losses')
    gindex_df.to_excel('Rad{}.xlsx'.format(str(int(wl*1e9))),'Group Index')
    out_df.to_excel('Rad{}.xlsx'.format(str(int(wl*1e9))),'Out')
    shifty_df.to_excel('Rad{}.xlsx'.format(str(int(wl*1e9))),'Shift y')

    #print("La matriz se ha escrito en la hoja 2 del archivo 'matriz.xlsx'.")
    return 0
        

#testing area if you want to test it ake out the # comment in line 121, comment line 39 and take out the comment of line 40
mode_analysis(0.4e-6, 90,"Metal",0,1.55e-6)
