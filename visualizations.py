
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
import plotly.express as px


def Model1_Prices_Comparison(data: pd.DataFrame = None):
    """
    Model 1 Graphical Hypothesis Evaluation
    This function displays a graph on which the prices and the future prices are
    overlapped, in order for us to test the Model 1 hypothesis, which is:
    "The best estimator for the future price is the current price"

    Parameters
    ----------
    data (DataFrame) : 

    Returns
    -------
    plotly figure to be rendered
    
    """

    midpricesshift = data.iloc[1:]
    df = pd.DataFrame({
        "Mid Price" : data,
        "Mid Price t_1" : midpricesshift
    })
    fig = px.line(df)
    #fig.show()
    return fig
    
    
def Model1_graph_results_t1(data: pd.DataFrame = None) -> True:
    """
    Experiment 1 Graphical Results Type 1
    Returns Bar plot for the number of succesful predictions and unsuccesful 
    for the first experiment of the model

    Parameters
    ----------
    data (DataFrame) : Parameter Description

    Returns
    -------
    plotly figure to be rendered
    """
    fig = px.bar(data, x="Amount")
    #fig.show()
    return fig
    

def Model1_graph_results_t2(data: pd.DataFrame = None) -> True:
    """
    Experiment 1 Graphical Results Type 2
    Returns Histogram

    Parameters
    ----------
    data (DataFrame) : Parameter Description

    Returns
    -------
    plotly figure to be rendered
    """
    fig = px.histogram(data,x="Ratio e1")
    #fig.show()
    return fig

def Model1_graph_results_t3(data: pd.DataFrame = None) -> True:
    """
    Experiment 1 Graphical Results
    Returns Bar plot

    Parameters
    ----------
    data (DataFrame) : Parameter Description

    Returns
    -------
    plotly figure to be rendered
    """
    fig = px.bar(data.drop(columns=["Total Trades"]))
    #fig.show()
    return fig
    
def Model2_graph_results(data: pd.DataFrame = None) -> True:
    """
    Function Description here
    Plots Line plot comparing actual spread vs calculated spread and histogram showing
    the distribution of the spread.

    Parameters
    ----------
    data (DataFrame) : Parameter Description

    Returns
    -------
    plotly figure to be rendered

    """
    fig1 = px.line(data,y=data.columns[0:2])
    fig2 = px.histogram(data,x="Spread")
    return fig1,fig2
    #fig1.show()
    #fig2.show()