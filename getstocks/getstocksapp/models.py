from django.db import models
from .alphavantage_data import get_ticker_info_obj

class Market(models.Model):
    name = models.CharField(max_length=200)
    logo_path = models.CharField(max_length=200, default="BLANKFLAG.png")
    logo_img = models.ImageField(upload_to='market_logos/', blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Ticker(models.Model):
    ticker_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=255, default="No data")
    company_description = models.CharField(max_length=255, default="No data")
    currency = models.CharField(max_length=255, default="No data")
    sector = models.CharField(max_length=255, default="No data")
    industry = models.CharField(max_length=255, default="No data")
    exchange = models.CharField(max_length=255, default="No data")
    address = models.CharField(max_length=255, default="No data")
    origin_market = models.ForeignKey(Market, on_delete=models.CASCADE)
    data_fetched = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.ticker_name


    def download_data(self, *args, **kwargs):
        if not self.data_fetched:
            ticker_info = get_ticker_info_obj(self.ticker_name)
            self.company_name = ticker_info.company_name
            self.company_description = ticker_info.description
            self.currency = ticker_info.currency
            self.sector = ticker_info.sector
            self.industry = ticker_info.industry
            self.exchange = ticker_info.exchange
            self.address = ticker_info.address
            self.data_fetched= True
        super().save(*args, **kwargs)