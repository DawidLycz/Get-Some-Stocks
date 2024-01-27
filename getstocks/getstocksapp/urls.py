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
    path('profile<int:pk>', views.UserProfileView.as_view(), name='profile'),
    path('profile_edit<int:pk>', views.UserProfileEditView.as_view(), name='profile_edit'),
    path('wallet<int:pk>', views.WalletView.as_view(), name='wallet'),
    path('wallet_add', views.WalletAddView.as_view(), name='wallet_add'),
    path('wallet_edit<int:pk>', views.WalletEditView.as_view(), name='wallet_edit'),
    path('wallet_invite<int:pk>', views.WalletInviteView.as_view(), name='wallet_invite'),
    path('wallet_edit_record<int:pk>', views.WalletEditRecordView.as_view(), name='wallet_edit_record'),
    path('wallet_transfer_record<int:pk>', views.WalletTransferRecordView.as_view(), name='wallet_transfer_record'),
    path('wallet_delete_record<int:pk>', views.WalletDeleteRecordView.as_view(), name='wallet_delete_record'),

]

