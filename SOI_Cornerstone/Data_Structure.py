# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 20:00:58 2024

@author: Antonio
"""

import pandas as pd
import openpyxl
from openpyxl.chart import LineChart, Reference


class DataStructure:
    def __init__(self):
        self.data = {}
        self.wavelength_data = {}

    def add(self, nombre, radio, numero):
        if nombre not in self.data:
            self.data[nombre] = {}
        self.data[nombre][radio] = numero

    def add_with_wavelength(self, nombre, radio, wavelength, valor):
        if nombre not in self.wavelength_data:
            self.wavelength_data[nombre] = {}
        if radio not in self.wavelength_data[nombre]:
            self.wavelength_data[nombre][radio] = {}
        self.wavelength_data[nombre][radio][wavelength] = valor

    def get_by_nombre(self, nombre):
        return self.data.get(nombre, {})

    def get_by_radio(self, radio):
        result = {}
        for nombre, radios in self.data.items():
            if radio in radios:
                result[nombre] = radios[radio]
        return result

    def get_all_nombres(self):
        return list(self.data.keys())

    def to_excel(self, filename, sheet_name):
        # Obtener todos los radios únicos
        all_radios = set()
        for radios in self.data.values():
            all_radios.update(radios.keys())
        all_radios = sorted(all_radios)

        # Crear un DataFrame con los radios como índice y los nombres como columnas
        df = pd.DataFrame(index=all_radios)
        for nombre, radios in self.data.items():
            df[nombre] = pd.Series(radios)

        # Escribir el DataFrame al archivo Excel
        try:
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a') as writer:
                df.to_excel(writer, sheet_name=sheet_name)
        except FileNotFoundError:
            with pd.ExcelWriter(filename, engine='openpyxl', mode='w') as writer:
                df.to_excel(writer, sheet_name=sheet_name)

        # Agregar gráficos al archivo Excel
        wb = openpyxl.load_workbook(filename)
        ws = wb[sheet_name]

        chart = LineChart()
        chart.title = "Gráfico de Datos"
        chart.style = 13
        chart.y_axis.title = 'Valor'
        chart.x_axis.title = 'Radio'

        data = Reference(ws, min_col=2, min_row=1, max_col=len(df.columns)+1, max_row=len(df.index)+1)
        categories = Reference(ws, min_col=1, min_row=2, max_row=len(df.index)+1)

        chart.add_data(data, titles_from_data=True)
        chart.set_categories(categories)

        ws.add_chart(chart, "E5")
        wb.save(filename)
        
    def to_excel_with_wavelength(self, filename, sheet_name):
        # Obtener todos los nombres, radios y longitudes de onda únicos
        all_wavelengths = sorted({wavelength for nombre_data in self.wavelength_data.values()
                                   for radio_data in nombre_data.values() for wavelength in radio_data.keys()})
    
        # Crear una lista para almacenar las filas de datos
        rows = []
        for nombre, radios in self.wavelength_data.items():
            for radio, wavelengths in radios.items():
                row = [nombre, radio]
                # Agregar los valores de las longitudes de onda en el orden correcto
                row.extend(wavelengths.get(wl, None) for wl in all_wavelengths)
                rows.append(row)
    
        # Crear un DataFrame con los nombres y radios como primeras columnas
        columns = ['Nombre', 'Radio'] + [f"Wavelength {wl}" for wl in all_wavelengths]
        df = pd.DataFrame(rows, columns=columns)
    
        # Escribir el DataFrame al archivo Excel
        try:
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        except FileNotFoundError:
            with pd.ExcelWriter(filename, engine='openpyxl', mode='w') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)


# # Ejemplo de uso
# ds1 = DataStructure()
# ds1.add("objeto1", 5, 100)
# ds1.add("objeto1", 10, 200)
# ds1.add("objeto2", 5, 300)

# # Convertir el primer DataStructure a un archivo Excel en la hoja 'Hoja1'
# ds1.to_excel('data_structure.xlsx', 'Hoja1')

# ds2 = DataStructure()
# ds2.add("objeto3", 15, 400)
# ds2.add("objeto4", 20, 500)

# # Convertir el segundo DataStructure a una nueva hoja en el mismo archivo Excel
# ds2.to_excel('data_structure.xlsx', 'Hoja2')

# print("El archivo Excel se ha actualizado exitosamente con múltiples hojas.")