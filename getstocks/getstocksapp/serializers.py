from django.contrib.auth.models import User
from rest_framework import serializers
from getstocksapp.models import Market, Ticker, Wallet, WalletRecord
from django.urls import reverse


class TickerSerializer(serializers.HyperlinkedModelSerializer):
    origin_market = serializers.HyperlinkedRelatedField(view_name='getstocksapp:api-market-detail', read_only=True)
    financial_data = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='getstocksapp:api-ticker-detail')

    class Meta:
        model = Ticker
        fields = ['url', 'origin_market', 'financial_data', 'id', 'ticker_name', 'company_name', 'currency', 'sector', 'industry', 'exchange', 'address', 'capitalization']
    
    def get_financial_data(self, obj):
        return self.context['request'].build_absolute_uri(reverse('getstocksapp:api-ticker-financial-info', args=[obj.pk]))

class MarketSerializer(serializers.HyperlinkedModelSerializer):
    tickers = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='getstocksapp:api-market-detail')

    class Meta:
        model = Market
        fields = ['url', 'id', 'name', 'description', 'website', 'tickers']

    def get_tickers(self, obj):
        tickers_queryset = obj.tickers.filter(for_display=True)
        return {
            ticker.ticker_name: self.context['request'].build_absolute_uri(reverse('getstocksapp:api-ticker-detail', args=[ticker.pk])) 
            for ticker in tickers_queryset
            }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    wallets = serializers.SerializerMethodField()
    guest_wallets = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='getstocksapp:api-user-detail')

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'wallets', 'guest_wallets',]

    def get_wallets(self, obj):
        wallets_queryset = obj.wallets.all()
        return {wallet.name: self.context['request'].build_absolute_uri(reverse('getstocksapp:api-wallet-detail', args=[wallet.pk])) for wallet in wallets_queryset}
    
    def get_guest_wallets(self, obj):
        wallets_queryset = obj.guest_wallets.all()
        return {wallet.name: self.context['request'].build_absolute_uri(reverse('getstocksapp:api-wallet-detail', args=[wallet.pk])) for wallet in wallets_queryset}


class WalletSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SerializerMethodField()
    guests = serializers.SerializerMethodField()
    records = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='getstocksapp:api-wallet-detail')
    
    class Meta:
        model = Wallet
        fields = ['url', 'id', 'name', 'owner', 'guests', 'records']
    
    def get_records(self, obj):
        records_queryset = obj.records.all()
        return {record.name: self.context['request'].build_absolute_uri(reverse('getstocksapp:api-wallet-record-detail', args=[record.pk])) for record in records_queryset}
    
    def get_owner(self,obj):
        owner_user = obj.owner
        return f"{owner_user.username} : {self.context['request'].build_absolute_uri(reverse('getstocksapp:api-user-detail', args=[owner_user.pk]))}"

    def get_guests(self, obj):
        guests_queryset = obj.guests.all()
        return {guest.username: self.context['request'].build_absolute_uri(reverse('getstocksapp:api-user-detail', args=[guest.pk])) for guest in guests_queryset}
 

class WalletRecordSerializer(serializers.HyperlinkedModelSerializer):
    wallet = serializers.SerializerMethodField()
    ticker = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='getstocksapp:api-wallet-record-detail')

    class Meta:
        model = WalletRecord
        fields = ['url', 'id', 'wallet', 'name', 'ticker', 'quantity', 'creation_time', 'init_price']

    def get_wallet(self, obj):
        return f"{obj.wallet.name} : {self.context['request'].build_absolute_uri(reverse('getstocksapp:api-wallet-detail', args=[obj.wallet.pk]))}"
    
    def get_ticker(self, obj):
        return f"{obj.ticker.ticker_name} : {self.context['request'].build_absolute_uri(reverse('getstocksapp:api-wallet-detail', args=[obj.ticker.pk]))}"
  


