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

dir_mat="Material_script/LNOI_materials.lsf"

import lumapi

#define relevant paths
current_dir = os.getcwd()
process_file_path = os.path.join(current_dir, "example_process_file.lbr")
gds_file_path = os.path.join(current_dir, "straight_wg.gds")

#create gds
wg = df.shallow.euler(angle=90).put()
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
FDTD.loadprocessfile(process_file_path)
FDTD.select("layer group")
FDTD.loadgdsfile(gds_file_path)
