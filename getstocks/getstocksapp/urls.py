# urls.py
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include

app_name = "getstocksapp"

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('<int:pk>', views.CountryReview.as_view(), name='countryreview'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
