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
from django.views.generic.edit import FormView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from rest_framework import status, mixins, generics, permissions, renderers, viewsets, filters
from rest_framework import generics as drfgenerics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.parsers import JSONParser
from rest_framework.reverse import reverse as drf_reverse

from .models import Market, Ticker, Advisor, Wallet, WalletRecord
from .forms import CSVUploadForm, CustomUserCreationForm, CustomAuthenticationForm, UserProfileEditForm, WalletRecordForm, RecordChangeWalletForm, WalletEditForm, WalletInviteForm, RecordEditForm

from .serializers import *
from .permissions import IsAdminOrReadOnly, IsOwnerOrGuestInWallet, IsOwnerOrGuestInRecord
from .trade_logic import *
from .data_downloaders.yfinance_data import get_stock_data, get_prices_of_many_tickers


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


class MarketDetailView(generic.DetailView):
    model = Market
    template = "getstocksapp/market_detail.html"

        
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        market = self.get_object()
        tickers = Ticker.objects.filter(origin_market=market, for_display=True)
        sorter = self.request.GET.get('sort-by')
        
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
    

class TickerDetailView(generic.DetailView):
    model = Ticker
    template = "getstocksapp/ticker_detail.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        ticker = self.get_object()
        advisors = Advisor.objects.all()
        period = self.request.GET.get('period')
        if not period:
            period = "1y"
        data = get_stock_data(ticker=ticker.ticker_name, period=period)
        context["data_availble"] = not data.empty

        if not data.empty:
            for advisor in advisors:
                advisor.advice = advisor.get_advice(data)
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
            context['advisors'] = advisors
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


class AdvisorListView(generic.ListView):
    model = Advisor
    template = "getstocksapp/advisor_list.html"


class AdvisorDetailView(generic.DetailView):
    model = Advisor
    context_object_name = "advisor"
    template = "getstocksapp/advisor_detail.html"



############### Authorisation ##############


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
            return redirect(self.next_page)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class UserProfileView(generic.DetailView):
    model = User
    template_name = 'getstocksapp/user_profile.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        field_names = ['Id', 'Username', 'E-mail', 'First name', 'Last name', 'Joined']
        field_values = [user.id, user.username, user.email, user.first_name, user.last_name, user.date_joined,]

        context['user_data'] = list(zip(field_names, field_values))
        context['wallets'] = Wallet.objects.filter(owner=user)
        context['wallets_as_guest'] =  Wallet.objects.filter(guests=user)

        return context
    
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        already_existing_wallets = Wallet.objects.filter(owner=user)
        names = [wallet.name for wallet in already_existing_wallets]
        name = f"{user.username}_wallet"
        if name in names:
            base_name = name
            end_num = 0
            while True:
                if name in names:
                    end_num += 1
                    name = f'{base_name}_{end_num}'
                else:
                    break
            
        new_wallet = Wallet(owner=user, name=name)
        new_wallet.save()
        return redirect('getstocksapp:profile', pk=user.pk)


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileEditForm
    template_name = 'getstocksapp/user_profile_edit.html'
    success_url = reverse_lazy('getstocksapp:home')

    def get_object(self, queryset=None):
        return self.request.user


class AssetsView(generic.ListView):
    model = Wallet
    template_name = "getstocksapp/assets.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            return super().get(self, request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('getstocksapp:home'))
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        return context


class MyAssetsView(generic.DetailView):
    model = User
    template_name = "getstocksapp/my_assets.html"
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user = self.request.user
        context['own_wallets'] = Wallet.objects.filter(owner=user)
        context['wallets_as_guest'] =  Wallet.objects.filter(guests=user)
        return context
    
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        already_existing_wallets = Wallet.objects.filter(owner=user)
        names = [wallet.name for wallet in already_existing_wallets]
        name = f"{user.username}_wallet"
        if name in names:
            base_name = name
            end_num = 0
            while True:
                if name in names:
                    end_num += 1
                    name = f'{base_name}_{end_num}'
                else:
                    break
        new_wallet = Wallet(owner=user, name=name)
        new_wallet.save()
        return redirect('getstocksapp:my-assets', pk=user.pk)
    
    
################# Wallet #################


class WalletView(generic.DetailView):
    model = Wallet
    template_name = 'getstocksapp/wallet_as_unknown.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        wallet = self.get_object()
        related_records = WalletRecord.objects.filter(wallet = wallet)
        context['wallet_id'] = wallet.id
        context['guests'] = wallet.guests.all()
        total_wealth_in_currencies = {}
        if related_records:
            context['related_records'] = related_records
            tickers_names = [record.ticker.ticker_name for record in related_records]
            tickers_currencies = [record.ticker.currency for record in related_records]
            init_values = [record.init_price for record in related_records]
            prices = get_prices_of_many_tickers(tickers_names)
            growths = [price - init_price for price, init_price in zip(prices, init_values)]
            total_values = [price * record.quantity for price, record in zip(prices, related_records)]
            total_init_values = [(record.quantity * record.init_price) for record in related_records]
            total_growths = [total_value - total_init_value for total_value, total_init_value in zip(total_values, total_init_values)]
            context['records_data'] = list(zip(related_records, prices, growths, total_values, total_growths))
            for price, currency in zip(total_values, tickers_currencies):
                value = total_wealth_in_currencies.get(currency, 0)
                total_wealth_in_currencies[currency] = value + price
            context['wealth_by_currencies'] = total_wealth_in_currencies
        return context
    
    def get_template_names(self):
        wallet = self.get_object()
        user = self.request.user
        
        if wallet.owner == user:
            return ['getstocksapp/wallet_as_owner.html']
        elif user in wallet.guests.all():
            return ['getstocksapp/wallet_as_guest.html']
        
        return super().get_template_names()
    
    def post(self, request, *args, **kwargs):
        
        wallet = self.get_object()
        user = wallet.owner
        wallet.delete()
        return redirect('getstocksapp:my-assets', pk=user.pk)


class WalletAddView(generic.FormView):
    template_name = 'getstocksapp/wallet_add_record.html'
    form_class = WalletRecordForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['available_wallets'] = Wallet.objects.filter(owner=self.request.user)
        ticker_id = self.request.GET.get('ticker-id')
        context['ticker'] = Ticker.objects.get(id=ticker_id)

        return context


    def form_valid(self, form):
        wallet = form.cleaned_data['wallet']
        record = form.save(commit=False)

        record.quantity = form.cleaned_data.get('quantity', 1)
        record.wallet = wallet

        ticker_id = self.request.GET.get('ticker-id')
        price =  self.request.GET.get('price')
        record.init_price = price
        ticker = Ticker.objects.get(id=ticker_id)
        record.ticker = ticker
        record.save()
        return redirect('getstocksapp:wallet', pk=record.wallet.id)
    

class WalletEditView(generic.FormView):
    template_name = 'getstocksapp/wallet_edit.html'
    form_class = WalletEditForm


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['wallet'] = Wallet.objects.get(pk=self.kwargs['pk'])
        return context
    

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    

    def form_valid(self, form):
        wallet = Wallet.objects.get(pk=self.kwargs['pk'])
        name = form.cleaned_data['name']
        wallet.name = name
        wallet.save()
        return redirect('getstocksapp:wallet', pk=wallet.id)


class WalletInviteView(generic.FormView):
    template_name = 'getstocksapp/wallet_invite.html'
    form_class = WalletInviteForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['wallet'] = Wallet.objects.get(pk=self.kwargs['pk'])
        return context
    

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    

    def form_valid(self, form):
        wallet = Wallet.objects.get(pk=self.kwargs['pk'])
        user = form.cleaned_data['guests']
        wallet.guests.add(user)
        return redirect('getstocksapp:wallet', pk=wallet.id)


class WalletDropGuestView(generic.TemplateView):
    template_name = 'getstocksapp/wallet_drop_guest.html'


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['wallet'] = Wallet.objects.get(pk=self.kwargs['pk1'])
        context['guest'] = User.objects.get(pk=self.kwargs['pk2'])
        return context


    def post(self, request, *args, **kwargs):
        wallet = Wallet.objects.get(pk=self.kwargs['pk1'])
        guest = User.objects.get(pk=self.kwargs['pk2'])
        wallet.guests.remove(guest)
        wallet.save()
        return redirect('getstocksapp:my-assets', pk = self.request.user.id)


class WalletDeleteRecordView(generic.FormView):
    template_name = 'getstocksapp/wallet_delete_record.html'
    form_class = WalletRecordForm


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['record'] = WalletRecord.objects.get(pk=self.kwargs['pk'])
        return context
    

    def post(self, request, *args, **kwargs):    
        record = WalletRecord.objects.get(pk=self.kwargs['pk'])
        wallet = record.wallet
        record.delete()
        return redirect('getstocksapp:wallet', pk=wallet.pk)


class WalletEditRecordView(generic.FormView):
    template_name = 'getstocksapp/wallet_edit_record.html'
    form_class = RecordEditForm


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['record'] = WalletRecord.objects.get(pk=self.kwargs['pk'])
        return context


    def form_valid(self, form):
        record = WalletRecord.objects.get(pk=self.kwargs['pk'])
        name = form.cleaned_data['name']
        quantity = form.cleaned_data['quantity']
        if name:
            record.name = name
        record.quantity = quantity
        record.save()
        return redirect('getstocksapp:wallet', pk=record.wallet.id)
    

class WalletTransferRecordView(generic.FormView):
    template_name = 'getstocksapp/wallet_transfer_record.html'
    form_class = RecordChangeWalletForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['record'] = WalletRecord.objects.get(pk=self.kwargs['pk'])
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        record = WalletRecord.objects.get(pk=self.kwargs['pk'])
        wallet = form.cleaned_data['wallet']
        record.wallet = wallet
        record.save()
        return redirect('getstocksapp:wallet', pk=record.wallet.id)

########################### API

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'markets': drf_reverse('getstocksapp:api-market-list', request=request, format=format),
        'tickers': drf_reverse('getstocksapp:api-ticker-list', request=request, format=format),
        'users': drf_reverse('getstocksapp:api-user-list', request=request, format=format),
        'wallets': drf_reverse('getstocksapp:api-wallet-list', request=request, format=format),
        'wallet records': drf_reverse('getstocksapp:api-wallet-record-list', request=request, format=format),

    })


class ApiMarketListView(mixins.ListModelMixin, mixins.CreateModelMixin, drfgenerics.GenericAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class ApiMarketDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, drfgenerics.GenericAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class ApiTickerListView(mixins.ListModelMixin, mixins.CreateModelMixin, drfgenerics.GenericAPIView):
    queryset = Ticker.objects.filter(for_display=True)
    serializer_class = TickerSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class ApiTickerDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, drfgenerics.GenericAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ApiTickerFinancialDataView(drfgenerics.RetrieveAPIView):
    queryset = Ticker.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, *args, **kwargs):
        try:
            ticker = self.get_object()
            data = get_stock_data(ticker=ticker.ticker_name, period='1y')
            advisors = Advisor.objects.all()
            advices = {}
            for advisor in advisors:
                advices[advisor.name] = advisor.get_advice(data=data)
            hisorical_data = {}         
            for index, row in data.iterrows():
                hisorical_data[str(index)] = row.to_dict()

            financial_data = {'Current_price': float(data.iloc[-1]['Close']),
                            'Currency': ticker.currency,
                            'Advices': advices,
                            'History': hisorical_data
                            }
            data = data.iloc[::-1]
            return Response(financial_data)
        except:
            return Response("Data Unavailble")


class ApiUserListView(mixins.ListModelMixin, mixins.CreateModelMixin, drfgenerics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ApiUserDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, drfgenerics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ApiWalletListView(mixins.ListModelMixin, mixins.CreateModelMixin, drfgenerics.GenericAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsOwnerOrGuestInWallet]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Wallet.objects.all()
        if user.is_authenticated:
            queryset1 = Wallet.objects.filter(owner=user)
            queryset2 = Wallet.objects.filter(guests=user)
            return queryset1.union(queryset2)
        else:
            return Wallet.objects.none()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail: You do not have permission to do this."}, status=status.HTTP_403_FORBIDDEN)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class ApiWalletDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, drfgenerics.GenericAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsOwnerOrGuestInWallet]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class ApiWalletRecordListView(mixins.ListModelMixin, mixins.CreateModelMixin, drfgenerics.GenericAPIView):
    queryset = WalletRecord.objects.all()
    serializer_class = WalletRecordSerializer
    permission_classes = [IsOwnerOrGuestInRecord]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class ApiWalletRecordDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, drfgenerics.GenericAPIView):
    queryset = WalletRecord.objects.all()
    serializer_class = WalletRecordSerializer
    permission_classes = [IsOwnerOrGuestInRecord]


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ApiWalletRecordFinancialInfoView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, drfgenerics.GenericAPIView):
    wallets = Wallet.objects.filter()
    queryset = WalletRecord.objects.all()