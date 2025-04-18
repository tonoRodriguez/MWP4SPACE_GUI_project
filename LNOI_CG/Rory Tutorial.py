# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 16:00:00 2025

@author: Antonio
"""
import numpy as np
#import matplotlib.pyplot as plt
import os
import sys
#import imp
import nazca as nd
from nazca import demofab as df

sys.path.append("C:/Program Files/Lumerical/v241/api/python/")
sys.path.append(os.path.dirname(__file__))

dir_mat="Material_script/LNOI_materials.lsf"

import lumapi

#define relevant paths
current_dir = os.getcwd()
process_file_path = os.path.join(current_dir, "example_process_file.lbr")
gds_file_path = os.path.join(current_dir, "straight_wg.gds")

#create gds
l= 4
wg = df.shallow.strt(width = 0.7,length = l).put()
nd.export_gds(filename = "straight_wg")

n_ordinary = 2.2111
n_extraordinary = 2.13755
n_matrix = np.array([n_ordinary,n_extraordinary,n_ordinary])
#generate simulation from gds
FDTD =lumapi.FDTD()
mymaterial =FDTD.addmaterial("(n,k) Material");
FDTD.setmaterial(mymaterial,"name","LN_anisotropic");
FDTD.setmaterial("LN_anisotropic", "Anisotropy", 1); # enable diagonal anisotropy
FDTD.setmaterial("LN_anisotropic","Refractive Index",n_matrix)
FDTD.addlayerbuilder()
FDTD.select("layer group")
#FDTD.set("x span" , 500e-6)
#FDTD.set("y span" , 500e-6)
FDTD.select("layer group")
FDTD.loadprocessfile(process_file_path)
FDTD.select("layer group")
FDTD.loadgdsfile(gds_file_path)

FDTD.addfdtd(x = l/2*1e-6, x_span = (l-1) *1e-6 , y= 0 , y_span = 5e-6 , z = 0.3e-6 , z_span = 3e-6,
             set_simulation_bandwidth = 1 , simulation_wavelength_min = 1.5e-6 , simulation_wavelength_max = 1.6e-6)
FDTD.addport()
# FDTD.addplane()
# FDTD.set("injection axis","x-axis")

FDTD.set("x", 1.5e-6)
FDTD.set( "y", 0)
FDTD.set("y span" , 0.8e-6 + 4e-6)
FDTD.set( "z", 0.3e-6)
FDTD.set("z span" , 2e-6)
FDTD.set("number of field profile samples", 3)


FDTD.addport()
FDTD.set("direction","Backward")
FDTD.set("x", (l-1.5)*1e-6)
FDTD.set( "y", 0)
FDTD.set("y span" , 0.8e-6 + 4e-6)
FDTD.set( "z", 0.3e-6)
FDTD.set("z span" , 2e-6)
FDTD.set("number of field profile samples", 3)

FDTD.addprofile(x = l/2*1e-6  , x_span = (l-2)*1e-6 , y = 0,y_span = 5e-6 , z =  0.3e-6 )
FDTD.addmesh(x = l/2*1e-6  , x_span = (l-2)*1e-6, y = 0,y_span = 1e-6 , z =  0.315e-6 , z_span = 0.6e-6)

