from django.contrib.auth import views
from . import views
from django.urls import path


app_name = "getstocksapp"

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('market<int:pk>', views.MarketReview.as_view(), name='marketreview'),
    path('ticker<int:pk>', views.TickerReview.as_view(), name='tickerreview'),
    path('upload_csv', views.CSVUploadView.as_view(), name='upload_csv'),
    path('about', views.AboutUs.as_view(), name = 'about_us'),
    path('services', views.Services.as_view(), name = 'services'),
    path('contact', views.Contact.as_view(), name = 'contact')
]

