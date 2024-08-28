import pandas as pd
import numpy as np
import unicodedata
import re
from utilities import separateHours, remove_accents

siiaPath = r'cargasiia232.xlsx' # ! Change for user path
chPath = r'CH2023-2.xlsx' # ! Change for user path

#Importing the siia EXCEL file with the columns that we only need (Check the Google DOCS), and with MAESTRO column as float
siia = pd.read_excel(siiaPath, usecols="C:F,H,K,N,R:V,Z,AJ,AL,AN,AP,AR").astype({"MAESTRO":'float'})
#Importing the CH EXCEL, skiping the image on it
ch = pd.read_excel(chPath,skiprows = 4) #bien

# * DATA CLEANING PROCESS

# creates LU, LU.1, etc from LUNES, etc and deletes the unused col
dias = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES']
for d in dias:
    siia[[d[:2] , d[:2]+'.1']] = siia[d].apply(separateHours).apply(pd.Series)
for d in dias:
    siia.drop(d, axis = 1)
    
# * FORMATTING TEXT PROCESS

# Aply the funcion to eliminate acents and replace the dots in the columns
siia['NOMBRE'] = siia['NOMBRE'].apply(remove_accents).str.replace(r'[.,]', '', regex=True)
siia['NOMBREMATE'] = siia['NOMBREMATE'].apply(remove_accents).str.replace(r'[.,]', '', regex=True)

# Replace the - signs in the NOMBRE column (Professor's name) with the Ñ
siia['NOMBRE'] = siia['NOMBRE'].str.replace(r'—', 'Ñ', regex=True)
# Replace the - signs in the NOMBREMATE column (Subject's name) with the Ñ
siia['NOMBREMATE'] = siia['NOMBREMATE'].str.replace("—", "Ñ", case=False, regex=True)

# Modifies the 'GRUPO' column, so it matches the 'GRUPO' column from the FIF
siia['GRUPO'] = siia['GRUPO'] % 100

# * COMPARE PROCESS