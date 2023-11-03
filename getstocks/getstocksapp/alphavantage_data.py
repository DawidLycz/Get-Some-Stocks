from alpha_vantage.fundamentaldata import FundamentalData

api_key = '4KL6FXFAI196YG5S'

fd = FundamentalData(key=api_key)

class TickerInfo:
    def __init__(
        self,
        ticker: str,
        company_name: str="No data",
        description: str="No data",
        currency: str="No data",
        country: str="No data",
        sector: str="No data",
        industry: str="No data",
        exchange: str="No data",
        address: str="No data",
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
        try:
            api_info, meta_data = fd.get_company_overview(symbol=self.ticker)
            if api_info["Name"]:
                self.company_name = api_info["Name"]
            if api_info["Description"]:
                self.description = short_text(api_info["Description"])
            if api_info["Currency"]:
                self.currency = api_info["Currency"]
            if api_info["Country"]:
                self.country = api_info["Country"]
            if api_info["Sector"]:
                self.sector = api_info["Sector"]
            if api_info["Industry"]:
                self.industry = api_info["Industry"]
            if api_info["Industry"]:
                self.industry = api_info["Industry"]
            if api_info["Exchange"]:
                self.exchange = api_info["Exchange"]
            if api_info["Address"]:
                self.address = api_info["Address"]
        except ValueError:
            print ("Data can't be fetch")


    def get_particular_info(ticker: str, key: str) -> str:
        try:
            company_data, meta_data = fd.get_company_overview(symbol=ticker)
            return short_text(company_data[key])
        except KeyError:
            return "NO DATA"
        except ValueError:
            return "WRONG TICKER"


def get_ticker_info_obj(ticker: str) -> TickerInfo:
    obj = TickerInfo(ticker=ticker)
    obj.get_all_info()
    return obj


def short_text(text: str, max_lenght: int = 255) -> str:
    sentences = text.split(". ")
    new_text = ""
    total_lenght = 0
    for sentence in sentences:
        sentence += ". "
        if total_lenght + len(sentence) <= max_lenght:
            total_lenght += len(sentence)
            new_text += sentence
        else:
            break
    return new_text


