import pandas as pd
import numpy as np
import utilities as util

siiaPath = r'cargasiia232.xlsx' # ! Change for user path
chPath = r'CH2023-2.xlsx' # ! Change for user path

# file reading
siia = util.read_siia(siiaPath)
ch = util.read_ch(chPath)

# highlighting
dfp = util.highlight_differences(siia, ch)
dfp.to_excel('comparison_output.xlsx', engine='openpyxl', index=False)