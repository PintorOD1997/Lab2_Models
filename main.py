
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Lab 2: Models                                                       -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: pintorOD1997                                                            -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: https://github.com/PintorOD1997/Lab2_Models                                                         -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import data as dt
import numpy as np
import pandas as pd 
import functions as ft
OB = dt.openOB()



#TESTnuevafuncionMidPrices
from functions import totalMidPrice
midP = totalMidPrice(OB)


data_ob = OB
# Resampleando
ob_ts = list(data_ob.keys())

l_ts = [pd.to_datetime(i_ts) for i_ts in ob_ts]




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

midprice = pd.DataFrame(midprice)

dic = {}
for index, row in midprice.iterrows():
    key = str(index.hour) + ":" + str(index.minute)
    value = row["Mid Price"]
    try:
        dic[key].append(value)
    except KeyError:
        dic[key] = [value]
    
metricasMin = {}
for i in list(dic): # <- iteración sobre índices del diccionario
    e1 = sum([dic[i][i_t] == dic[i][i_t+1] for i_t in range(len(dic[i])-1)])
    e2 = sum([dic[i][i_t] != dic[i][i_t+1] for i_t in range(len(dic[i])-1)])
    metricasMin[i] = (
        {"e1" :{"cantidad" :  e1, "proporcion" : e1/(len(dic[i])-1)}, 
         "e2" :{"cantidad" :  e2, "proporcion" : e2/(len(dic[i])-1)},
         "total" : len(dic[i])-1
         }
        )
  
tot = []
for i in list(metricasMin):
    tot.append(metricasMin[i]["total"])
np.array(tot).sum()

# Proporción de frecuencia de martingalas
mgE1 = []
for i in list(metricasMin):
    mgE1.append(metricasMin[i]["e1"]["cantidad"])
np.array(mgE1).sum()/np.array(tot).sum()

# Promedio de proporción de martingalas
propE1 = []
for i in list(metricasMin):
    propE1.append(metricasMin[i]["e1"]["proporcion"])
np.array(propE1).mean()

#datos para llenar df fnal:
df_exp2 = pd.DataFrame(metricasMin).T
df_e1_exp2=pd.DataFrame(df_exp2["e1"][i] for i in range(0,60))
df_e1_exp2_conteo = pd.DataFrame(df_e1_exp2["cantidad"])
df_e2_exp2=pd.DataFrame(df_exp2["e2"][i] for i in range(0,60))
df_e2_exp2_conteo = pd.DataFrame(df_e2_exp2["cantidad"])
df_e1_exp2_proporcion = pd.DataFrame(df_e1_exp2["proporcion"])
df_e2_exp2_proporcion = pd.DataFrame(1-df_e1_exp2["proporcion"])
df_exp2_total = pd.DataFrame(df_e1_exp2_conteo["cantidad"]+df_e2_exp2_conteo["cantidad"])


# llenar el df del experimento 2:
df_exp2_2 = pd.DataFrame()
df_exp2_2 = df_exp2_2.assign(e1=None)
df_exp2_2 = df_exp2_2.assign(e2=None)
df_exp2_2 = df_exp2_2.assign(total=None)
df_exp2_2 = df_exp2_2.assign(proporcion1=None)
df_exp2_2 = df_exp2_2.assign(proporcion2=None)
times = (l_ts)
valor_e1 = df_e1_exp2_conteo 
valor_e2 = df_e2_exp2_conteo 
valor_total = df_exp2_total
valor_proporcion1 = df_e1_exp2_proporcion 
valor_proporcion2 = df_e2_exp2_proporcion 
df_exp2_2['e1'] = valor_e1
df_exp2_2['e2'] = valor_e2
df_exp2_2['total'] = valor_e1+valor_e2
df_exp2_2['proporcion1'] = valor_proporcion1
df_exp2_2['proporcion2'] = valor_proporcion2
df_exp2_2.index = midprice.resample('60S').asfreq()[0:-1].index 
df_exp2_2


# Repetir lo anterior para otros (Experimentos con datos de cada minuto)

# Experimentos: 00:06:00 - 00:07:00 ... 00:05:00 - 00:06:00


# Hacer un dataframe con resultados finales


# Para Weighted Midprice
x,_,_ = ft.OB_metrics(OB)
Wmidprice = x["Weighted MidPrice (Ask)"]
# Contabilizar ocurrencias de escenarios (Utilizando todos los datos)
# e1 = midprice_t == midprice_t+1
# e2 = midprice_t != midprice_t+1, e2 = total_datos - e1

e1 = [Wmidprice[i] == Wmidprice[i+1] for i in range(len(Wmidprice)-1)]
e2 = [Wmidprice[i] != Wmidprice[i+1] for i in range(len(Wmidprice)-1)] # puede ser definido por antonomasia

Wmetricas = {"e1" : {"cantidad" : sum(e1), "proporcion" : sum(e1)/len(Wmidprice)}, 
            "e2" : {"cantidad" : sum(e2), "proporcion" : sum(e2)/len(Wmidprice)},
            "total" : len(Wmidprice)-1 }
Wmidprice = pd.DataFrame(Wmidprice)

Wdic = {}
for index, row in Wmidprice.iterrows():
    key = str(index.hour) + ":" + str(index.minute)
    value = row["Weighted MidPrice (Ask)"]
    try:
        Wdic[key].append(value)
    except KeyError:
        Wdic[key] = [value]
    
WmetricasMin = {}
for i in list(dic): # <- iteración sobre índices del diccionario
    e1 = sum([dic[i][i_t] == dic[i][i_t+1] for i_t in range(len(dic[i])-1)])
    e2 = sum([dic[i][i_t] != dic[i][i_t+1] for i_t in range(len(dic[i])-1)])
    WmetricasMin[i] = (
        {"e1" :{"cantidad" :  e1, "proporcion" : e1/(len(dic[i])-1)}, 
         "e2" :{"cantidad" :  e2, "proporcion" : e2/(len(dic[i])-1)},
         "total" : len(dic[i])-1
         }
        )
  
Wtot = []
for i in list(WmetricasMin):
    Wtot.append(WmetricasMin[i]["total"])
np.array(Wtot).sum()

# Proporción de frecuencia de martingalas
WmgE1 = []
for i in list(WmetricasMin):
    WmgE1.append(WmetricasMin[i]["e1"]["cantidad"])
np.array(WmgE1).sum()/np.array(Wtot).sum()

# Promedio de proporción de martingalas
WpropE1 = []
for i in list(WmetricasMin):
    WpropE1.append(WmetricasMin[i]["e1"]["proporcion"])
np.array(WpropE1).mean()

#datos para llenar df fnal:
df_exp2 = pd.DataFrame(WmetricasMin).T
df_e1_exp2=pd.DataFrame(df_exp2["e1"][i] for i in range(0,60))
df_e1_exp2_conteo = pd.DataFrame(df_e1_exp2["cantidad"])
df_e2_exp2=pd.DataFrame(df_exp2["e2"][i] for i in range(0,60))
df_e2_exp2_conteo = pd.DataFrame(df_e2_exp2["cantidad"])
df_e1_exp2_proporcion = pd.DataFrame(df_e1_exp2["proporcion"])
df_e2_exp2_proporcion = pd.DataFrame(1-df_e1_exp2["proporcion"])
df_exp2_total = pd.DataFrame(df_e1_exp2_conteo["cantidad"]+df_e2_exp2_conteo["cantidad"])


# llenar el df del experimento 2:
df_exp2_2 = pd.DataFrame()
df_exp2_2 = df_exp2_2.assign(e1=None)
df_exp2_2 = df_exp2_2.assign(e2=None)
df_exp2_2 = df_exp2_2.assign(total=None)
df_exp2_2 = df_exp2_2.assign(proporcion1=None)
df_exp2_2 = df_exp2_2.assign(proporcion2=None)
times = (l_ts)
valor_e1 = df_e1_exp2_conteo 
valor_e2 = df_e2_exp2_conteo 
valor_total = df_exp2_total
valor_proporcion1 = df_e1_exp2_proporcion 
valor_proporcion2 = df_e2_exp2_proporcion 
df_exp2_2['e1'] = valor_e1
df_exp2_2['e2'] = valor_e2
df_exp2_2['total'] = valor_e1+valor_e2
df_exp2_2['proporcion1'] = valor_proporcion1
df_exp2_2['proporcion2'] = valor_proporcion2
df_exp2_2.index = Wmidprice.resample('60S').asfreq()[0:-1].index 
df_exp2_2



# Modelo 2

