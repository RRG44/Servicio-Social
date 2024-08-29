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
siia.rename(columns={
    'SEMESTRE': 'BLOQUE',
    'MATERIA': 'CVEM',
    'NOMBREMATE': 'MATERIA',
    'AREA': 'PE',
    'MAESTRO': 'CVE PROFESOR',
    'NOMBRE': 'PROFESOR',
    'AULALUNES': 'SA',
    'AULAMARTES': 'SA.1',
    'AULAMIERCO': 'SA.2',
    'AULAJUEVES': 'SA.3',
    'AULAVIERNE': 'SA.4'
}, inplace=True)

# * ADDING AULA TO SA.1, SA.2, ETC DEPENDING ON THE DAY AND CLEARING AULA IF MOVED
# Mapping days to their respective columns
day_to_sa = {
    'LU': 'SA',
    'MA': 'SA.1',
    'MI': 'SA.2',
    'JU': 'SA.3',
    'VI': 'SA.4'
}

# Adding aula to SA.1, SA.2, etc. depending on the day and clearing AULA if moved
for day, sa in day_to_sa.items():
    condition = siia[day].notnull() | siia[f'{day}.1'].notnull()
    siia[sa] = np.where(condition, siia['AULA'], siia[sa])
    siia['AULA'] = np.where(condition, np.nan, siia['AULA'])

# Merge rows with the same CVEM, GRUPO, BLOQUE, MATERIA, PE, CVE PROFESOR, PROFESOR and concatenate the SA.1, SA.2, SA.3, SA.4, SA.5 columns and lu, lu.1, etc
siia = siia.groupby(['CVEM', 'GRUPO', 'BLOQUE', 'MATERIA', 'PE', 'CVE PROFESOR', 'PROFESOR'], as_index=False).agg({
    'SA': lambda x: ', '.join(x.dropna().astype(str)),
    'SA.1': lambda x: ', '.join(x.dropna().astype(str)),
    'SA.2': lambda x: ', '.join(x.dropna().astype(str)),
    'SA.3': lambda x: ', '.join(x.dropna().astype(str)),
    'SA.4': lambda x: ', '.join(x.dropna().astype(str)),
    'LU': lambda x: ', '.join(x.dropna().astype(str)),
    'LU.1': lambda x: ', '.join(x.dropna().astype(str)),
    'MA': lambda x: ', '.join(x.dropna().astype(str)),
    'MA.1': lambda x: ', '.join(x.dropna().astype(str)),
    'MI': lambda x: ', '.join(x.dropna().astype(str)),
    'MI.1': lambda x: ', '.join(x.dropna().astype(str)),
    'JU': lambda x: ', '.join(x.dropna().astype(str)),
    'JU.1': lambda x: ', '.join(x.dropna().astype(str)),
    'VI': lambda x: ', '.join(x.dropna().astype(str)),
    'VI.1': lambda x: ', '.join(x.dropna().astype(str))
})
# Organize the columns of frame siia in the order of the CH
siia = siia[[ 'GRUPO', 'BLOQUE', 'CVEM', 'MATERIA', 'PE', 'CVE PROFESOR', 'PROFESOR', 'LU','LU.1','SA','MA','MA.1','SA.1','MI','MI.1','SA.2','JU','JU.1','SA.3','VI','VI.1','SA.4']]
# * COMPARE PROCESS