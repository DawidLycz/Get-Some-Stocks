from django.contrib.auth import views
from django.contrib.auth.views import LogoutView
from . import views
from django.urls import path


app_name = "getstocksapp"

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('market<int:pk>', views.MarketReview.as_view(), name='marketreview'),
    path('ticker<int:pk>', views.TickerReview.as_view(), name='tickerreview'),
    path('upload_csv', views.CSVUploadView.as_view(), name='upload_csv'),
    path('about', views.AboutUs.as_view(), name='about_us'),
    path('services', views.Services.as_view(), name='services'),
    path('contact', views.Contact.as_view(), name='contact'),
    path('advisor_info', views.AdvisorInfo.as_view(), name='advisor_info'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logoutconfirm', views.LogoutConfirm.as_view(), name='logoutconfirm'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile<int:pk>', views.UserProfileView.as_view(), name='profile')

]

