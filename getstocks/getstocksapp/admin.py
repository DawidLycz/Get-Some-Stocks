from django import forms
from django.contrib import admin
from django.http import HttpResponse, JsonResponse
from django.urls import path, reverse
from django.utils.safestring import mark_safe
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt

import pandas as pd

from admin_extra_buttons.api import ExtraButtonsMixin, button, confirm_action, link, view
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer

from .data_downloaders.alphavantage_data import get_ticker_info_obj

from .models import Market, Ticker, Advisor,  Wallet, WalletRecord

class MarketAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ('name', 'logo_thumbnail') 
    search_fields = ['name']  
    list_filter = ['name'] 

    def logo_thumbnail(self, obj):
        if obj.logo_img:
            return mark_safe(f'<img src="{obj.logo_img.url}" width="100" height="auto" />')
        return "No logo"

    logo_thumbnail.short_description = 'Logo'


    @link(change_list=False, html_attrs={'target': '_new', 'style': 'background-color:var(--button-bg)'})
    def upload_csv(self, button):
        original = button.context['original']
        button.label = f"Upload CSV data for {original.name}."
        button.href = reverse('getstocksapp:upload-csv')



class TickerAdmin(admin.ModelAdmin):
    
    search_fields = ['ticker_name'] 
    list_display = ('ticker_name', 'company_name', 'origin_market', 'data_fetched', 'full_data', 'for_display')
    list_filter = ['origin_market','data_fetched', 'full_data', 'for_display']
    ordering = ['ticker_name']
    actions = ['fetch_data', 'mark_unfetch', 'verify_data', 'mark_for_display_unconditionaly', 'mark_for_display_if_full_data']

    def fetch_data(self, request, queryset):
        
        for ticker in queryset:
            ticker.download_data()
        self.message_user(request, "Data has been downloaded and assingned to record(s)")        
    
    def mark_unfetch(self, request, querryset):

        for ticker in querryset:
            ticker.data_fetched = False
            ticker.save()
        self.message_user(request, "Records has been set as unfetched")

    def mark_for_display_unconditionaly(self, request, querryset):

        for ticker in querryset:
            ticker.set_for_display() 
        self.message_user(request, "Records has been set as for display")

    def mark_for_display_if_full_data(self, request, querryset):

        for ticker in querryset:
            if ticker.full_data:
                ticker.set_for_display()      
        self.message_user(request, "Records has been set as for display")

    def verify_data(self, request, querryset):
        for ticker in querryset:
            ticker.verify_full_data()
        self.message_user(request, "Data has been verified. Tickers with full data has been marked")
        
    mark_unfetch.short_description = "Mark unfetched"
    fetch_data.short_description = "Fetch data"
    verify_data.short_description = "Verify if data in database"
    mark_for_display_if_full_data.short_description = "Mark ticker as 'for display' if full data"
    mark_for_display_unconditionaly.short_description = "Mark ticker as 'for display' unconditionaly"

admin.site.register(Market, MarketAdmin)
admin.site.register(Ticker, TickerAdmin)
admin.site.register(Advisor)
admin.site.register(Wallet)
admin.site.register(WalletRecord)
