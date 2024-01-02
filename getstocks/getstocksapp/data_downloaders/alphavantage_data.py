from alpha_vantage.fundamentaldata import FundamentalData
import logging
from django.conf import settings
from dataclasses import dataclass

# APLHAVANTAGE_API_KEY = '4KL6FXFAI196YG5S'

fd = FundamentalData(key=settings.APLHAVANTAGE_API_KEY)

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
                self.description = (api_info["Description"])
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
            return (company_data[key])
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

# symbol = "A5H24"

# api_info, meta_data = fd.get_company_overview(symbol)

# print (api_info)