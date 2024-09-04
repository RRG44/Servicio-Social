import pandas as pd
import unicodedata

def separate_hours(hours):
    """Transform string hh:mm-hh:mm to float."""
    if hours == '-':
        return None, None
    start, end = hours.split("-")
    start, end = start.lstrip("0").replace(":00", ""), end.lstrip("0").replace(":00", "")
    return float(start), float(end)

def remove_accents(input_str):
    """Remove accents and punctuation from a string."""
    if isinstance(input_str, str):
        return ''.join(c for c in unicodedata.normalize('NFKD', input_str) if not unicodedata.combining(c))
    return input_str

def read_siia(path):
    """Import and process SIIA Excel data."""
    columns_mapping = {
        'SEMESTRE': 'BLOQUE', 'MATERIA': 'CVEM', 'NOMBREMATE': 'MATERIA',
        'AREA': 'PE', 'MAESTRO': 'CVE PROFESOR', 'NOMBRE': 'PROFESOR'
    }
    
    # TODO: try catch format NOE
    

    def validar_excel(file_path):
        expected_columns = [
            'PERIODO', 'ADSCRIP', 'AREA', 'MATERIA', 'SEMESTRE', 'GRUPO',
            'LABORATORI', 'MAESTRO', 'HORAS', 'TIPOHOR', 'NOMBRE', 'CVECARPRED',
            'PUESTO', 'NOMBREMATE', 'FORMPAG', 'FECINIP', 'TIPOHORA', 'LUNES',
            'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'CARRERA',
            'EDIFICIO', 'AULA', 'ADSCRIPCIO', 'CUPO', 'SUPLENTE', 'MOTIVO',
            'FECHASSUPL', 'FECHCAPTUR', 'CAPTURO', 'CARGA', 'EDIFLUNES',
            'AULALUNES', 'EDIFMARTES', 'AULAMARTES', 'EDIFMIERCO', 'AULAMIERCO',
            'EDIFJUEVES', 'AULAJUEVES', 'EDIFVIERNE', 'AULAVIERNE', 'EDIFSABADO',
            'AULASABADO'
        ]
        
        try:
            # Cargar el archivo Excel
            data = pd.read_excel(r'C:\Users\casti\OneDrive\Documentos\SS\carga siia 232.xlsx')

            # Verificar que todas las columnas esperadas estén presentes
            missing_columns = [col for col in expected_columns if col not in data.columns]
            if missing_columns:
                raise ValueError(f"Las siguientes columnas faltan en el archivo: {', '.join(missing_columns)}")
            
            # Aquí podrías agregar más validaciones, como los tipos de datos

            print("El archivo es válido y cumple con el formato esperado.")
            
        except Exception as e:
            print(f"Error al validar el archivo: {str(e)}")

    # Ejemplo de uso
    file_path = r'C:\Users\casti\OneDrive\Documentos\SS\carga siia 232.xlsx'
    validar_excel(file_path)
        


    siia = pd.read_excel(path, usecols="C:F,H,K,N,R:V,Z,AJ,AL,AN,AP,AR").rename(columns=columns_mapping)
    siia['CVE PROFESOR'] = siia['CVE PROFESOR'].astype(float)
    
    # Apply accent and punctuation removal
    siia['PROFESOR'] = siia['PROFESOR'].apply(remove_accents).str.replace(r'[.,]', '', regex=True)
    siia['MATERIA'] = siia['MATERIA'].apply(remove_accents).str.replace(r'[.,]', '', regex=True)
    
    # Replace special characters
    siia['PROFESOR'] = siia['PROFESOR'].str.replace(r'—', 'Ñ', regex=True)
    siia['MATERIA'] = siia['MATERIA'].str.replace("—", "Ñ", case=False, regex=True)
    
    # Adjust GRUPO column
    siia['GRUPO'] = siia['GRUPO'] % 100

    # Process days of the week
    dias = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES']
    for d in dias:
        siia[[d[:2], d[:2]+'.1']] = siia[d].apply(separate_hours).apply(pd.Series)
    siia.drop(labels=dias, axis=1, inplace=True)
    
    # Process AULA data
    for i, d in enumerate(dias):
        sa_column = 'SA' if i == 0 else f'SA.{i}'
        siia[sa_column] = siia['AULA'].where(pd.notna(siia[d[:2]]))
    siia.drop(labels=['AULA'], axis=1, inplace=True)
    
    # Check and process different SA values
    dias_aula = ['LUNES', 'MARTES', 'MIERCO', 'JUEVES', 'VIERNE']
    for i, d in enumerate(dias_aula):
        sa_column = 'SA' if i == 0 else f'SA.{i}'
        aula_column = f'AULA{d}'
        siia[sa_column] = siia[aula_column].where(pd.notna(siia[aula_column]), siia[sa_column])
        siia.drop(labels=[aula_column], axis=1, inplace=True)
    
    # Convert data types and aggregate
    siia = siia.convert_dtypes()
    aggregated = siia.groupby(['GRUPO', 'BLOQUE', 'CVEM', 'PE', 'CVE PROFESOR'], as_index=False).agg(
        {col: 'max' for col in siia.columns if col not in ['GRUPO', 'BLOQUE', 'CVEM', 'PE', 'CVE PROFESOR']}
    )
    return aggregated

def read_ch(path):
    """Import and process CH Excel data."""
    required_columns = ['GRUPO', 'BLOQUE', 'CVEM', 'MATERIA', 'PE', 'CVE PROFESOR', 'PROFESOR',
                        'LU', 'LU.1', 'SA', 'MA', 'MA.1', 'SA.1', 'MI', 'MI.1', 'SA.2', 'JU',
                        'JU.1', 'SA.3', 'VI', 'VI.1', 'SA.4']
    try:
        ch = pd.read_excel(path, skiprows=4).drop(columns=['No'])
        ch = ch.convert_dtypes()

        # Check if all required columns are present
        missing_columns = [col for col in required_columns if col not in ch.columns]
        if missing_columns:
            raise KeyError(f"Columnas faltantes: {', '.join(missing_columns)}")

        return ch
    except KeyError as e:
        print(f"Error: El formato del archivo Excel es inválido. {e}")
    except Exception as e:
        print(f"Error: No se pudo procesar el archivo Excel. Detalles: {e}")

def change_col_order(df):
    df = df[['GRUPO', 'BLOQUE', 'CVEM', 'MATERIA', 'PE', 'CVE PROFESOR', 'PROFESOR',
        'LU', 'LU.1', 'SA', 'MA', 'MA.1', 'SA.1', 'MI', 'MI.1', 'SA.2', 'JU',
        'JU.1', 'SA.3', 'VI', 'VI.1', 'SA.4']]
    return df