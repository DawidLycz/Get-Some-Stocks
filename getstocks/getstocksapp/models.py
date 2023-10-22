from django.db import models
from .alphavantage_data import get_ticker_info_obj

class Country(models.Model):
    name = models.CharField(max_length=200)
    flag_img = models.CharField(max_length=200, default="BLANKFLAG.png")

    def save(self, *args, **kwargs):
        self.flag_img = f'getstocksapp/flag_images/{self.flag_img}'
        super().save(*args, **kwargs)

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
    origin_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    data_fetched = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.ticker_name


    def save(self, *args, **kwargs):
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