from django.contrib.auth import views
from django.contrib.auth.views import LogoutView
from . import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


app_name = "getstocksapp"
market_list = views.ApiMarketViewSet.as_view({'get': 'list', 'post': 'create'})
market_detail = views.ApiMarketViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})
ticker_list = views.ApiTickerViewSet.as_view({'get': 'list', 'post': 'create'})
ticker_detail = views.ApiTickerViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})


urlpatterns = format_suffix_patterns([
    path('', views.IndexView.as_view(), name='home'),
    path('market/<int:pk>/', views.MarketReview.as_view(), name='marketreview'),
    path('ticker/<int:pk>/', views.TickerReview.as_view(), name='tickerreview'),
    path('upload_csv/', views.CSVUploadView.as_view(), name='upload-csv'),
    path('about/', views.AboutUs.as_view(), name='about-us'),
    path('advisor_info/', views.AdvisorInfo.as_view(), name='advisor-info'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logoutconfirm/', views.LogoutConfirm.as_view(), name='logoutconfirm'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', views.UserProfileEditView.as_view(), name='profile-edit'),
    path('wallets/<int:pk>/', views.WalletView.as_view(), name='wallet'),
    path('wallets/add/', views.WalletAddView.as_view(), name='wallet-add'),
    path('wallets/edit/<int:pk>/', views.WalletEditView.as_view(), name='wallet-edit'),
    path('wallets/invite/<int:pk>/', views.WalletInviteView.as_view(), name='wallet-invite'),
    path('wallets/edit/record/<int:pk>/', views.WalletEditRecordView.as_view(), name='wallet-edit-record'),
    path('wallets/transfer/record/<int:pk>/', views.WalletTransferRecordView.as_view(), name='wallet-transfer-record'),
    path('wallets/delete/record/<int:pk>/', views.WalletDeleteRecordView.as_view(), name='wallet-delete-record'),
    path('wallets/drop-guest/<int:pk1>/<int:pk2>/', views.WalletDropGuestView.as_view(), name='wallet-drop-guest'),

    ###############
    
    path('api/', views.api_root, name='api-root'),
    path('api/market/', market_list, name='market-list'),
    path('api/market/<int:pk>/', market_detail, name='market-detail'),
    path('api/ticker/', ticker_list, name='ticker-list'),
    path('api/ticker/<int:pk>/', ticker_detail, name='ticker-detail'),
])
