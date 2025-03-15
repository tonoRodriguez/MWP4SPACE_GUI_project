# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 15:18:28 2025

@author: Antonio
"""
from docx import Document
from docx.shared import Inches
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
#import imp

sys.path.append("C:/Program Files/Lumerical/v241/api/python/")
sys.path.append(os.path.dirname(__file__))
#lumapi = imp.load_source("lumapi","C:/Program Files/Lumerical/v241/api/python/lumapi.py")
#os.add_dll_directory("C:/Program Files/Lumerical/v241/api/python")

dir_mat="Material_script/LNOI_materials.lsf"
import lumapi

angle = 90
height2=0.12e-6
height1=0.1e-6
width1=0.55e-6
width2=0.65e-6
#m=0.55191502449
centered_z=0
#radius=50e-6
Lc =0
Period= 8.034e-6
x_span=4*Period
gap = 0.25e-6

base_hight= 2e-6


wl =1.55e-6
#gap = 0.1e-6
width_film_x = x_span
width_film_y = width1 + width2 + 5e-6
boundry = "PML"
centered_x = 0
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
		 z_max= centered_z +base_hight, material = "SiO2_fusedquartz" )
centered_z=centered_z +base_hight

mode1.addrect(name="Si_core1",x = centered_x, x_span=width_film_x,
		 y = centered_y, y_span=width_film_y, z_min = centered_z,
		 z_max= centered_z+ height1, material = "Si_Salzberg"  )
centered_z=centered_z+height1 

mode1.addrect(name="SiO2_cladding2",x = centered_x, x_span=width_film_x,
		 y = centered_y, y_span=width_film_y, z_min = centered_z,
		 z_max= centered_z +base_hight*0.25, material = "SiO2_fusedquartz" , alpha = 0.5 )


#Input and output waveguides


mode1.addwaveguide(name = "Input", base_angle = angle, base_height= height2, base_width=width1, material = "Si_Salzberg")


mode1.setnamed("Input","poles",np.array([[-2*Period , centered_y  ],
                                         [-Period , centered_y  ]]))
mode1.setnamed("Input","z",centered_z + height2*0.5)

mode1.addwaveguide(name = "Output", base_angle = angle, base_height= height2, base_width=width1, material = "Si_Salzberg")
#mode1.addwaveguide(name = "outer_bottom", base_angle = angle, base_height= height2, base_width=width, material = "LN_SE" )

mode1.setnamed("Output","poles",np.array([[Period , centered_y   ],
                                         [2*Period , centered_y   ]]))
mode1.setnamed("Output","z",centered_z + height2*0.5)


#Grattings a ver

mode1.addwaveguide(name = "waveguide1", base_angle = angle, base_height= height2, base_width=width1, material = "Si_Salzberg")
#mode1.addwaveguide(name = "outer_bottom", base_angle = angle, base_height= height2, base_width=width, material = "LN_SE" )

mode1.setnamed("waveguide1","poles",np.array([[-Period , centered_y  ],
                                         [0 , centered_y  ]]))
mode1.setnamed("waveguide1","z",centered_z + height2*0.5)

mode1.addwaveguide(name = "waveguide2", base_angle = angle, base_height= height2, base_width=width2, material = "Si_Salzberg")
#mode1.addwaveguide(name = "outer_bottom", base_angle = angle, base_height= height2, base_width=width, material = "LN_SE" )

mode1.setnamed("waveguide2","poles",np.array([[0 , centered_y   ],
                                         [Period , centered_y   ]]))
mode1.setnamed("waveguide2","z",centered_z + height2*0.5)


mode1.addmesh(name = "mesh_waveguide", x_min =-Period/2 , x_max = Period/2,
  		y = centered_y , y_span= width2, z = centered_z + height1/2, z_span = (height1 + height2),
  		override_x_mesh = 0, override_y_mesh = 1,
  		override_z_mesh = 1, set_maximum_mesh_step = 1,
  		dy = 15e-9, dz = 15e-9)

mode1.addeme(x_min = -2*Period, y = centered_y, y_span= width_film_y,z=centered_z, z_span= 0.5e-6, wavelength = wl)
mode1.set("number of cell groups",4)
mode1.set("group spans",np.array([[Period], [Period], [Period],[Period]]))
mode1.set("cells",np.array([[1],[ 1],[1],[ 1]]))
mode1.set("subcell method",np.array([[0],[ 0], [0],[0]]))
mode1.set("start cell group",2)
mode1.set("end cell group",3)
mode1.set("periods",100)

# set up ports: port 1
mode1.select("EME::Ports::port_1")
mode1.set("use full simulation span",1)
mode1.set("y",0)
mode1.set("y span",width1)
mode1.set("z",0)
mode1.set("z span",0.4e-6)
mode1.set("mode selection","fundamental mode")
# set up ports: port 2
mode1.select("EME::Ports::port_2")
mode1.set("use full simulation span",1)
mode1.set("y",0)
mode1.set("y span",width1)
mode1.set("z",0)
mode1.set("z span",0.4e-6)
mode1.set("mode selection","fundamental mode")

mode1.setactivesolver("EME")
mode1.addemeprofile(x_min = -2*Period, x_max= 2*Period, y = centered_y, y_span = width_film_y, z =centered_z )

mode1.run()


mode1.setemeanalysis("wavelength sweep",1);
mode1.setemeanalysis("start wavelength", wl -0.05e-6);
mode1.setemeanalysis("stop wavelength",wl  + 0.05e-6);
mode1.setemeanalysis("number of wavelength points", 200);
mode1.emesweep("wavelength sweep");

S_param=mode1.getemesweep("S_wavelength_sweep")

angle=np.angle(S_param["s21"])
magnitude = np.abs(S_param["s21"])

# Convertir la fase a grados para mejor interpretación
# Aplicar phase unwrapping para corregir saltos de 2pi
#angle_unwrapped = np.unwrap(angle)

# Convertir la fase a grados
angle_deg = np.degrees(angle)
wL_sp = S_param["wavelength"]

# Gráfico de fase
plt.figure(figsize=(8,4))
plt.plot(wL_sp, angle_deg ,  color='blue', label="Fase (°)")
plt.xlabel("Longitud de onda (nm)")
plt.ylabel("Fase (grados)")
plt.title("Fase vs Longitud de onda")
plt.legend()
plt.grid()
plt.show()

# Gráfico de magnitud
plt.figure(figsize=(8,4))
plt.plot(wL_sp, magnitude, color='red', label="Magnitud |S21|")
plt.xlabel("Longitud de onda (nm)")
plt.ylabel("Magnitud")
plt.title("Magnitud vs Longitud de onda")
plt.legend()
plt.grid()
plt.show()






