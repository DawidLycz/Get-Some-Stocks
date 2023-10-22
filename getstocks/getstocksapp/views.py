from typing import Any
from django.db import models
from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Country, Ticker

import matplotlib.pyplot as plt
import io
import urllib
import base64
import yfinance as yf
import random

tickers = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "KO", "PG", "GE", "JNJ", "V", "JPM", "META",
    "TSLA", "AMZN", "NFLX", "GOOG", "INTC", "NVDA", "ADBE", "CSCO", "PYPL" 
]
ticker_list_one = tickers[:10]
ticker_list_two = tickers[10:]

api_key= '4KL6FXFAI196YG5S'

def show_stock_data(ticker: str):
    stock_data = yf.Ticker(ticker)
    historical_data = stock_data.history(period="1y") 
    return (historical_data)

class IndexView(generic.TemplateView):
    
    template_name = "getstocksapp/index.html"


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        ticker = self.request.GET.get('ticker')
        if not ticker:
            ticker = random.choice(tickers)
        print (ticker)
        data = show_stock_data(ticker)
        data_list = list(data.iterrows())
        data = reversed(data_list)
        countries = Country.objects.all()
        context["countries"] = countries
        context['data'] = data
        context['tickers'] = tickers
        context['tickers_one'] = ticker_list_one
        context['tickers_two'] = ticker_list_two
        context['ticker'] = ticker
        return context
    
class CountryReview(generic.DetailView):
    model = Country
    template = "getstocksapp/country_review.html"
    

    