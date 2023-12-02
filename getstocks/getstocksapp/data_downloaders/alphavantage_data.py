from alpha_vantage.fundamentaldata import FundamentalData
import logging
# from getstocks.getstocks.settings import APLHAVANTAGE_API_KEY
from dataclasses import dataclass

APLHAVANTAGE_API_KEY = '4KL6FXFAI196YG5S'

fd = FundamentalData(key=APLHAVANTAGE_API_KEY)

logger = logging.getLogger(__name__)

@dataclass
class TickerInfo:
    ticker: str
    company_name: str="No data"
    description: str="No data"
    currency: str="No data"
    country: str="No data"
    sector: str="No data"
    industry: str="No data"
    exchange: str="No data"
    address: str="No data"
    capitalization : int=0

    def get_all_info(self):
        try:
            api_info, meta_data = fd.get_company_overview(symbol=self.ticker)
            self.company_name = api_info.get("Name", "No Data")
            if api_info["Description"] not in ["None.", "None", ""]:  
                self.description = short_text(api_info["Description"])
            else:
                self.description = "No data"
            self.currency = api_info.get("Currency", "No Data")
            self.country = api_info.get("Country", "No Data")
            self.sector = api_info.get("Sector", "No Data")
            self.industry = api_info.get("Industry", "No Data")
            self.exchange = api_info.get("Exchange", "No Data")
            self.address = api_info.get("Address", "No Data")
            if api_info["MarketCapitalization"]:
                try:
                    self.capitalization = int(api_info["MarketCapitalization"])
                except ValueError:
                    self.capitalization = 0
            else:
                self.capitalization = 0
            logger.info("Data fetched successfully")
        except ValueError:
            logger.warning("Data can't be fetch")

    def get_particular_info(ticker: str, key: str) -> str:

        try:
            company_data, meta_data = fd.get_company_overview(symbol=ticker)
            return short_text(company_data[key])
        except KeyError:
            logger.warning(f"Can't find '{key}' in api")
            return "No Data"
        except ValueError:
            logger.warning(f"Ticker: '{ticker}' is incorrect")
            return "No Data"


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


