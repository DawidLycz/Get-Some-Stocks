from typing import Any
import csv
import json
from io import BytesIO
import base64
import random

import matplotlib.pyplot as plt
import yfinance as yf
from pandas import DataFrame

from django.views import generic
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Market, Ticker
from .forms import CSVUploadForm
from .trade_logic import *


STRATEGY_DESCRIPTION_FILE = r"getstocks/getstocksapp/static/getstocksapp/strategy_descriptions.json"

with open(STRATEGY_DESCRIPTION_FILE, "r") as stream:
    strategies_info = json.load(stream)


def create_chart(data: DataFrame, ticker: Ticker, period: str = "1y") -> str:
    
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data["Close"], label="Open price", color="gold")

    plt.title(f'{ticker} stock price for last {period}.', color='gold')
    plt.xlabel('DATE')
    plt.ylabel(ticker.currency)

    plt.grid(visible=True, color='gold', linewidth=0.2)

    plt.gca().xaxis.label.set_color('#ff7c11')
    plt.gca().yaxis.label.set_color('#ff7c11')
    
    plt.gca().spines['left'].set_color('#ff7c11') 
    plt.gca().spines['bottom'].set_color('#ff7c11') 
    plt.gca().spines['right'].set_color('none')
    plt.gca().spines['top'].set_color('none')
    
    plt.tick_params(axis='x', colors='gold')
    plt.tick_params(axis='y', colors='gold')

    for axis in ['top','bottom','left','right']:
        plt.gca().spines[axis].set_linewidth(3.5)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', transparent = True)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    buffer.close() 

    return image_base64


class IndexView(generic.TemplateView):
    
    template_name = "getstocksapp/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        ticker_list = Ticker.objects.all().order_by('-capitalization')[:20]
        ticker_dict_one = {ticker.ticker_name : ticker.company_name for ticker in ticker_list[:10]}
        ticker_dict_two = {ticker.ticker_name : ticker.company_name for ticker in ticker_list[10:]}
        ticker_dict_full = {**ticker_dict_one, **ticker_dict_two}
        clicked_ticker = self.request.GET.get('ticker_click')
        if not clicked_ticker:
            clicked_ticker = random.choice(list(ticker_dict_full.keys()))
        data = get_stock_data(clicked_ticker, reverse=True)
        markets = Market.objects.all()
        context["markets"] = markets
        context['data'] = data
        context['tickers_one'] = ticker_dict_one
        context['tickers_two'] = ticker_dict_two
        context['ticker'] = clicked_ticker
        context['company_name'] = ticker_dict_full[clicked_ticker]
        return context


class MarketReview(generic.DetailView):
    model = Market
    template = "getstocksapp/market_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        market = self.get_object()
        tickers = Ticker.objects.filter(origin_market=market)
        tickers = Ticker.objects.filter(data_fetched=True)
        sort_by = self.request.GET.get('sort_by')
        if not sort_by:
            sort_by = 'company_name'
        tickers = tickers.order_by(sort_by)
        context['related_tickers'] = tickers
        return context


class TickerReview(generic.DetailView):
    model = Ticker
    template = "getstocksapp/ticker_detail.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        ticker = self.get_object()
        period = "1y"
        data = get_stock_data(ticker=ticker.ticker_name, period=period)
        signals_smas = analyze_by_single_moving_average_strategy(data)
        signals_dmas = analyze_by_double_moving_averages_strategy(data)
        signals_rsis = analyze_by_rsi_strategy(data)
        signals_mrs = analyze_by_mean_reversion_strategy(data)
        
        context['current_price'] = data.iloc[-1]['Close']
        context['chart'] = create_chart(data, ticker, period)
        context['advice_single_moving_average'] = advice_move(signals_smas)
        context['advice_double_moving_average'] = advice_move(signals_dmas)
        context['advice_rsi'] = advice_move(signals_rsis)
        context['advice_mean_reversion'] = advice_move(signals_mrs)
        context['info_single_moving_average'] = strategies_info["single_moving_average"]
        context['info_double_moving_average'] = strategies_info["double_moving_average"]
        context['info_rsi'] = strategies_info["rsi"]
        context['info_mean_reversion'] = strategies_info["mean_reversion"]
        return context


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


class AboutUs(generic.TemplateView):
    
    template_name = "getstocksapp/about_us.html"


class Services(generic.TemplateView):

    template_name = "getstocksapp/services.html"


class Contact(generic.TemplateView):

    template_name = "getstocksapp/contact.html"
    