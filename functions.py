
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
