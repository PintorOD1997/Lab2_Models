
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import data as dt
import numpy as np
import pandas as pd 
import functions as ft
OB = dt.openOB()


# Calcular el midprice
x,_,_ = ft.OB_metrics(OB)
midprice = x["Mid Price"]
# Contabilizar ocurrencias de escenarios (Utilizando todos los datos)
# e1 = midprice_t == midprice_t+1
# e2 = midprice_t != midprice_t+1, e2 = total_datos - e1
e1 = [midprice[i] == midprice[i+1] for i in range(len(midprice)-1)]
e2 = [midprice[i] != midprice[i+1] for i in range(len(midprice)-1)] # puede ser definido por antonomasia

metricas = {"e1" : {"cantidad" : sum(e1), "proporcion" : sum(e1)/len(midprice)}, 
            "e2" : {"cantidad" : sum(e2), "proporcion" : sum(e2)/len(midprice)},
            "total" : len(midprice)-1 }


# Imprimir el resultado como una tabla

# Repetir lo anterior para otros (Experimentos con datos de cada minuto)

# Experimentos: 00:06:00 - 00:07:00 ... 00:05:00 - 00:06:00


# Hacer un dataframe con resultados finales
