"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: LAB 1 MARKET MICROSTRUCTURE                                                      -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: PintorOD1997                                                                      -- #
# -- license: GNU General Public License v3.0                                               -- #
# -- repository: https://github.com/PintorOD1997/Lab1-Market-Microstructure-                                                                    -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""


import pandas as pd 
import json
from tkinter import filedialog as fd
from tkinter import *



def openOB():
    win = Tk()
    win.withdraw()
    filename = fd.askopenfilename()
    # Opening JSON file
    orderbooks_data = json.load(open(filename))
    ob_data = orderbooks_data["bitfinex"]
    # Drop None Keys
    ob_data = {i_key: i_value for i_key, i_value in ob_data.items() if i_value is not None}
    # Convert to dataframe and rearange columns
    ob_data = {i_ob: pd.DataFrame(ob_data[i_ob])[["bid_size","bid","ask","ask_size"]]
            if ob_data[i_ob] is not None else None for i_ob in list(ob_data.keys())}
    return ob_data



def openPT():
    win = Tk()
    win.withdraw()
    filename = fd.askopenfilename()
    pt_data = pd.read_csv(filename,header=0)
    pt_data.index = pd.to_datetime(pt_data["timestamp"])
    return pt_data
