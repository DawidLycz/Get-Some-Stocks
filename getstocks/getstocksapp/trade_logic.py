from pandas import DataFrame
import yfinance as yf

DEF_TICKER = "AAPL"

def analyze_by_single_moving_average_strategy(data: DataFrame, window: int=5) -> DataFrame:
    '''
    Function creates new column called signal.
    Calculates moving average of last (default 5) prices and based on that, forms new record to signal.
    If average price of last few days is lower that current day signal become 1.0, 
    but if it's higher, signal becomes -1.0
    '''
    signals = DataFrame(index=data.index)
    signals['signal'] = 0.0
    signals['rolling_mean'] = data['Close'].rolling(window=window).mean()
    signals.loc[data['Close'] > signals['rolling_mean'], 'signal'] = 1.0
    signals.loc[data['Close'] < signals['rolling_mean'], 'signal'] = -1.0
    data = signals['signal']
    return signals

def analyze_by_double_moving_averages_strategy(data: DataFrame, window1: int=20, window2: int=50) -> DataFrame:
    '''
    Function creates new column called signal.
    Calculates two moving averages (default 20 and 50 days) and compares them. 
    If average of shorter period is higher than other, signal becomes 1.0, else it becomes -1.0
    '''
    signals = DataFrame(index=data.index)
    signals['20_SMA'] = data['Close'].rolling(window=window1).mean()
    signals['50_SMA'] = data['Close'].rolling(window=window2).mean()
    signals['signal'] = 0
    signals.loc[signals['20_SMA'] > signals['50_SMA'], 'signal'] = 1.0
    signals.loc[signals['20_SMA'] < signals['50_SMA'], 'signal'] = -1.0

    return signals

def analyze_by_rsi_strategy(data: DataFrame, window: int=14, overbought_threshold: int=70, oversold_threshold: int=30) -> DataFrame:    
    '''
    Function creates new column called signal.
    RSI strategy calculates average gain and average loss for specified time period (default 14) 
    and based on that, forms RSI column. RSI is number beetween 0 and 100.
    Oversold and overbought trashold are specified in args but can be edited.
    If RSI is below overbought treshold, signal becomes -1.0.
    If RRI is above oversold treshold, signal becomes 1.0.
    '''
    signals = DataFrame(index=data.index)
    signals['Price Change'] = data['Close'].diff()
    signals['Positive Change'] = signals['Price Change'].apply(lambda x: x if x > 0 else 0)
    signals['Negative Change'] = signals['Price Change'].apply(lambda x: -x if x < 0 else 0)
    signals['Avg Gain'] = signals['Positive Change'].rolling(window=window).mean()
    signals['Avg Loss'] = signals['Negative Change'].rolling(window=window).mean()
    signals['RS'] = signals['Avg Gain'] / signals['Avg Loss']
    signals['RSI'] = 100 - (100 / (1 + signals['RS']))
    signals['signal'] = 0
    signals.loc[signals['RSI'] > overbought_threshold, 'signal'] = -1.0
    signals.loc[signals['RSI'] < oversold_threshold, 'signal'] = 1.0
    return signals

def analyze_by_mean_reversion_strategy(data: DataFrame, sell_multiplier: float=1.5, buy_multiplier: float=0.75):
    '''
    Function creates new column called signal.
    Function calculates average value of all records in "Close" column
    Based on that average, function forms sell, and buy tresholds by multipling it with args.
    If price is above sell treshold, signal becomes -1.0
    If price is below buy treshold, signal becomes 1.0
    '''
    signals = DataFrame(index=data.index)
    average_price = data['Close'].mean()
    sell_treshold = average_price * sell_multiplier
    buy_treshold = average_price * buy_multiplier
    signals['signal'] = 0
    signals.loc[data['Close'] > sell_treshold, 'signal'] = -1.0
    signals.loc[data['Close'] < buy_treshold, 'signal'] = 1.0
    return signals


def advice_move(signals: DataFrame, ticks: int=3) -> None:
    
    last_few_signals = signals.iloc[-ticks:]['signal']
    average = round(last_few_signals.mean(), 2)
    if average >= 1.0:
        return "BUY"
    elif average <= -1.0:
        return "SELL"
    else:
        return "STAND BY"

def get_stock_data(ticker: str, period: str="1y", reverse: bool=False) -> DataFrame:
    stock_data = yf.Ticker(ticker)
    data = stock_data.history(period=period)
    data["Growth"] = data["Close"] - data["Open"]
    if reverse:
        data_list = list(data.iterrows())
        data = reversed(data_list)
    return data


