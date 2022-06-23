
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
import visualizations
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
g1_df,_ = ft.Model1_Exp_2(midprice)
_,g2_df,_ = ft.Model1_Exp_3(data_ob)
g3_df,_ = ft.Model2(pd.DataFrame(midprice),x)

g1 = visualizations.Model1_Stack_Bar_Graph(g1_df,
                                           ["e1","e2"],
                                           ["Martingale Succesful Forecast", "Martingale Unsuccesful Forecast"],
                                           "APT Model Results")
g2 = visualizations.Model1_Stack_Bar_Graph(g2_df,
                                           ["e1","e2"],
                                           ["Martingale Succesful Forecast", "Martingale Unsuccesful Forecast"],
                                           "APT, Volume-Weighted Mid Prices")
g3 = visualizations.Model2_price_timeseries(
    g3_df,
    ["Bid","Mid Price","Ask"],
    ["Observed Bid","Mid Price","Observed Ask"],
    "Observed Spread"
)
g4 = visualizations.Model2_price_timeseries(
    g3_df,
    ["Model Bid","Mid Price","Model Ask"],
    ["Theoretical Bid","Mid Price","Theoretical Ask"],
    "Theoretical Spread"
)


