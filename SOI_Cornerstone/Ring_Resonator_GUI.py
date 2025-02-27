# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 10:35:34 2025

@author: Antonio
"""

import tkinter as tk
from ring_resonator import Ring_Resonator
from tkinter import ttk



root = tk.Tk()
root.title("PDK LNOI fabrication")

# Crear y colocar la entrada para el ancho
tk.Label(root, text = "Ring Resonator").grid(row=0, column=0)
tk.Label(root, text="Width um:").grid(row=1, column=0)
width_entry = tk.Entry(root)
width_entry.grid(row=1, column=1)

# Crear y colocar la entrada para el ángulo
tk.Label(root, text="Angle:").grid(row=2, column=0)
angle_entry = tk.Entry(root)
angle_entry.grid(row=2, column=1)

# Crear y colocar el gap
tk.Label(root, text="Gap um:").grid(row=3, column=0)
Gap_entry = tk.Entry(root)
Gap_entry.grid(row=3, column=1)

# Crear y colocar el gap
tk.Label(root, text="Radius um:").grid(row=4, column=0)
radius_entry = tk.Entry(root)
radius_entry.grid(row=4, column=1)

tk.Label(root, text="x span um:").grid(row=5, column=0)
x_span_entry = tk.Entry(root)
x_span_entry.grid(row=5, column=1)

# Crear y colocar el menú desplegable para el material
tk.Label(root, text="Branches:").grid(row=6, column=0)
branch_var = tk.StringVar()
branch_dropdown = ttk.Combobox(root, textvariable=branch_var)
branch_dropdown['values'] = ("One branch", "Two branches")
branch_dropdown.grid(row=6, column=1)

#Waveguide analysis and Word Documentation

# Agregar Checkbutton con etiqueta "L opt"
wl_opt_var = tk.IntVar()  # Variable para almacenar el estado (0 o 1)
wl_opt_check = tk.Checkbutton(root, text="S_param", variable=wl_opt_var)
wl_opt_check.grid(row=7, column=0, columnspan=1)

# Agregar Checkbutton con etiqueta "L opt"
wg_var = tk.IntVar()  # Variable para almacenar el estado (0 o 1)
wg_check = tk.Checkbutton(root, text="Coupling analysis", variable=wg_var)
wg_check.grid(row=8, column=0, columnspan=1)

# Agregar Checkbutton con etiqueta "L opt"
word_var = tk.IntVar()  # Variable para almacenar el estado (0 o 1)
word_check = tk.Checkbutton(root, text="Word document", variable=word_var)
word_check.grid(row=9, column=0, columnspan=1)


def on_button_click_rad():
    width = float(width_entry.get()) * 1e-6    
    angle = float(angle_entry.get())
    Gap = float(Gap_entry.get()) *1e-6
    Radius= float(radius_entry.get())*1e-6
    x_span= float(x_span_entry.get())*1e-6
    branch = branch_dropdown.get()
    
    wl_opt_state = wl_opt_var.get()  # Obtener el estado del checkbutton (0 o 1)
    wg_check_state = wg_var.get()  # Obtener el estado del checkbutton (0 o 1)
    word_state = word_var.get()  # Obtener el estado del checkbutton (0 o 1)
    
    if branch == "One branch":
        b=1
    else:
        b=2
    Ring_Resonator(angle, width, Gap, Radius,x_span,b,
                   wl_opt_state)
    return 0

button_rad = tk.Button(root, text="Submit Rad", command=on_button_click_rad)
button_rad.grid(row=10, columnspan=2)

root.mainloop()
