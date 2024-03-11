from django.contrib.auth.models import User
from rest_framework import serializers
from getstocksapp.models import Market, Ticker, Wallet
from django.urls import reverse


class TickerSerializer(serializers.HyperlinkedModelSerializer):
    origin_market = serializers.HyperlinkedRelatedField(view_name='getstocksapp:market-detail', read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='getstocksapp:ticker-detail')

    class Meta:
        model = Ticker
        fields = ['url', 'origin_market', 'id', 'ticker_name', 'company_name', 'currency', 'sector', 'industry', 'exchange', 'address', 'capitalization']


class MarketSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='getstocksapp:market-detail')
    tickers = serializers.SerializerMethodField()

    class Meta:
        model = Market
        fields = ['url', 'id', 'name', 'description', 'website', 'tickers']

    def get_tickers(self, obj):
        tickers_queryset = obj.tickers.filter(for_display=True)
        tickers_urls = {ticker.ticker_name: self.context['request'].build_absolute_uri(reverse('getstocksapp:ticker-detail', args=[ticker.pk])) for ticker in tickers_queryset}
        return tickers_urls

