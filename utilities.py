import pandas as pd
import unicodedata

def separate_hours(hours):
    """Transform string hh:mm-hh:mm to float."""
    if hours == '-':
        return 0, 0  # Use 0.0 for numeric operations
    start, end = hours.split("-")
    start, end = start.lstrip("0").replace(":00", ""), end.lstrip("0").replace(":00", "")
    return int(start), int(end)

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
    siia = pd.read_excel(path, usecols=["AREA","MATERIA","SEMESTRE","GRUPO","MAESTRO","NOMBRE","NOMBREMATE","LUNES","MARTES","MIERCOLES","JUEVES","VIERNES","AULALUNES","AULAMARTES","AULAMIERCO","AULAJUEVES","AULAVIERNE", "AULA"]).rename(columns=columns_mapping)
    siia['CVE PROFESOR'] = siia['CVE PROFESOR'].astype('Int64')
    # Apply accent and punctuation removal
    siia['PROFESOR'] = siia['PROFESOR'].apply(remove_accents).str.replace(r'[.,]', '', regex=True)
    siia['MATERIA'] = siia['MATERIA'].apply(remove_accents).str.replace(r'[.,]', '', regex=True)

    # Replace special characters
    siia['PROFESOR'] = siia['PROFESOR'].str.replace(r'—', 'N', regex=True)
    siia['MATERIA'] = siia['MATERIA'].str.replace("—", "N", case=False, regex=True)
    
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
        siia[sa_column] = siia['AULA'].where(siia[d[:2]]>0.0, "")
    siia.drop(labels=['AULA'], axis=1, inplace=True)

    # Check and process different SA values
    dias_aula = ['LUNES', 'MARTES', 'MIERCO', 'JUEVES', 'VIERNE']
    for i, d in enumerate(dias_aula):
        sa_column = 'SA' if i == 0 else f'SA.{i}'
        aula_column = f'AULA{d}'
        siia[sa_column] = siia[aula_column].where((pd.notna(siia[aula_column])) & (siia[aula_column] != ''), siia[sa_column])
        siia.drop(labels=[aula_column], axis=1, inplace=True)

    # Convert data types and aggregate
    siia = siia.convert_dtypes().fillna("")  # Fill NaNs in string columns with an empty string
    siia = siia.fillna(0)  # Ensure numeric columns have 0 instead of NaN
    aggregated = siia.groupby(['GRUPO', 'BLOQUE', 'CVEM', 'PE', 'CVE PROFESOR'], as_index=False).agg(
        {col: 'max' for col in siia.columns if col not in ['GRUPO', 'BLOQUE', 'CVEM', 'PE', 'CVE PROFESOR']}
    )
    
    return convert_types(aggregated)

def read_ch(path):
    """Import and process CH Excel data with specified dtypes."""
    required_columns = ['GRUPO', 'BLOQUE', 'CVEM', 'MATERIA', 'PE', 'CVE PROFESOR', 'PROFESOR',
                        'LU', 'LU.1', 'SA', 'MA', 'MA.1', 'SA.1', 'MI', 'MI.1', 'SA.2', 'JU',
                        'JU.1', 'SA.3', 'VI', 'VI.1', 'SA.4']
    try:
        ch = pd.read_excel(path, skiprows=4).drop(columns=['No'])

        # if missing columns do not execute
        missing_columns = [col for col in required_columns if col not in ch.columns]
        if missing_columns:
            raise KeyError(f"Columnas faltantes: {', '.join(missing_columns)}")
        
        # Apply accent and punctuation removal
        ch['PROFESOR'] = ch['PROFESOR'].apply(remove_accents).str.replace(r'[.,]', '', regex=True)
        ch['MATERIA'] = ch['MATERIA'].apply(remove_accents).str.replace(r'[.,]', '', regex=True)

        # Replace special characters
        ch['PROFESOR'] = ch['PROFESOR'].str.replace(r'—', 'Ñ', regex=True)
        ch['MATERIA'] = ch['MATERIA'].str.replace("—", "Ñ", case=False, regex=True)
        return convert_types(ch)
    except KeyError as e:
        print(f"Error: El formato del archivo Excel es inválido. {e}")
    except Exception as e:
        print(f"Error: No se pudo procesar el archivo Excel. Detalles: {e}")
    
def change_col_order(df):
    df = df[['GRUPO', 'BLOQUE', 'CVEM', 'MATERIA', 'PE', 'CVE PROFESOR', 'PROFESOR',
        'LU', 'LU.1', 'SA', 'MA', 'MA.1', 'SA.1', 'MI', 'MI.1', 'SA.2', 'JU',
        'JU.1', 'SA.3', 'VI', 'VI.1', 'SA.4']]
    return df

def convert_types(df):
    # Fill NaNs and empty strings with appropriate values
    df = df.fillna({
        'GRUPO': 0, 'BLOQUE': 0, 'CVEM': 0, 'MATERIA': "",
        'PE': "", 'CVE PROFESOR': 0, 'PROFESOR': "",
        'LU': 0, 'LU.1': 0, 'MA': 0, 'MA.1': 0, 'MI': 0, 'MI.1': 0, 
        'JU': 0, 'JU.1': 0, 'VI': 0, 'VI.1': 0,
        'SA': "", 'SA.1': "", 'SA.2': "", 'SA.3': "", 'SA.4': ""
    })

    # Remove any non-numeric values and convert to int
    int_columns = [
        'GRUPO', 'BLOQUE', 'CVEM', 'CVE PROFESOR', 
        'LU', 'LU.1', 'MA', 'MA.1', 'MI', 'MI.1',
        'JU', 'JU.1', 'VI', 'VI.1'
    ]
    for column in int_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0).astype('Int64')

    # Convert string columns
    string_columns = [
        'MATERIA', 'PE', 'PROFESOR', 
        'SA', 'SA.1', 'SA.2', 'SA.3', 'SA.4'
    ]
    for column in string_columns:
        df[column] = df[column].astype('string[python]')
    
    return df

def highlight(row):
    theres_blank, styles = blank_row(row)
    
    if theres_blank:
        return styles
    
    for col in row.index:
        condition = ('PROFESOR_' in col) or ('MATERIA_' in col)

        if not condition and ('_ch' in col):
            col_base = col.replace('_ch', '')
            val_ch = row[col]
            val_siia = row.get(f'{col_base}_siia')
            
            if pd.isna(val_siia) and pd.isna(val_ch):
                styles.append('')  # No highlight, both are NaN
            elif (pd.isna(val_siia) and not pd.isna(val_ch)) or (not pd.isna(val_siia) and pd.isna(val_ch)):
                styles.append('background-color: red')  # Highlight if one is NaN and the other is not
            elif val_siia != val_ch:
                styles.append('background-color: red')  # Highlight if different
            else:
                styles.append('')  # No highlight if they are the same
        else:
            styles.append('')
    return styles

def highlight_differences(siia, ch):
    # Merge df on the key columns
    comparison = ch.merge(siia, on=['GRUPO', 'BLOQUE', 'CVEM', 'PE'], suffixes=('_ch', '_siia'), how='outer')
    df = comparison.style.apply(highlight, axis=1)
    return df

def insert_na(data):
    return data.replace(to_replace=[0, ''], value=pd.NA)

def blank_row(row):
    styles = []
    blank_siia = True if (pd.isna(row.get('CVE PROFESOR_siia')) or row.get('CVE PROFESOR_siia')==0) and (pd.isna(row.get('MATERIA_siia')) or row.get('MATERIA_siia')=='') else False
    blank_ch = True if (pd.isna(row.get('CVE PROFESOR_ch')) or row.get('CVE PROFESOR_ch')==0) and (pd.isna(row.get('MATERIA_ch')) or row.get('MATERIA_ch')=='') else False
    there_are = True if blank_siia or blank_ch else False
    
    if not there_are:
        return there_are, styles

    for _ in row.index:
        if blank_siia:
            styles.append('background-color: orange')
        if blank_ch:
            styles.append('background-color: yellow')

    return there_are, styles
