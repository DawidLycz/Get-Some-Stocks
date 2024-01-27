import yfinance as yf
from pandas import DataFrame
import numpy as np

def get_stock_data(ticker: str, period: str="1y", reverse: bool=False) -> DataFrame:
    stock_data = yf.Ticker(ticker)
    data = stock_data.history(period=period)
    data["Growth"] = data["Close"] - data["Open"]
    if reverse:
        data_list = list(data.iterrows())
        data = reversed(data_list)
    return data


def get_prices_of_many_tickers(tickers: list[str]) -> list[float]:
    data = yf.download(tickers, start="2024-01-01")
    prices = []
    if len(set(tickers)) == 1:
        price = round(data['Adj Close'].iloc[-1], 2)
        if np.isnan(price):
            price = None
        return [price] * len(tickers)

    for ticker in tickers:            
        price = round(data['Adj Close'][ticker].iloc[-1], 2)
        if np.isnan(price):
            price = None
        prices.append(price)
    return prices

