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

# * FORMATTING COLUMN NAMES PROCESS
# Renames the columns Semestre to Bloque
siia.rename(columns={'SEMESTRE':'BLOQUE'}, inplace=True)
# Renames the columns Materia to CVEM
siia.rename(columns={'MATERIA':'CVEM'}, inplace=True)
# Renames the columns Nombremate to Materia
siia.rename(columns={'NOMBREMATE':'MATERIA'}, inplace=True)
# Renames the columns Area to Pe
siia.rename(columns={'AREA':'PE'}, inplace=True)
# Renames the columns Maestro to CVE Profesor
siia.rename(columns={'MAESTRO':'CVE PROFESOR'}, inplace=True)
# Renames the columns Nombre to Profesor
siia.rename(columns={'NOMBRE':'PROFESOR'}, inplace=True)
# Renames the columns AulaLunes to SA.1, AulaMartes to SA.2, AulaMiercoles to SA.3, AulaJueves to SA.4, AulaViernes to SA.5
siia.rename(columns={'AULALUNES':'SA.1', 'AULAMARTES':'SA.2', 'AULAMIERCO':'SA.3', 'AULAJUEVES':'SA.4', 'AULAVIERNE':'SA.5'}, inplace=True)

# * ADDING AULA TO SA.1, SA.2, ETC DEPENDING ON THE DAY AND CLEARING AULA IF MOVED
# Mapping days to their respective columns
day_to_sa = {
    'LU': 'SA.1',
    'MA': 'SA.2',
    'MI': 'SA.3',
    'JU': 'SA.4',
    'VI': 'SA.5'
}

# Adding aula to SA.1, SA.2, etc. depending on the day and clearing AULA if moved
for day, sa in day_to_sa.items():
    condition = siia[day].notnull() | siia[f'{day}.1'].notnull()
    siia[sa] = np.where(condition, siia['AULA'], siia[sa])
    siia['AULA'] = np.where(condition, np.nan, siia['AULA'])
    
# * COMPARE PROCESS