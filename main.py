import pandas as pd
import numpy as np
import utilities as util

siiaPath = r'cargasiia232.xlsx' # ! Change for user path
chPath = r'CH2023-2.xlsx' # ! Change for user path

# file reading
siia = util.read_siia(siiaPath)
ch = util.read_ch(chPath)
siia = util.change_col_order(siia)
siia.insert(0, "div", "")

# highlighting
dfp = util.highlight_differences(siia, ch)
dfp.data = util.insert_na(dfp.data)

dfp.set_properties(**{
        'border': '1px solid black',
        'text-align': 'center',
    })

writer = pd.ExcelWriter('Comparasion.xlsx', engine='xlsxwriter')
dfp.to_excel(writer, sheet_name='Sheet1', index=False)

workbook = writer.book
worksheet = writer.sheets['Sheet1']

format_black = workbook.add_format({'bg_color': '#000000'})

for row in range(1, len(dfp.data) + 1):  # Comienza en la fila 1
    worksheet.write_blank(row, dfp.data.columns.get_loc('div'), None, format_black)  # Columna 1 corresponde a "Div"

for i, col in enumerate(dfp.data.columns):
    max_len = max(dfp.data[col].apply(lambda x: len(str(x))).max(), len(col))
    worksheet.set_column(i, i, max_len + 1)

writer.close()    



