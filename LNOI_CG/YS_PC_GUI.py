# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 22:46:26 2025

@author: Antonio
"""

import tkinter as tk
import pandas as pd
from Y_spl_Power_Coupler import y_splitter, PowerCoupler
root = tk.Tk()
root.title("Y splitter and Power coupler")

# Crear y colocar la entrada para el ancho
tk.Label(root, text = "y splitter").grid(row=0, column=0)


tk.Label(root, text="base angle").grid(row=1, column=0)
angle_entry = tk.Entry(root)
angle_entry.grid(row=1, column=1)


tk.Label(root, text="base width um").grid(row=2, column=0)
base_width_entry = tk.Entry(root)
base_width_entry.grid(row=2, column=1)


tk.Label(root, text="y span um").grid(row=3, column=0)
y_span_entry = tk.Entry(root)
y_span_entry.grid(row=3, column=1)

tk.Label(root, text="Lw um").grid(row=4, column=0)
Lw_entry = tk.Entry(root)
Lw_entry.grid(row=4, column=1)

tk.Label(root, text="Ls um").grid(row=5, column=0)
Ls_entry = tk.Entry(root)
Ls_entry.grid(row=5, column=1)

def on_button_click():
    angle = float(angle_entry.get())  
    base_width= float(base_width_entry.get()) *1e-6
    y_span= int(y_span_entry.get()) * 1e-6
    Lw = float(Lw_entry.get()) * 1e-6
    Ls = float(Ls_entry.get())*1e-6

    y_splitter(angle, base_width, y_span, Lw, Ls)
    

button = tk.Button(root, text="Submit", command=on_button_click)
button.grid(row=6, columnspan=2)

# Crear y colocar la entrada para el ancho
tk.Label(root, text = "Power Coupler").grid(row=7, column=0)
tk.Label(root, text="Gap um").grid(row=8, column=0)
gap_entry = tk.Entry(root)
gap_entry.grid(row=8, column=1)

tk.Label(root, text="Lc um").grid(row=9, column=0)
Lc_entry = tk.Entry(root)
Lc_entry.grid(row=9, column=1)

def on_buttonPC_click():
    angle = float(angle_entry.get())  
    base_width= float(base_width_entry.get()) *1e-6
    y_span= int(y_span_entry.get()) * 1e-6
    Lw = float(Lw_entry.get()) * 1e-6
    Ls = float(Ls_entry.get())*1e-6
    gap = float(gap_entry.get())*1e-6
    Lc = float(Lc_entry.get())*1e-6

    PowerCoupler(angle, base_width, y_span, Lw, Ls,gap, Lc)

button = tk.Button(root, text="Submit PC", command=on_buttonPC_click)
button.grid(row=10, columnspan=2)

root.mainloop()