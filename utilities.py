import pandas as pd
import numpy as np
import unicodedata

def separateHours(hours):
    """This function transforms string hh:mm-hh:mm to float
        In: string Out: float, float"""
    if hours == '-' :
        return
    split = hours.split("-")

    for i in range(len(split)):
        split[i] = split[i].replace(":00", "")
        if split[i][0] == "0":
            split[i] = split[i][1:]

    return float(split[0]), float(split[1]) # Example hours: 8:00-9:00, output: 8.0, 9.0


def remove_accents(input_str):
    """Function to eliminate the acents and signs of punctuation in the data frame"""
    if isinstance(input_str, str):  # Verifica si el valor es una cadena
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    return input_str  # Devuelve el valor tal cual si no es una cadena


def readSiia(path):
    """Importing the siia EXCEL file with the columns that we only need (Check the Google DOCS), and with MAESTRO column as float"""
    
    siia =  pd.read_excel(path, usecols="C:F,H,K,N,R:V,Z,AJ,AL,AN,AP,AR").astype({"MAESTRO":'float'})
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

    # Aply the funcion to eliminate acents and replace the dots in the columns
    siia['PROFESOR'] = siia['PROFESOR'].apply(remove_accents).str.replace(r'[.,]', '', regex=True)
    siia['MATERIA'] = siia['MATERIA'].apply(remove_accents).str.replace(r'[.,]', '', regex=True)

    # Replace the - signs in the NOMBRE column (Professor's name) with the Ñ
    siia['PROFESOR'] = siia['PROFESOR'].str.replace(r'—', 'Ñ', regex=True)
    # Replace the - signs in the NOMBREMATE column (Subject's name) with the Ñ
    siia['MATERIA'] = siia['MATERIA'].str.replace("—", "Ñ", case=False, regex=True)

    # Modifies the 'GRUPO' column, so it matches the 'GRUPO' column from the FIF
    siia['GRUPO'] = siia['GRUPO'] % 100

    # Creates LU and LU.1 for each day
    dias = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES']
    for d in dias:
        siia[[d[:2] , d[:2]+'.1']] = siia[d].apply(separateHours).apply(pd.Series)
    siia.drop(labels=dias, axis = 1, inplace=True)

    # Creates SA for each day
    for i, d in enumerate(dias):
        if i > 0:
            siia[f'SA.{i}'] = siia['AULA'].where(pd.notna(siia[d[:2]]))
            continue
        siia['SA'] = siia['AULA'].where(pd.notna(siia[d[:2]]))
    siia.drop(labels=['AULA'], axis = 1, inplace=True)

    # Checks for different SA in each day
    dias_aula = ['LUNES', 'MARTES', 'MIERCO', 'JUEVES', 'VIERNE']

    for i, d in enumerate(dias_aula):
        if i > 0:
            siia[f'SA.{i}'] = siia[f'AULA{d}'].where(pd.notna(siia[f'AULA{d}']), siia[f'SA.{i}'])
            siia.drop(labels=[f'AULA{d}'], axis = 1, inplace=True)
            continue
        siia['SA'] = siia[f'AULA{d}'].where(pd.notna(siia[f'AULA{d}']), siia['SA'])
        siia.drop(labels=[f'AULA{d}'], axis = 1, inplace=True)

    mg = siia.convert_dtypes() # ! this changes all to target datatype and None, NaN to <NA>

    # This code formats to the specified format and combines same classes
    mg = mg.groupby(['GRUPO', 'BLOQUE', 'CVEM', 'PE', 'CVE PROFESOR'], as_index=False).agg(
        {
            'PROFESOR': 'max',
            'MATERIA' : 'max',
            'LU': 'max',
            'LU.1': 'max',
            'SA' : 'max',
            'MA': 'max',
            'MA.1': 'max',
            'SA.1' : 'max',
            'MI': 'max',
            'MI.1': 'max',
            'SA.2' : 'max',
            'JU': 'max',
            'JU.1': 'max',
            'SA.3' : 'max',
            'VI': 'max',
            'VI.1': 'max',
            'SA.4' : 'max',
        }
    )
    return mg


def readCH(path):
    """Importing the CH EXCEL, skiping the image on it"""
    ch = pd.read_excel(path,skiprows = 4)
    ch.drop(labels=['No'], axis=1, inplace=True)
    correct = ch.convert_dtypes() # ! this changes all to target datatype and None, NaN to <NA>
    return correct