from typing import Any
from django.db import models
from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Market, Ticker
from .forms import CSVUploadForm
from django.http import JsonResponse
from django.views.generic.edit import FormView
from .forms import CSVUploadForm
from django.contrib import messages
from django.urls import reverse_lazy

import matplotlib.pyplot as plt
import io
import urllib
import base64
import yfinance as yf
import random
import csv

tickers = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "KO", "PG", "GE", "JNJ", "V", "JPM", "META",
    "TSLA", "AMZN", "NFLX", "GOOG", "INTC", "NVDA", "ADBE", "CSCO", "PYPL" 
]
ticker_list_one = tickers[:10]
ticker_list_two = tickers[10:]


def show_stock_data(ticker: str):
    stock_data = yf.Ticker(ticker)
    data = stock_data.history(period="1y")
    data["Growth"] = data["Close"] - data["Open"]
    data_list = list(data.iterrows())
    data = reversed(data_list)
    return data

class IndexView(generic.TemplateView):
    
    template_name = "getstocksapp/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        ticker = self.request.GET.get('ticker')
        if not ticker:
            ticker = random.choice(tickers)
        data = show_stock_data(ticker)
        markets = Market.objects.all()
        context["markets"] = markets
        context['data'] = data
        context['tickers'] = tickers
        context['tickers_one'] = ticker_list_one
        context['tickers_two'] = ticker_list_two
        context['ticker'] = ticker
        return context
    
class MarketReview(generic.DetailView):
    model = Market
    template = "getstocksapp/country_review.html"


class CSVUploadView(FormView):
    template_name = 'getstocksapp/upload_csv.html'
    form_class = CSVUploadForm 
    success_url = reverse_lazy('getstocksapp:home')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            ticker_name = form.cleaned_data.get('name_for_ticker_in_file')
            selected_market = form.cleaned_data.get('market')
            csv_file = request.FILES['csv_file']
            csv_data = self.process_csv(csv_file)
            market, created = Market.objects.get_or_create(name=selected_market)
            for row in csv_data:
                ticker = row[ticker_name]
                if not Ticker.objects.filter(ticker_name=ticker, origin_market=market).exists():
                    Ticker.objects.create(ticker_name=ticker, origin_market=market)
                    print (f"Ticker {ticker} has been created")
                else:
                    print (f"Ticker {ticker} already exists")
            messages.success(request, "Data has been imported from CSV file.")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def process_csv(self, file):
        csv_data = []

        try:
            reader = csv.DictReader(file.read().decode('utf-8').splitlines())
            for row in reader:
                csv_data.append(row)
        except Exception as e:
            print(f"Error processing CSV: {e}")

        return csv_data


