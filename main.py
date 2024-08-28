import pandas as pd
import numpy as np
from utilities import separateHours 

siia = pd.read_excel(r'carga siia 232.xlsx') # ! Change for user path
ch = pd.read_excel(r'CH 2023-2.xlsx', skiprows = 4) # ! Change for user path

# * DATA CLEANING PROCESS

dias = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES']
for d in dias:
    siia[[d[:2] , d[:2]+'.1']] = siia[d].apply(separateHours).apply(pd.Series)
for d in dias:
    siia.drop(d, axis = 1)

# * COMPARE PROCESS
