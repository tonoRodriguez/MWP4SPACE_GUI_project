# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 11:01:04 2025

@author: Antonio
"""

direction = "C:\Program Files (x86)\CST Studio Suite 2024\AMD64\python_cst_libraries\cst\__init__.py"

import sys

sys.path.append(r"C:\Program Files (x86)\CST Studio Suite 2024\AMD64\python_cst_libraries")
import cst


import cst.interface  # Importar la interfaz de CST
import cst.results    # Para extraer resultados
import os

# Conectar con CST
cst_project = cst.interface.DesignEnvironment().new_mws()

print(type(cst_project))

# Parámetros de la CPW
substrate_thickness = 0.635  # Espesor del sustrato (mm)
substrate_epsilon_r = 9.8    # Permitividad relativa
ground_plane_thickness = 0.035  # Espesor del cobre (mm)
signal_width = 1.5  # Ancho de la línea central (mm)
gap_width = 0.3     # Separación entre línea y plano de tierra (mm)
length = 20         # Longitud de la línea (mm)
width = 10          # Ancho total (mm)

# Crear el sustrato
cst_project.parameter("substrate_thickness", substrate_thickness)
cst_project.parameter("substrate_epsilon_r", substrate_epsilon_r)
cst_project.parameter("ground_plane_thickness", ground_plane_thickness)


s = cst_project.modeler
s.solid_name("Substrate")
s.create_brick(xmin=0, xmax=width, ymin=0, ymax=length, zmin=0, zmax=-substrate_thickness, material="Rogers RT/Duroid 6006")

# Crear el conductor central
s.solid_name("SignalLine")
s.create_brick(xmin=(width/2 - signal_width/2), xmax=(width/2 + signal_width/2), 
               ymin=0, ymax=length, zmin=0, zmax=ground_plane_thickness, material="Copper (annealed)")

# Crear los planos de tierra
s.solid_name("GroundPlaneLeft")
s.create_brick(xmin=0, xmax=(width/2 - signal_width/2 - gap_width),
               ymin=0, ymax=length, zmin=0, zmax=ground_plane_thickness, material="Copper (annealed)")

s.solid_name("GroundPlaneRight")
s.create_brick(xmin=(width/2 + signal_width/2 + gap_width), xmax=width,
               ymin=0, ymax=length, zmin=0, zmax=ground_plane_thickness, material="Copper (annealed)")

# Configurar la simulación
solver = cst_project.solver
solver.frequency_range(1, 40)  # Rango de frecuencias de 1 GHz a 40 GHz
solver.set_solver_type("HF Time Domain")  # Usar el solver de dominio del tiempo

# Guardar el proyecto
project_path = os.path.join(os.getcwd(), "coplanar_waveguide.cst")
cst_project.save_as(project_path, overwrite=True)

print(f"Proyecto guardado en: {project_path}")