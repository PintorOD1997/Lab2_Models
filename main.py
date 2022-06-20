
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

ft.Model1_Exp_1(midprice)
ft.Model1_Exp_2(midprice)
ft.Model1_Exp_3(data_ob)
ft.Model2(pd.DataFrame(midprice),x)
