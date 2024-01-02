import yfinance as yf
from pandas import DataFrame

def get_stock_data(ticker: str, period: str="1y", reverse: bool=False) -> DataFrame:
    stock_data = yf.Ticker(ticker)
    data = stock_data.history(period=period)
    data["Growth"] = data["Close"] - data["Open"]
    if reverse:
        data_list = list(data.iterrows())
        data = reversed(data_list)
    return data


