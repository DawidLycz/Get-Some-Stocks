from django.contrib.auth import views
from django.contrib.auth.views import LogoutView
from . import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


app_name = "getstocksapp"


urlpatterns = format_suffix_patterns([
    path('', views.IndexView.as_view(), name='home'),
    path('market/<int:pk>/', views.MarketDetailView.as_view(), name='market-detail'),
    path('ticker/<int:pk>/', views.TickerDetailView.as_view(), name='ticker-detail'),
    path('upload_csv/', views.CSVUploadView.as_view(), name='upload-csv'),
    path('about/', views.AboutUs.as_view(), name='about-us'),
    path('advisor_info/', views.AdvisorInfo.as_view(), name='advisor-info'),
    path('advisors/', views.AdvisorListView.as_view(), name='advisor-list'),
    path('advisors/<int:pk>/', views.AdvisorDetailView.as_view(), name='advisor-detail'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logoutconfirm/', views.LogoutConfirm.as_view(), name='logoutconfirm'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', views.UserProfileEditView.as_view(), name='profile-edit'),

    path('assets/', views.AssetsView.as_view(), name='assets'),
    path('assets/<int:pk>/', views.MyAssetsView.as_view(), name='my-assets'),

    path('wallets/add/', views.WalletAddView.as_view(), name='wallet-add'),
    path('wallets/<int:pk>/', views.WalletView.as_view(), name='wallet'),
    path('wallets/edit/<int:pk>/', views.WalletEditView.as_view(), name='wallet-edit'),
    path('wallets/invite/<int:pk>/', views.WalletInviteView.as_view(), name='wallet-invite'),
    path('wallets/edit/record/<int:pk>/', views.WalletEditRecordView.as_view(), name='wallet-edit-record'),
    path('wallets/transfer/record/<int:pk>/', views.WalletTransferRecordView.as_view(), name='wallet-transfer-record'),
    path('wallets/delete/record/<int:pk>/', views.WalletDeleteRecordView.as_view(), name='wallet-delete-record'),
    path('wallets/drop-guest/<int:pk1>/<int:pk2>/', views.WalletDropGuestView.as_view(), name='wallet-drop-guest'),

    ###############

    path('api/', views.api_root, name='api-root'),
    path('api/markets/', views.ApiMarketListView.as_view(), name='api-market-list'),
    path('api/markets/<int:pk>/', views.ApiMarketDetailView.as_view(), name='api-market-detail'),
    path('api/tickers/', views.ApiTickerListView.as_view(), name='api-ticker-list'),
    path('api/tickers/<int:pk>/', views.ApiTickerDetailView.as_view(), name='api-ticker-detail'),
    path('api/tickers/<int:pk>/financialinfo/', views.ApiTickerFinancialDataView.as_view(), name='api-ticker-financial-info'),
    path('api/users/', views.ApiUserListView.as_view(), name='api-user-list'),
    path('api/users/<int:pk>/', views.ApiUserDetailView.as_view(), name='api-user-detail'),
    path('api/wallets/', views.ApiWalletListView.as_view(), name='api-wallet-list'),
    path('api/wallets/<int:pk>/', views.ApiWalletDetailView.as_view(), name='api-wallet-detail'),
    path('api/wallets/records/', views.ApiWalletRecordListView.as_view(), name='api-wallet-record-list'),
    path('api/wallets/records/<int:pk>/', views.ApiWalletRecordDetailView.as_view(), name='api-wallet-record-detail'),
])
