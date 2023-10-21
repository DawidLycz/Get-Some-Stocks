import yfinance as yf

# Lista tickerów spółek składających się na S&P 500
sp500_components = ["AAPL", "MSFT", "ALE"]  # Tutaj wstaw listę tickerów spółek
# us_tickers = [
#     "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JPM", "V", "PYPL", "NKE",
#     "DIS", "NVDA", "MRK", "PFE", "CSCO", "KO", "IBM", "ORCL", "VZ",
#     "T", "INTC", "WMT", "HD", "UNH", "PG", "CRM", "ADBE", "PEP", "NFLX",
#     "MCD", "CMCSA", "XOM", "BA", "CVX", "GS", "CAT", "GE", "GM", "F",
#     "C", "BAC", "AIG", "AAL", "DAL", "UAL", "LUV", "AMAT", "TSM", "SPY"
# ]
# uk_tickers = [
#     "BP", "HSBA", "RDSA", "ULVR", "RDSB", "GSK", "BARC", "AZN", "VOD", "LLOY",
#     "BATS", "RIO", "RBS", "BHP", "DGE", "BDEV", "AV", "LAND", "SSE", "REL",
#     "CPG", "DCC", "RR", "BT-A", "III", "NXT", "TSCO", "MKS", "JD", "GVC",
#     "RTO", "SMIN", "PRU", "MRW", "EZJ", "CNA", "EXPN", "CCL", "MGGT", "LGEN", "DLG",
#     "SMT", "BKG", "IHG", "RSA", "STJ", "STAN", "KGF", "CCH"
# ]


# # Pobieranie danych akcji dla tych spółek
# data = yf.download(uk_tickers, period="1d")  # Pobiera cenę na dzień

# # Wyświetlenie danych
# print(data["Adj Close"])


import yfinance as yf

# Podaj symbol (ticker) firmy
symbol = "GOOGL"  # Przykład dla firmy Apple Inc.

# Uzyskaj informacje o firmie
company_info = yf.Ticker(symbol).info

# Wyświetl informacje o firmie
print("Nazwa firmy:", company_info.get("longName"))
print("Branża:", company_info.get("industry"))
print("Siedziba:", company_info.get("country"))
print("Opis firmy:", company_info.get("longBusinessSummary"))
