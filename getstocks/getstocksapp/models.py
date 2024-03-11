from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .data_downloaders.alphavantage_data import get_ticker_info_obj
from django.utils import timezone


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
    origin_market = models.ForeignKey(Market, related_name='tickers', on_delete=models.CASCADE)
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


class Wallet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
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
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    creation_time = models.DateTimeField(default=timezone.now)
    init_price = models.FloatField(default=0.0)


    def __str__(self) -> str:
        return self.name


@receiver(pre_save, sender=WalletRecord)
def wallet_pre_save(sender, instance, **kwargs):
    if not instance.name:
        instance.name = f"{instance.ticker.company_name}"
