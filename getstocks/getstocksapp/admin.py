from django.contrib import admin
from .models import Market, Ticker
from .alphavantage_data import get_ticker_info_obj
from django.utils.safestring import mark_safe

import pandas as pd
from django.http import HttpResponse
from django.urls import path
from django import forms
from django.contrib import admin
from .models import Ticker
import csv
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib import admin
from .models import Market

class CustomAdminSite(admin.sites.AdminSite):
    site_header = "Get Some Stocks"
    
    def custom_link(self, request):
        return(HttpResponseRedirect('upload_csv'))


class MarketAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_thumbnail') 
    search_fields = ['name']  
    list_filter = ['name'] 

    def logo_thumbnail(self, obj):
        if obj.logo_img:
            return mark_safe(f'<img src="{obj.logo_img.url}" width="100" height="auto" />')
        return "No logo"

    logo_thumbnail.short_description = 'Logo'

from django.contrib import admin
from .models import Ticker

class TickerAdmin(admin.ModelAdmin):
    
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
custom_admin_site = CustomAdminSite(name='custom_admin')