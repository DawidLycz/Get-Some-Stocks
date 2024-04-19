from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .data_downloaders.alphavantage_data import get_ticker_info_obj
from django.utils import timezone
from pandas import DataFrame


NO_DATA = ["No data", "None", "Not available", "Unknown", "N/A", "-", "NaN"]


class Market(models.Model):
    name = models.CharField(max_length=200)
    logo_img = models.ImageField(upload_to='market_logos/', blank=True, null=True)
    description = models.TextField(default='', blank=True)
    website = models.URLField(default='', blank=True)


    def __str__(self) -> str:
        return self.name


class Ticker(models.Model):
    ticker_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=255, default=NO_DATA[0])
    company_description = models.TextField(default='', blank=True)
    currency = models.CharField(max_length=255, default=NO_DATA[0])
    sector = models.CharField(max_length=255, default=NO_DATA[0])
    industry = models.CharField(max_length=255, default=NO_DATA[0])
    exchange = models.CharField(max_length=255, default=NO_DATA[0])
    address = models.CharField(max_length=255, default=NO_DATA[0])
    capitalization = models.BigIntegerField(default=0)
    origin_market = models.ForeignKey(Market, related_name='tickers', on_delete=models.CASCADE)
    data_fetched = models.BooleanField(default=False)
    full_data = models.BooleanField(default=False)
    for_display = models.BooleanField(default=False)


    class Meta:
        unique_together = ('ticker_name', 'origin_market')


    def __str__(self) -> str:
        return self.ticker_name

    def __repr__(self) -> str:
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
        self.full_data = True
        for value in self.__dict__.values():
            if value in NO_DATA:
                self.full_data = False
        self.save()
    

    def set_for_display(self):
        self.for_display = True
        self.save()


class Advisor(models.Model):
    name = models.CharField(max_length=200, default="Unknown")
    image = models.ImageField(upload_to='advisors_images/', blank=True, null=True)
    description = models.TextField(default='', blank=True)
    code = models.TextField(default='', blank=True)

    def __str__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name
    
    def get_dataframe(self, data, **kwargs) -> DataFrame:
        global_vars, local_vars = {}, {'data': data, 'kwargs': kwargs}
        exec(self.code, global_vars, local_vars)
        return local_vars.get('df')
    
    def get_advice(self, data, ticks=3, **kwargs) -> str:
        global_vars, local_vars = {}, {'data': data, 'kwargs': kwargs}
        exec(self.code, global_vars, local_vars)
        df = local_vars.get('df')
        try:
            last_few_signals = df.iloc[-ticks:]['signal']
        except:
            return "CAN'T UNDERSTAND DATA"
        average = round(last_few_signals.mean(), 2)
        if average >= 1.0:
            return "BUY"
        elif average <= -1.0:
            return "SELL"
        else:
            return "STAND BY"


 

class Wallet(models.Model):
    owner = models.ForeignKey(User, related_name='wallets', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    guests = models.ManyToManyField(User, related_name='guest_wallets', blank=True)


    def __str__(self) -> str:
        return self.name
    
                
@receiver(pre_save, sender=Wallet)
def wallet_pre_save(sender, instance, **kwargs):
    if not instance.name:
        instance.name = f"{instance.owner.username}_wallet"


class WalletRecord(models.Model):
    name = models.CharField(max_length=200, blank=True)
    wallet = models.ForeignKey(Wallet, related_name='records',  on_delete=models.CASCADE)
    ticker = models.ForeignKey(Ticker, related_name='wallet_records', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    creation_time = models.DateTimeField(default=timezone.now)
    init_price = models.FloatField(default=0.0)


    def __str__(self) -> str:
        return self.name


@receiver(pre_save, sender=WalletRecord)
def wallet_pre_save(sender, instance, **kwargs):
    if not instance.name:
        instance.name = f"{instance.ticker.company_name}"
