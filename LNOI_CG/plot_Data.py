# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 04:06:59 2024

@author: Antonio
"""

import pandas as pd
import matplotlib.pyplot as plt
from Data_Structure import DataStructure
import numpy as np

def plot_excel_sheet(filename, sheet_name):
    # Leer los datos de la hoja de Excel seleccionada
    df = pd.read_excel(filename, sheet_name=sheet_name, engine='openpyxl')

    # Crear el gráfico
    plt.figure(figsize=(10, 6))
    
    # Iterar sobre las columnas (excepto la primera que es el índice)
    for column in df.columns[1:]:
        plt.plot(df[df.columns[0]], df[column], marker='o', label=column)
    
    # Configurar el gráfico
    plt.title(f'Gráfico de Datos - {sheet_name}')
    plt.xlabel('Radio')
    plt.ylabel('Valor')
    plt.legend()
    plt.grid(True)
    
    # Mostrar el gráfico
    plt.show()
# def plot_from_excel(file_name, sheet_name):
#     """
#     Lee un archivo Excel y genera gráficos de longitud de onda vs. valor para cada combinación de radio y nombre.

#     Args:
#         file_name (str): El nombre del archivo Excel.
#         sheet_name (str): El nombre de la hoja a leer.
#     """
#     # Leer la hoja específica del archivo Excel
#     try:
#         df = pd.read_excel(file_name, sheet_name=sheet_name)
#     except FileNotFoundError:
#         print(f"El archivo {file_name} no fue encontrado.")
#         return
#     except ValueError:
#         print(f"La hoja {sheet_name} no existe en el archivo {file_name}.")
#         return

#     # Verificar que las columnas requeridas existan
#     if not {'Nombre', 'Radio'}.issubset(df.columns):
#         print("El archivo Excel no tiene las columnas 'Nombre' y 'Radio'.")
#         return

#     # Extraer las columnas de longitudes de onda
#     wavelength_columns = [col for col in df.columns if col.startswith('Wavelength')]

#     if not wavelength_columns:
#         print("No se encontraron columnas de longitud de onda en el archivo Excel.")
#         return

#     # Crear gráficos para cada combinación de Nombre y Radio
#     for _, row in df.iterrows():
#         nombre = row['Nombre']
#         radio = row['Radio']

#         # Extraer las longitudes de onda y los valores correspondientes
#         wavelengths = [int(col.split()[-1]) for col in wavelength_columns]
#         values = row[wavelength_columns].values

#         # Crear el gráfico
#         plt.figure(figsize=(8, 6))
#         plt.plot(wavelengths, values, marker='o', label=f"{nombre} (Radio {radio})")
#         plt.title(f"Longitud de Onda vs. Valor\n{nombre} - Radio {radio}")
#         plt.xlabel("Longitud de Onda")
#         plt.ylabel("Valor")
#         plt.grid(True)
#         plt.legend()
#         plt.show()
        
def plot_from_excel(file_name, sheet_name):
    """
    Lee un archivo Excel y genera gráficos de valor vs. longitud de onda 
    para cada combinación de nombre y radio.

    Args:
        file_name (str): El nombre del archivo Excel.
        sheet_name (str): El nombre de la hoja a leer.
    """
    # Leer la hoja específica del archivo Excel
    try:
        df = pd.read_excel(file_name, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"El archivo {file_name} no fue encontrado.")
        return
    except ValueError:
        print(f"La hoja {sheet_name} no existe en el archivo {file_name}.")
        return

    # Verificar que las columnas requeridas existan
    if not {'Nombre', 'Radio'}.issubset(df.columns):
        print("El archivo Excel no tiene las columnas 'Nombre' y 'Radio'.")
        return

    # Extraer las columnas de longitudes de onda
    wavelength_columns = [col for col in df.columns if col.startswith('Wavelength')]
    #print(wavelength_columns)
    if not wavelength_columns:
        print("No se encontraron columnas de longitud de onda en el archivo Excel.")
        return
    
    group_index= DataStructure()
    disperssion= DataStructure()
    c=3e8
    # Crear gráficos para cada combinación de Nombre y Radio
    for _, row in df.iterrows():

        nombre = row['Nombre']
        radio = row['Radio']
        print(nombre, radio)
        # Extraer las longitudes de onda como flotantes y los valores correspondientes
        wavelengths = [float(col.split()[-1]) for col in wavelength_columns]
        values = row[wavelength_columns].values
        
        delta_w=wavelengths[1]-wavelengths[0]
        gradient=np.gradient(values,delta_w)
        dble_gradient=np.gradient(gradient,delta_w)
        
        group_index.add(nombre, radio, values[15]-wavelengths[15]*gradient[15])
        disperssion.add(nombre, radio, -wavelengths[15]**2*dble_gradient[15]/c)
        # # Crear el gráfico
        # plt.figure(figsize=(8, 6))
        # plt.plot(values, wavelengths, marker='o', label=f"{nombre} - Radio {radio}")
        # plt.title(f"{nombre} - Radio {radio}")
        # plt.xlabel("Valor")
        # plt.ylabel("Longitud de Onda (m)")
        # plt.grid(True)
        # plt.legend()

        # # Guardar el gráfico como archivo PNG
        # plt.savefig(f"{nombre}_Radio_{radio}.png", dpi=300)
        # plt.show()
    group_index.to_excel('Mode_{}.xlsx'.format(str(int(wavelengths[15]*1e9)) + "nm"),'Group Index calculated')
    disperssion.to_excel('Mode_{}.xlsx'.format(str(int(wavelengths[15]*1e9)) + "nm"),'Disspersion')
    return 
    
w,g=plot_from_excel('Mode_1500nm.xlsx','Effective Indexes for analysis')