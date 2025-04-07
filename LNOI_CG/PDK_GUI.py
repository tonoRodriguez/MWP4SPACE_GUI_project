# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:50:35 2024

@author: Antonio
"""
import tkinter as tk
import pandas as pd
from tkinter import ttk
from Mode_analysis import mode_analysis, rad_analysis, File_creator
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import numpy as np
from Data_Structure import DataStructure




# Función que se llama cuando se hace clic en el botón
#hacerlo con una matriz!!!!!
def mode_function(width_max, width_min, points, angle, material,wl , eff_inx):
    #print(width_min, width_max, points, angle, material)
    widths=np.linspace(width_max,width_min,points)
    delta_w=5e-9
    wavelengths=np.linspace(wl-delta_w,wl + delta_w,7)
    
    neff_df=DataStructure()
    losses_df=DataStructure()
    gindex_df=DataStructure()
    array_eff_index=DataStructure()
    for n in wavelengths:
        for i in range(0,points):
            x =mode_analysis(widths[i],angle, material,0,n,eff_inx)
            #print(x)
            if n == wl and x:
                print("Entro =wl")
                for j in range(0,len(x)):
                    neff_df.add(x[j][0], widths[i], x[j][2])
                    losses_df.add(x[j][0],widths[i],x[j][3])
                    gindex_df.add(x[j][0],widths[i],x[j][5])
                    array_eff_index.add_with_wavelength(x[j][0],widths[i],n,x[j][5])
                    #print(neff_df)
                    array_eff_index.add_with_wavelength(x[j][0],widths[i],n,x[j][5])
                    #print(array_eff_index)
            elif x:
                print("Entro !=wl")            
                for j in range(0,len(x)):
                    array_eff_index.add_with_wavelength(x[j][0],widths[i],n,x[j][5])
            else:
                print("no entra")

        
    array_eff_index.to_excel_with_wavelength('Mode_{}.xlsx'.format(str(int(wl*1e9)) + "nm"),'Effective Indexes for analysis')
    neff_df.to_excel('Mode_{}.xlsx'.format(str(int(wl*1e9)) + "nm"),'Effective Index')
    losses_df.to_excel('Mode_{}.xlsx'.format(str(int(wl*1e9)) + "nm"),'Losses')
    gindex_df.to_excel('Mode_{}.xlsx'.format(str(int(wl*1e9)) + "nm"),'Group Index')

    print("La matriz se ha escrito en la hoja 2 del archivo 'matriz.xlsx'.")
#     print(x)
#     print(f"Width: {width}, Angle: {angle}, Material: {material}")
    return 0


root = tk.Tk()
root.title("PDK LNOI fabrication")

# Crear y colocar la entrada para el ancho
tk.Label(root, text = "Mode analysis",font=("Helvetica", 10, "bold")).grid(row=0, column=0)
tk.Label(root, text="Min Width um:").grid(row=1, column=0)
width_entry_min = tk.Entry(root)
width_entry_min.grid(row=1, column=1)


# Crear y colocar la entrada para el ancho
tk.Label(root, text="Max Width um:").grid(row=1, column=2)
width_entry_max = tk.Entry(root)
width_entry_max.grid(row=1, column=3)
# Crear y colocar la entrada para el ángulo
tk.Label(root, text="Angle:").grid(row=2, column=0)
angle_entry = tk.Entry(root)
angle_entry.grid(row=2, column=1)


# Crear y colocar la entrada para espaciado
tk.Label(root, text="number of points:").grid(row=3, column=0)
points_entry = tk.Entry(root)
points_entry.grid(row=3, column=1)
# Crear y colocar el menú desplegable para el material
tk.Label(root, text="Material:").grid(row=4, column=0)
material_var = tk.StringVar()
material_dropdown = ttk.Combobox(root, textvariable=material_var)
material_dropdown['values'] = ("Metal", "PML", "Material 3")
material_dropdown.grid(row=4, column=1)

#wavelength
tk.Label(root, text="Wavelength um:").grid(row=5, column=0)
wl_entry = tk.Entry(root)
wl_entry.grid(row=5, column=1)
# Crear y colocar el botón

# Agregar Checkbutton con etiqueta "L opt"
Ex_direc = tk.IntVar()  # Variable para almacenar el estado (0 o 1)
Ex_direc_md = tk.Checkbutton(root, text="Use extraordinary effective Index", variable=Ex_direc)
Ex_direc_md.grid(row=6, column=0, columnspan=1)

def on_button_click():
    width_min = float(width_entry_min.get()) * 1e-6    
    width_max = float(width_entry_max.get()) * 1e-6
    space= int(points_entry.get())
    angle = float(angle_entry.get())
    wl_opt_state = Ex_direc.get()  # Obtener el estado del checkbutton (0 o 1)
    material = material_var.get()
    wl = float(wl_entry.get())*1e-6
    eff_inx = "LN_SE"
    if wl_opt_state == 1:
        eff_inx = "LN_SE_extraordinary"

    mode_function(width_min, width_max, space, angle, material,wl,eff_inx)

button = tk.Button(root, text="Submit", command=on_button_click)
button.grid(row=7, columnspan=2)


tk.Label(root, text = "Bend analysis",font=("Helvetica", 10, "bold")).grid(row=8, column=0)

tk.Label(root, text="Min Rad um:").grid(row=9, column=0)
rad_entry_min = tk.Entry(root)
rad_entry_min.grid(row=9, column=1)


# Crear y colocar la entrada para el ancho
tk.Label(root, text="Max Rad um:").grid(row=9, column=2)
rad_entry_max = tk.Entry(root)
rad_entry_max.grid(row=9, column=3)
# Crear y colocar la entrada para el ángulo

# Crear y colocar la entrada para el ángulo
tk.Label(root, text="Angle:").grid(row=10, column=0)
angle_entry_rad = tk.Entry(root)
angle_entry_rad.grid(row=10, column=1)


# Crear y colocar la entrada para espaciado
tk.Label(root, text="number of points:").grid(row=11, column=0)
points_entry_rad = tk.Entry(root)
points_entry_rad.grid(row=11, column=1)
# Crear y colocar la entrada para espaciado
tk.Label(root, text="width um:").grid(row=12, column=0)
width_r = tk.Entry(root)
width_r.grid(row=12, column=1)
# Crear y colocar el menú desplegable para el material# Crear y colocar el menú desplegable para el material
tk.Label(root, text="Material:").grid(row=13, column=0)
material_var_rad = tk.StringVar()
material_dropdown_rad = ttk.Combobox(root, textvariable=material_var_rad)
material_dropdown_rad['values'] = ("Metal", "PML", "Material 3")
material_dropdown_rad.grid(row=13, column=1)

#wavelength
tk.Label(root, text="Wavelength:").grid(row=14, column=0)
wlb_entry = tk.Entry(root)
wlb_entry.grid(row=14, column=1)
# Crear y colocar el botón

# Agregar Checkbutton con etiqueta "L opt"
Word_var = tk.IntVar()  # Variable para almacenar el estado (0 o 1)
Word_check = tk.Checkbutton(root, text="Make Word Doc", variable=Word_var)
Word_check.grid(row=15, column=0, columnspan=1)

def on_button_click_rad():
    rad_min = float(rad_entry_min.get()) * 1e-6    
    rad_max = float(rad_entry_max.get()) * 1e-6
    space= int(points_entry_rad.get())
    angle = float(angle_entry_rad.get())
    material = material_var_rad.get()
    width = float(width_r.get()) *1e-6
    wl= float(wlb_entry.get())*1e-6

    s=rad_analysis(rad_min, rad_max, space, angle, material,width,wl)
    return s

button_rad = tk.Button(root, text="Submit Rad", command=on_button_click_rad)
button_rad.grid(row=16, columnspan=2)



tk.Label(root, text = "Component to interconnect",font=("Helvetica", 10, "bold")).grid(row=17, column=0)

# Crear y colocar la entrada para espaciado
tk.Label(root, text="width um:").grid(row=18, column=0)
width_f = tk.Entry(root)
width_f.grid(row=18, column=1)

# Crear y colocar la entrada para el ángulo
tk.Label(root, text="Angle:").grid(row=19, column=0)
angle_entry_f = tk.Entry(root)
angle_entry_f.grid(row=19, column=1)

tk.Label(root, text="Rad um:").grid(row=20, column=0)
rad_entry_f = tk.Entry(root)
rad_entry_f.grid(row=20, column=1)

#wavelength
tk.Label(root, text="Wavelength (min wl) [um] (100 nm spam):").grid(row=21, column=0)
wlf_entry = tk.Entry(root)
wlf_entry.grid(row=21, column=1)
# Crear y colocar el botón

def on_button_click_S():
    
    rad = float(rad_entry_f.get()) * 1e-6    
    angle = float(angle_entry_f.get())
    waveguide_w = float(width_f.get()) *1e-6
    wl= float(wlf_entry.get())*1e-6
    File_creator(angle, waveguide_w,wl,rad)

    return 0

button_S = tk.Button(root, text="Create LMS file", command=on_button_click_S)
button_S.grid(row=22, columnspan=2)

root.mainloop()
