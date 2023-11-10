from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.fundamentaldata import FundamentalData
import yfinance as yf
import pandas as pd


import yfinance as yf
import pandas as pd

def show_stock_data(ticker: str):
    stock_data = yf.Ticker(ticker)
    data = stock_data.history(period="1y")
    data["Growth"] = data["Open"] - data["Close"]
    data = data.iterrows()
    return data

ticker = "AAIN"

data = show_stock_data(ticker)
print (type(data))









  


