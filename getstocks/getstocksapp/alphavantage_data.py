from alpha_vantage.fundamentaldata import FundamentalData

api_key = '4KL6FXFAI196YG5S'

fd = FundamentalData(key=api_key)

class TickerInfo:
    def __init__(
        self,
        ticker: str,
        company_name: str=None,
        description: str=None,
        currency: str=None,
        country: str=None,
        sector: str=None,
        industry: str=None,
        exchange: str=None,
        address: str=None,
    ):
        self.ticker = ticker
        self.company_name = company_name
        self.description = description
        self.currency = currency
        self.country = country
        self.sector = sector
        self.industry = industry
        self.exchange = exchange
        self.address = address
    
    def __str__(self):
        return self.ticker
    
    def __repr__(self):
        return f"{self.company_name}, {self.description}, {self.currency}, {self.country}, {self.sector}, {self.industry}, {self.exchange}, {self.address}"


    def get_all_info(self):
        api_info, meta_data = fd.get_company_overview(symbol=self.ticker)
        self.company_name = api_info["Name"]
        self.description = api_info["Description"]
        self.currency = api_info["Currency"]
        self.country = api_info["Country"]
        self.sector = api_info["Sector"]
        self.industry = api_info["Industry"]
        self.exchange = api_info["Exchange"]
        self.address = api_info["Address"]  


    def get_particular_info(ticker: str, key: str) -> str:
        try:
            company_data, meta_data = fd.get_company_overview(symbol=ticker)
            return company_data[key]
        except KeyError:
            return "NO DATA"
        except ValueError:
            return "WRONG TICKER"


def get_ticker_info_obj(ticker: str) -> TickerInfo:
    obj = TickerInfo(ticker=ticker)
    obj.get_all_info()
    return obj




