import pandas as pd
import numpy as np
import utilities as util

siiaPath = r'C:\Users\casti\OneDrive\Documentos\SS\carga siia 232.xlsx'
chPath = r'C:\Users\casti\OneDrive\Documentos\SS\CH 2023-2.xlsx' 

siia = util.read_siia(siiaPath)
ch = util.read_ch(chPath)