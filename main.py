
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Lab 2: Models                                                                              -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: pintorOD1997                                                                                -- #
# -- license: GNU General Public License v3.0                                                            -- #
# -- repository: https://github.com/PintorOD1997/Lab2_Models                                             -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

# Library import
import data as dt
import numpy as np
import pandas as pd 
import functions as ft

# OrderBook opening using data openOB function
data_ob = dt.openOB()

# Orderbook timestamp
ob_ts = list(data_ob.keys())

# Timestamp listing
l_ts = [pd.to_datetime(i_ts) for i_ts in ob_ts]


# MidPrice, using the metrics dataframe from the functions library
x,_,_ = ft.OB_metrics(data_ob)
midprice = x["Mid Price"]

# Martingale count, all scenarios

e1 = [midprice[i] == midprice[i+1] for i in range(len(midprice)-1)]
e2 = [midprice[i] != midprice[i+1] for i in range(len(midprice)-1)]

APT_dic = {"e1" : {"Amount" : sum(e1), "Ratio" : sum(e1)/len(midprice)}, 
            "e2" : {"Amount" : sum(e2), "Ratio" : sum(e2)/len(midprice)},
            "total" : len(midprice)-1 }

# Asset Pricing Theory, DataFrame results
APT_df = pd.DataFrame(APT_dic).T

### Second Experiment: Martingale evaluation of the Asset Pricing theory using minute segmented data
midprice = pd.DataFrame(midprice)
# Minute indexed dictionary, index is Hour + Minute, to avoid minute reprisal.
dic = {}
for index, row in midprice.iterrows():
    key = str(index.hour) + ":" + str(index.minute)
    value = row["Mid Price"]
    try:
        dic[key].append(value)
    except KeyError:
        dic[key] = [value]
# Martingale Evaluation of the segmented data
APT_exp2 = {}
for i in list(dic): # <- iteración sobre índices del diccionario
    e1 = sum([dic[i][i_t] == dic[i][i_t+1] for i_t in range(len(dic[i])-1)])
    e2 = sum([dic[i][i_t] != dic[i][i_t+1] for i_t in range(len(dic[i])-1)])
    APT_exp2[i] = (
        {"e1" :{"Amount" :  e1, "Ratio" : e1/(len(dic[i])-1)}, 
         "e2" :{"Amount" :  e2, "Ratio" : e2/(len(dic[i])-1)},
         "total" : len(dic[i])-1
         }
        )
  
# Experiment 2 results, for each minute, as DataFrame
APT_minute_df = pd.DataFrame(data = {
    "e1": [APT_exp2[i]["e1"]["Amount"] for i in list(APT_exp2)],
    "e2": [APT_exp2[i]["e2"]["Amount"] for i in list(APT_exp2)],
    "Total": [APT_exp2[i]["total"] for i in list(APT_exp2)],
    "Ratio e1": [APT_exp2[i]["e1"]["Ratio"] for i in list(APT_exp2)],
    "Ratio e2": [APT_exp2[i]["e2"]["Ratio"] for i in list(APT_exp2)]
}, index = list(dic))

# Experiment 2 results, Ratio mean and total trades
APT_min_results_df = pd.DataFrame(data = {
    "e1 Ratio Mean" : np.array(APT_minute_df["Ratio e1"]).mean(),
    "e2 Ratio Mean" : np.array(APT_minute_df["Ratio e2"]).mean(),
    "Total Trades" : np.array(APT_minute_df["Total"]).sum()
},index = range(1))



###################################################################################
# Weighted Midprice Experiments
x,_,_ = ft.OB_metrics(data_ob)
Wmidprice = x["Weighted MidPrice (Ask)"]
e1 = [Wmidprice[i] == Wmidprice[i+1] for i in range(len(Wmidprice)-1)]
e2 = [Wmidprice[i] != Wmidprice[i+1] for i in range(len(Wmidprice)-1)] # puede ser definido por antonomasia
Wmetricas = {"e1" : {"Amount" : sum(e1), "Ratio" : sum(e1)/len(Wmidprice)}, 
            "e2" : {"Amount" : sum(e2), "Ratio" : sum(e2)/len(Wmidprice)},
            "total" : len(Wmidprice)-1 }
APT_df = pd.DataFrame(Wmetricas).T
Wmidprice = pd.DataFrame(Wmidprice)
Wdic = {}
for index, row in Wmidprice.iterrows():
    key = str(index.hour) + ":" + str(index.minute)
    value = row["Weighted MidPrice (Ask)"]
    try:
        Wdic[key].append(value)
    except KeyError:
        Wdic[key] = [value]
WAPT_exp2 = {}
for i in list(dic):
    e1 = sum([dic[i][i_t] == dic[i][i_t+1] for i_t in range(len(dic[i])-1)])
    e2 = sum([dic[i][i_t] != dic[i][i_t+1] for i_t in range(len(dic[i])-1)])
    WAPT_exp2[i] = (
        {"e1" :{"Amount" :  e1, "Ratio" : e1/(len(dic[i])-1)}, 
         "e2" :{"Amount" :  e2, "Ratio" : e2/(len(dic[i])-1)},
         "total" : len(dic[i])-1
         }
        )
WAPT_minute_df = pd.DataFrame(data = {
    "e1": [WAPT_exp2[i]["e1"]["Amount"] for i in list(WAPT_exp2)],
    "e2": [WAPT_exp2[i]["e2"]["Amount"] for i in list(WAPT_exp2)],
    "Total": [WAPT_exp2[i]["total"] for i in list(WAPT_exp2)],
    "Ratio e1": [WAPT_exp2[i]["e1"]["Ratio"] for i in list(WAPT_exp2)],
    "Ratio e2": [WAPT_exp2[i]["e2"]["Ratio"] for i in list(WAPT_exp2)]
}, index = list(dic))
WAPT_min_results_df = pd.DataFrame(data = {
    "e1 Ratio Mean" : np.array(WAPT_minute_df["Ratio e1"]).mean(),
    "e2 Ratio Mean" : np.array(WAPT_minute_df["Ratio e2"]).mean(),
    "Total Trades" : np.array(WAPT_minute_df["Total"]).sum()
})



# Modelo 2

