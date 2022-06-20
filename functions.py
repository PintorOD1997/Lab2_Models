
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Lab 2: Models                                                                              -- #
# -- script: functions.py : python functions that are used in main                                       -- #
# -- author: PintorOD1997                                                                                -- #
# -- license: GNU General Public License v3.0                                                            -- #
# -- repository: https://github.com/PintorOD1997/Lab2_Models                                             -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import numpy as np
import pandas as pd
import pyflakes


def OB_metrics(data_ob: dict = None) -> True:
    """
    OrderBook Metrics
    This function obtains the main metrics for a given OrderBook.
    The metrics returned are:
    -1. Median of time between trades
    -2. Spread of price
    -3. Midprice of given timestamp
    -4. Number of price levels
    -5. Bid Volume
    -6. Ask Volume
    -7.Total Volume
    -8. Volume Imbalance
    -9. Ask Weighted Midprice
    -10. Bid Weighted Midprice
    -11. Volume-Weighted-Average Price
    - Top of the Book Bids
    - Top of the Book Asks

    Parameters
    ----------
    data_ob (dict) : Dictonary containing the OrderBook

    Returns
    -------
    metrics : DataFrame containing the metrics obtained from the OrderBook
    ob_m1 : Median of time between trades
    ob_m4 : Number of price levels in the OrderBook
    


    """
    ob_ts = list(data_ob.keys())
    l_ts = [pd.to_datetime(i_ts) for i_ts in ob_ts]
    # Median timedelta
    ob_m1 = np.median([l_ts[n_ts+1]-l_ts[n_ts] for n_ts in range(len(l_ts)-1)]).total_seconds()*1000
    # Spread
    ob_m2 = [data_ob[ob_ts[i]]["ask"][0]- data_ob[ob_ts[i]]["bid"][0] for i in range(len(ob_ts))]
    # MidPrice
    ob_m3 = [(data_ob[ob_ts[i]]["ask"][0]+ data_ob[ob_ts[i]]["bid"][0])*0.5 for i in range(len(ob_ts))]  
    # Price Levels
    ob_m4 = [data_ob[i_ts].shape[0] for i_ts in ob_ts]   
    # Bid Volume
    ob_m5 = [np.round(data_ob[i_ts]["bid_size"].sum(), 6) for i_ts in ob_ts]  
    # Ask Volume
    ob_m6 = [np.round(data_ob[i_ts]["ask_size"].sum(), 6) for i_ts in ob_ts] 
    # Total Volume
    ob_m7 = [np.round(data_ob[i_ts]['bid_size'].sum() + data_ob[i_ts]['ask_size'].sum() , 6) for i_ts in ob_ts]  
    # Orderbook Imbalance
    ob_m8 = [ob_m5[i_ts]/ob_m7[i_ts] for i_ts in range(len(ob_ts))]
    #  Weighted-Midprice (Ask): ((Bid_Volume/ Bid_Volume + Ask Volume )) * ((bid_price[0] + ask_price[0])/2)
    ob_m9 = [ob_m8[i_ts]*ob_m3[i_ts] for i_ts in range(len(ob_ts))]
    # Weighted-MidPrice (Bid): ((Ask_Volume/ Bid_Volume + Ask Volume )*Bid_Price) + ((Bid_Volume/ Bid_Volume + Ask Volume )*Ask_Price)
    ob_m10 = [ (ob_m6[i_ts]/(ob_m5[i_ts] + ob_m6[i_ts]) * data_ob[ob_ts[i_ts]]['bid'][0]) + (ob_m8[i_ts]*(data_ob[ob_ts[i_ts]]['ask'][0])) for i_ts in range(len(ob_ts)) ]
    Bids_ToB = [data_ob[ob_ts[i]]['bid'][0] for i in range(len(ob_ts))]
    Asks_ToB = [data_ob[ob_ts[i]]['ask'][0] for i in range(len(ob_ts))]
    # VWAP (Volume-Weighted-Average Price)
    ob_m11 = [np.round((Bids_ToB[i]*ob_m5[i] + Asks_ToB[i]*ob_m6[i]) / (ob_m5[i]+ob_m6[i]),6) for i in range(len(ob_ts))]

    metrics = pd.DataFrame({
        "Spread" : ob_m2,
        "Mid Price" : ob_m3,
        "Bid Volume" : ob_m5,
        "Ask Volume" : ob_m6,
        "Total Volume" : ob_m7 ,
        "OrderBook Imbalance" : ob_m8,
        "Weighted MidPrice (Ask)" : ob_m9,
        "Weighted MidPrice (Bid)": ob_m10,
        "VWAP" : ob_m11,
        "Bids ToB" : Bids_ToB,
        "Asks ToB" : Asks_ToB
        
    })
    metrics.index = l_ts
    return metrics, ob_m1, ob_m4# Returns metrics dataframe, median of trades and no. of priceLevels

def Model1_Exp_1(midprice: pd.Series = None) -> True:
    """
    APT Experiment 1:
    APT model evaluation for ALL data in the OrderBooks.
    Utilizes the midprice as the fair price in order to evaluate the APT hypothesis
    (The best estimator for future prices is the current price)

    Parameters
    ----------
    midprice (Series) : TimeSeries containing the orderbook settled midprice
    for each timestamp

    Returns
    -------
    APT_df : DataFrame containing the results of the APT Model Evaluation 

    """
    # Martingale count, all scenarios

    e1 = [midprice[i] == midprice[i+1] for i in range(len(midprice)-1)]
    e2 = [midprice[i] != midprice[i+1] for i in range(len(midprice)-1)]

    APT_dic = {"e1" : {"Amount" : sum(e1), "Ratio" : sum(e1)/len(midprice)}, 
                "e2" : {"Amount" : sum(e2), "Ratio" : sum(e2)/len(midprice)},
                "total" : len(midprice)-1 }
    # Asset Pricing Theory, DataFrame results
    APT_df = pd.DataFrame(APT_dic).T
    return APT_df



### Second Experiment: Martingale evaluation of the Asset Pricing theory using minute segmented data

def Model1_Exp_2(midprice: pd.Series = None) -> True:
    """
    APT Second Experiment:
    Now, segmenting all data by Minute (The input orderbook should contain orderbooks data 
    by day, hour, and minute), finds the martingale evaluation of the orderbook mid prices 
    settlements fot each minute.

    Parameters
    ----------
    midprice (str) : Parameter Description

    Returns
    -------
    APT_minute_df : DataFrame containing the Model 1 Martingale results for each timestamp
    APT_min_results_df : DataFrame containing the previous results summarized in the mean results
    for each Ratio.

    """
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
    return APT_minute_df,APT_min_results_df



###################################################################################
# Weighted Midprice Experiments


def Model1_Exp_3(data_ob: dict = None) -> True:
    """
    APT model, using Volume-Weighted Mid Prices
    This function obtains the previous 2 experiments, now using
    the Volume-Weighted Mid Prices instead of the Mid Prices of the orderbooks.

    Parameters
    ----------
    data_ob (dict) : Dictionary containing the Orderbook. It is used in order to 
    obtain the VWMP and extract other relevant data.

    Returns
    -------
    WAPT_df : Experiment 1
    WAPT_minute_df : Experiment 2, all data
    WAPT_min_results_df : Experiment 2, results summarization
    """
    x,_,_ = OB_metrics(data_ob)
    Wmidprice = x["Weighted MidPrice (Ask)"]
    e1 = [Wmidprice[i] == Wmidprice[i+1] for i in range(len(Wmidprice)-1)]
    e2 = [Wmidprice[i] != Wmidprice[i+1] for i in range(len(Wmidprice)-1)] # puede ser definido por antonomasia
    Wmetricas = {"e1" : {"Amount" : sum(e1), "Ratio" : sum(e1)/len(Wmidprice)}, 
                "e2" : {"Amount" : sum(e2), "Ratio" : sum(e2)/len(Wmidprice)},
                "total" : len(Wmidprice)-1 }
    WAPT_df = pd.DataFrame(Wmetricas).T
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
    for i in list(Wdic):
        e1 = sum([Wdic[i][i_t] == Wdic[i][i_t+1] for i_t in range(len(Wdic[i])-1)])
        e2 = sum([Wdic[i][i_t] != Wdic[i][i_t+1] for i_t in range(len(Wdic[i])-1)])
        WAPT_exp2[i] = (
            {"e1" :{"Amount" :  e1, "Ratio" : e1/(len(Wdic[i])-1)}, 
            "e2" :{"Amount" :  e2, "Ratio" : e2/(len(Wdic[i])-1)},
            "total" : len(Wdic[i])-1
            }
            )
    WAPT_minute_df = pd.DataFrame(data = {
        "e1": [WAPT_exp2[i]["e1"]["Amount"] for i in list(WAPT_exp2)],
        "e2": [WAPT_exp2[i]["e2"]["Amount"] for i in list(WAPT_exp2)],
        "Total": [WAPT_exp2[i]["total"] for i in list(WAPT_exp2)],
        "Ratio e1": [WAPT_exp2[i]["e1"]["Ratio"] for i in list(WAPT_exp2)],
        "Ratio e2": [WAPT_exp2[i]["e2"]["Ratio"] for i in list(WAPT_exp2)]
    }, index = list(WAPT_exp2))
    WAPT_min_results_df = pd.DataFrame(data = {
        "e1 Ratio Mean" : np.array(WAPT_minute_df["Ratio e1"]).mean(),
        "e2 Ratio Mean" : np.array(WAPT_minute_df["Ratio e2"]).mean(),
        "Total Trades" : np.array(WAPT_minute_df["Total"]).sum()
    }, index = range(1))
    return WAPT_df,WAPT_minute_df,WAPT_min_results_df




def Model2(midprice: pd.DataFrame = None,x: pd.DataFrame = None) -> True:
    """
    Model #2: The Roll Model
    This function finds if the premise of the model can be confirmed usin data:
    The Optimal Spread of The Orderbooks can be estimated using the autocovariance of 
    the price differences. 
    This function, calculates said autocovariance, estimates the optimal spread,
    and summarizes the results in a DataFrame containing Each midprice, its spread, and the
    calculated spread (also compares the bid and ask data).

    Parameters
    ----------
    midprice (DataFrame) : DataFrame containing the midprice info.
    x (DataFrame) : Dataframe containing the Spread info.

    Returns
    -------
    model2_df : Dataframe containing, for each timestamp, The modeled spread, the actual spread
    the midprice, the bid, ask, modeled bid and modeled ask.
    roll_df_stats : 
    """
    # C constant
    # MidPrice Delta
    
    dP_t = midprice["Mid Price"].diff(1) # Present price changes
    dP_t_1 = midprice["Mid Price"].shift(1).diff(1) # 1 instant in time shifted mid prices
    # We now need to find this prices Covariance
    cov = pd.DataFrame({
        "dP_t" : dP_t, "dP_t_1" : dP_t_1
    }).cov().iloc[1,0]
    # Constant C is Sqrt(-cov)
    C = np.sqrt(-cov)
    spread = 2*C
    model2_df = pd.DataFrame({
        "Model Spread" : spread,
        "Spread" : x["Spread"],
        "Mid Price" : midprice["Mid Price"],
        "Bid": midprice["Mid Price"] - x["Spread"],
        "Ask" : midprice["Mid Price"] + x["Spread"],
        "Model Bid" : midprice["Mid Price"] - C,
        "Model Ask" : midprice["Mid Price"] + C        
    },index = x.index)
    
   
    # Modelling spread as a Random Variable and comparing it to the results obtained in Roll
    roll_df_stats = pd.DataFrame({
        "Spread Mean" : model2_df["Spread"].mean(),
        "Spread Variance" : model2_df["Spread"].var(),
        "Calculated Spread" : model2_df["Model Spread"][0]
    },index = range(1))
    roll_df_stats["Spread Mean Difference"] = roll_df_stats["Spread Mean"] - roll_df_stats["Calculated Spread"]
    
    return model2_df,roll_df_stats