from django.db import models
from .data_downloaders.alphavantage_data import get_ticker_info_obj

NO_DATA = "No data"

class Market(models.Model):
    name = models.CharField(max_length=200)
    logo_img = models.ImageField(upload_to='market_logos/', blank=True, null=True)
    description = models.TextField(default='', blank=True)
    website = models.URLField(default='', blank=True)


    def __str__(self) -> str:
        return self.name


class Ticker(models.Model):
    ticker_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=255, default=NO_DATA)
    company_description = models.TextField(default='', blank=True)
    currency = models.CharField(max_length=255, default=NO_DATA)
    sector = models.CharField(max_length=255, default=NO_DATA)
    industry = models.CharField(max_length=255, default=NO_DATA)
    exchange = models.CharField(max_length=255, default=NO_DATA)
    address = models.CharField(max_length=255, default=NO_DATA)
    capitalization = models.BigIntegerField(default=0)
    origin_market = models.ForeignKey(Market, on_delete=models.CASCADE)
    data_fetched = models.BooleanField(default=False)
    full_data = models.BooleanField(default=False)
    for_display = models.BooleanField(default=False)

    class Meta:
        unique_together = ('ticker_name', 'origin_market')

    def __str__(self) -> str:
        return self.ticker_name

    def download_data(self):
        if not self.data_fetched:
            ticker_info = get_ticker_info_obj(self.ticker_name)
            self.company_name = ticker_info.company_name
            self.company_description = ticker_info.description
            self.currency = ticker_info.currency
            self.sector = ticker_info.sector
            self.industry = ticker_info.industry
            self.exchange = ticker_info.exchange
            self.address = ticker_info.address
            if type(ticker_info.capitalization) is int:
                self.capitalization = ticker_info.capitalization
            else:
                self.capitalization = 0
            self.data_fetched= True
            self.save()

    def verify_full_data(self):
        d = NO_DATA
        self.full_data = all([
            self.company_name != d,
            self.company_description != d,
            self.currency != d,
            self.sector != d,
            self.industry != d,
            self.exchange != d,
            self.address != d,
            self.capitalization != 0,]
        )
        self.save()
    
    def set_for_display(self):
        self.for_display = True
        self.save()
    
    def do_desc(self):
        self.temp_description = self.company_description
        self.save()
    
    def do_desc2(self):
        self.company_description = self.temp_description
        self.save()