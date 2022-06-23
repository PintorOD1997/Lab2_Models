
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Lab 2: Models                                                                              -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: PintorOD1997                                                                                -- #
# -- license: GNU General Public License v3.0                                                            -- #
# -- repository: https://github.com/PintorOD1997/Lab2_Models                                             -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import pandas as pd 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.keys()
from pyparsing import col

def Model1_Stack_Bar_Graph(results: pd.DataFrame = None,columns: list = None, varnames: list = None, tit : str = None) -> True:
    """
    Model 1 Stack Bar Graph
    This function graphs in a stacked bar graph manner the results of the APT model

    Parameters
    ----------
    results (pd.DataFrame) : DataFrame containing the results for the model on each minute
    of the data
    columns (list) : List containing the columns to be displayed in the graph,
    in the order to be displayed
    varnames (list) : Variable names 
    tit (str) : Graph Title

    Returns
    -------
    fig : Plotly Graph containing the results

    """
    fig = go.Figure(
        data=[
            go.Bar(
                x = np.arange(0,61),
                y = results[columns[0]],
                name = varnames[0],
                text = results[columns[0]],
                offset=0
            ),
            go.Bar(
                x = np.arange(0,61),
                y = results[columns[1]],
                name = varnames[1],
                text = results[columns[1]],
                offset = 0,
                base = results[columns[0]]
            )
        ]
    )
    fig.update_layout(
        xaxis_title = "Minute",
        yaxis_title = "Trades",
        legend_title = "Martingale forecast result",
        title = tit
    )
    return fig

def Model2_price_timeseries(results: pd.DataFrame = None, cols : list = None, varnames : list = None, tit : str = None) -> True:
    """
    Model 2 Price Timeseries Scatterplot
    This function graphs using multiple scatterplots the results of the Roll model
    
    Parameters
    ----------
    results (pd.DataFrame) : Dataframe containing the price data to be graphed.
    cols (list) : list of columns to be graphed
    varnames (list) : List of variable names to be used on the graph
    tit (str) : Graph title
    Returns
    -------
    fig : Plotly figure containing the timeseries scatterplot of the provided data

    """
    fig = go.Figure(
        data = [
            go.Scatter(
                x = results.index,
                y = results[cols[0]],
                name = varnames[0]                
            ),
            go.Scatter(
                x = results.index,
                y = results[cols[1]],
                name = varnames[1]
            ),
            go.Scatter(
                x = results.index,
                y = results[cols[2]],
                name = varnames[2]
            )
        ]
    )
    fig.update_layout(
        xaxis_title = "Timestamp",
        yaxis_title = "Price",
        legend_title = "Price category",
        title = tit
    )
    return fig