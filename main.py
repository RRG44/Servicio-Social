import pandas as pd
import numpy as np
from utilities import separateHours 

siiaPath = r'cargasiia232.xlsx' # ! Change for user path
chPath = r'CH2023-2.xlsx' # ! Change for user path

siia = pd.read_excel(siiaPath, usecols="C:F,H,K,N,R:V,Z,AJ,AL,AN,AP,AR").astype({"MAESTRO":'float'})
ch = pd.read_excel(chPath,skiprows = 4) #bien

# * DATA CLEANING PROCESS

# creates LU, LU.1, etc from LUNES, etc and deletes the unused col
dias = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES']
for d in dias:
    siia[[d[:2] , d[:2]+'.1']] = siia[d].apply(separateHours).apply(pd.Series)
for d in dias:
    siia.drop(d, axis = 1)

# * COMPARE PROCESS
