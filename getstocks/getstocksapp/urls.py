from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


app_name = "getstocksapp"

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('<int:pk>', views.MarketReview.as_view(), name='marketreview'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('upload_csv', views.CSVUploadView.as_view(), name='upload_csv'),
]

