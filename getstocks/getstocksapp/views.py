from typing import Any
import csv
import json
from io import BytesIO
import base64
import random

import matplotlib.pyplot as plt
import yfinance as yf
from pandas import DataFrame

from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy, reverse

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views import View

from .models import Market, Ticker
from .forms import CSVUploadForm, CustomUserCreationForm, CustomAuthenticationForm
from .trade_logic import *
from .data_downloaders.yfinance_data import get_stock_data



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

        ticker_list_one = ticker_list[:10]
        ticker_list_two = ticker_list[10:]
        clicked_ticker_id = self.request.GET.get('ticker_click')
        if not clicked_ticker_id:
            clicked_ticker = random.choice(ticker_list)
        else:
            clicked_ticker = get_object_or_404(Ticker, id=clicked_ticker_id)
        data = get_stock_data(clicked_ticker.ticker_name, reverse=True)
        markets = Market.objects.all()
        context["markets"] = markets
        context['data'] = data
        context['tickers_one'] = ticker_list_one
        context['tickers_two'] = ticker_list_two
        context['clicked_ticker'] = clicked_ticker
        context['current_user'] = self.request.user

        return context


class MarketReview(generic.DetailView):
    model = Market
    template = "getstocksapp/market_detail.html"

        
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        market = self.get_object()
        tickers = Ticker.objects.filter(origin_market=market, for_display=True)
        sorter = self.request.GET.get('sort_by')
        
        if not sorter:
            sorter = 'company_name'

        tickers = tickers.order_by(sorter)
        context['table_columns'] = [
            ('ticker_name', 'Ticker'), 
            ('company_name', 'Name'), 
            ('sector', 'Sector'), 
            ('industry', 'Industry'), 
            ('capitalization', 'Market Capitalization')
            ]
        context['related_tickers'] = tickers
        context['current_sorter'] = sorter
        return context
    

class TickerReview(generic.DetailView):
    model = Ticker
    template = "getstocksapp/ticker_detail.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        ticker = self.get_object()
        period = self.request.GET.get('period')
        if not period:
            period = "1y"
        data = get_stock_data(ticker=ticker.ticker_name, period=period)
        context["data_availble"] = not data.empty
        if not data.empty:
            signals_smas = analyze_by_single_moving_average_strategy(data)
            signals_dmas = analyze_by_double_moving_averages_strategy(data)
            signals_rsis = analyze_by_rsi_strategy(data)
            signals_mrs = analyze_by_mean_reversion_strategy(data)
            context['chart_periods'] = [
                (0, "All times", "max"),
                (10, "10 Years", "10y"), 
                (20, "5 Years", "5y"),
                (30, "2 Years", "2y"),
                (40, "1 Year", "1y"),
                (50, "6 Months", "6mo"),
                (60, "3 Months", "3mo"),
                (70, "1 Month", "1mo"),
                (80, "5 Days", "5d"),
                (90, "1 Day", "1d")
                ]

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


class AdvisorInfo(generic.TemplateView):

    template_name = "getstocksapp/advisor_info.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        context = super().get_context_data(**kwargs)
        advisor = self.request.GET.get('advisor')
        match advisor:
            case "Single_moving_average":
                advisor_info = strategies_info["single_moving_average"]
                advisor_image_url = "/static/getstocksapp/images/advisor_img1.png"
            case "Double_moving_average":
                advisor_info = strategies_info["double_moving_average"]
                advisor_image_url = "/static/getstocksapp/images/advisor_img2.png"
            case "RSI":
                advisor_info = strategies_info["rsi"]
                advisor_image_url = "/static/getstocksapp/images/advisor_img3.png"
            case "Mean_reversion":
                advisor_info = strategies_info["mean_reversion"]
                advisor_image_url = "/static/getstocksapp/images/advisor_img4.png"
            case _:
                advisor = "Unknown"
                advisor_info = "Unknown Advisor"
                advisor_image_url = "/static/getstocksapp/images/advisor_img1.png"
        
        context["title"] = advisor.replace("_", " ")
        context["advisor_info"] = advisor_info
        context["advisor_image_url"] = advisor_image_url
        return context


class RegistrationView(generic.TemplateView):
    template_name = 'getstocksapp/registration.html'

    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('getstocksapp:home') 
        return render(request, self.template_name, {'form': form})
    

class CustomLoginView(LoginView):
    template_name = 'getstocksapp/login.html'
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('getstocksapp:home')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.success_url

class LogoutConfirm(generic.TemplateView):
    template_name = 'getstocksapp/logout.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('getstocksapp:home')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            # Użytkownik jest teraz wylogowany, przekieruj na stronę główną
            return redirect(self.next_page)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
