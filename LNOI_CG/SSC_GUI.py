# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 13:15:36 2024

@author: Antonio
"""

import tkinter as tk
import pandas as pd
from tkinter import ttk
from SSC_Analysis import SSC_sim,mmi_sim
import pandas as pd

root = tk.Tk()
root.title("SSC analysis")

# Crear y colocar la entrada para el ancho
tk.Label(root, text = "SSC design",font=("Helvetica", 10, "bold")).grid(row=0, column=0)
tk.Label(root, text="Min Width um:").grid(row=1, column=0)
width_entry_min = tk.Entry(root)
width_entry_min.grid(row=1, column=1)

# Crear y colocar la entrada para el ancho
tk.Label(root, text="Max Width um:").grid(row=2, column=0)
width_entry_max = tk.Entry(root)
width_entry_max.grid(row=2, column=1)
# Crear y colocar la entrada para el ángulo
tk.Label(root, text="Angle:").grid(row=3, column=0)
angle_entry = tk.Entry(root)
angle_entry.grid(row=3, column=1)

# Crear y colocar la entrada para espaciado
tk.Label(root, text="number of points in the SSC:").grid(row=4, column=0)
points_entry = tk.Entry(root)
points_entry.grid(row=4, column=1)

# Crear y colocar la entrada para espaciado
tk.Label(root, text="Length of the SSC um:").grid(row=5, column=0)
Length_entry = tk.Entry(root)
Length_entry.grid(row=5, column=1)

# Crear y colocar la entrada para longitud de ond
tk.Label(root, text="Wavelength um:").grid(row=6, column=0)
wl_entry = tk.Entry(root)
wl_entry.grid(row=6, column=1)

# Agregar Checkbutton con etiqueta "L opt"
l_opt_var = tk.IntVar()  # Variable para almacenar el estado (0 o 1)
l_opt_check = tk.Checkbutton(root, text="L opt", variable=l_opt_var)
l_opt_check.grid(row=7, column=0, columnspan=1)

# Crear y colocar la entrada para espaciado

# Variable con valor inicial 0 (numérico)
length_span_var = tk.DoubleVar(value=0)  
tk.Label(root, text="Length span um:").grid(row=8, column=0)
Length_span_entry = tk.Entry(root, textvariable=length_span_var)
Length_span_entry.grid(row=8, column=1)

# Agregar Checkbutton con etiqueta "L opt"
wl_opt_var = tk.IntVar()  # Variable para almacenar el estado (0 o 1)
wl_opt_check = tk.Checkbutton(root, text="S_param", variable=wl_opt_var)
wl_opt_check.grid(row=9, column=0, columnspan=1)

# Crear y colocar la entrada para espaciado

# Variable con valor inicial 0 (numérico)
wl_span_var = tk.DoubleVar(value=0)  
tk.Label(root, text="wavelength span um:").grid(row=10, column=0)
wl_span_entry = tk.Entry(root, textvariable=wl_span_var)
wl_span_entry.grid(row=10, column=1)

# Agregar Checkbutton con etiqueta "L opt"
effIn_var = tk.IntVar()  # Variable para almacenar el estado (0 o 1)
effIn_check = tk.Checkbutton(root, text="Extraordinary direction", variable=effIn_var)
effIn_check.grid(row=11, column=0, columnspan=1)

def on_button_click():
    width_min = float(width_entry_min.get()) * 1e-6    
    width_max = float(width_entry_max.get()) * 1e-6
    space= int(points_entry.get())
    angle = float(angle_entry.get())
    x_length = float(Length_entry.get()) * 1e-6
    l_opt_state = l_opt_var.get()  # Obtener el estado del checkbutton (0 o 1)
    length_span = float(Length_span_entry.get()) * 1e-6
    wl_opt_state = wl_opt_var.get()  # Obtener el estado del checkbutton (0 o 1)
    wl_span = float(wl_span_entry.get()) * 1e-6
    wl = float(wl_entry.get()) *1e-6
    eff_inx = "LN_SE"
    Ex_state = effIn_var.get()  # Obtener el estado del checkbutton (0 o 1)
    if Ex_state == 1:
        eff_inx = "LN_SE_extraordinary"
    #print(width_min ,width_max,space, angle, x_length,l_opt_state,length_span)
    SSC_sim(x_length,angle,width_max,width_min,space,wl, # basic tapper simulation
            l_opt_state,length_span, # length optimization
            wl_opt_state, wl_span,
            eff_inx)

button_SSC = tk.Button(root, text="Submit", command=on_button_click)
button_SSC.grid(row=12, columnspan=2)

tk.Label(root, text = "MMi analysis",font=("Helvetica", 10, "bold")).grid(row=13, column=0)
# ancho y largo

tk.Label(root, text="MMi width um:").grid(row=14, column=0)
MMi_width_entry = tk.Entry(root)
MMi_width_entry.grid(row=14, column=1)


# Crear y colocar la entrada para el ancho
tk.Label(root, text="MMi length um:").grid(row=15, column=0)
MMi_length_entry = tk.Entry(root)
MMi_length_entry.grid(row=15, column=1)

# Crear y colocar la entrada para el ancho
tk.Label(root, text="Distance between ports um:").grid(row=16, column=0)
MMi_distance = tk.Entry(root)
MMi_distance.grid(row=16, column=1)

def on_button_clic_MMi():
    width_min = float(width_entry_min.get()) * 1e-6    
    width_max = float(width_entry_max.get()) * 1e-6
    space= int(points_entry.get())
    angle = float(angle_entry.get())
    x_length = float(Length_entry.get()) * 1e-6
    MMi_width= float(MMi_width_entry.get())*1e-6
    MMi_length=float(MMi_length_entry.get())*1e-6
    distance=float(MMi_distance.get())*1e-6
    l_opt_state = l_opt_var.get()  # Obtener el estado del checkbutton (0 o 1)
    length_span = float(Length_span_entry.get()) * 1e-6
    wl_opt_state = wl_opt_var.get()  # Obtener el estado del checkbutton (0 o 1)
    wl_span = float(wl_span_entry.get()) * 1e-6
    wl = float(wl_entry.get()) *1e-6
    #print(width_min ,width_max,space, angle, x_length)
    eff_inx = "LN_SE"
    Ex_state = effIn_var.get()  # Obtener el estado del checkbutton (0 o 1)
    if Ex_state == 1:
        eff_inx = "LN_SE_extraordinary"
    #print(width_min ,width_max,space, angle, x_length,l_opt_state,length_span)
    mmi_sim(x_length,angle,width_max,width_min,space,MMi_width,MMi_length,distance,wl, # basic MMI simulation
                l_opt_state,length_span, # length optimization
                wl_opt_state, wl_span,  #wavelength s parameters
                eff_inx
            )


button = tk.Button(root, text="Submit", command=on_button_clic_MMi)
button.grid(row=17, columnspan=2)
root.mainloop()


