from django.contrib.auth import views
from django.contrib.auth.views import LogoutView
from . import views
from django.urls import path


app_name = "getstocksapp"

# urlpatterns = [
#     path('', views.IndexView.as_view(), name='home'),
#     path('market<int:pk>', views.MarketReview.as_view(), name='marketreview'),
#     path('ticker<int:pk>', views.TickerReview.as_view(), name='tickerreview'),
#     path('upload_csv', views.CSVUploadView.as_view(), name='upload_csv'),
#     path('about', views.AboutUs.as_view(), name='about_us'),
#     path('services', views.Services.as_view(), name='services'),
#     path('contact', views.Contact.as_view(), name='contact'),
#     path('advisor_info', views.AdvisorInfo.as_view(), name='advisor_info'),
#     path('registration/', views.RegistrationView.as_view(), name='registration'),
#     path('login/', views.CustomLoginView.as_view(), name='login'),
#     path('logoutconfirm', views.LogoutConfirm.as_view(), name='logoutconfirm'),
#     path('logout/', views.CustomLogoutView.as_view(), name='logout'),
#     path('profile<int:pk>', views.UserProfileView.as_view(), name='profile'),
#     path('profile_edit<int:pk>', views.UserProfileEditView.as_view(), name='profile_edit'),
#     path('wallet<int:pk>', views.WalletView.as_view(), name='wallet'),
#     path('wallet_add', views.WalletAddView.as_view(), name='wallet_add'),
#     path('wallet_edit<int:pk>', views.WalletEditView.as_view(), name='wallet_edit'),
#     path('wallet_invite<int:pk>', views.WalletInviteView.as_view(), name='wallet_invite'),
#     path('wallet_edit_record<int:pk>', views.WalletEditRecordView.as_view(), name='wallet_edit_record'),
#     path('wallet_transfer_record<int:pk>', views.WalletTransferRecordView.as_view(), name='wallet_transfer_record'),
#     path('wallet_delete_record<int:pk>', views.WalletDeleteRecordView.as_view(), name='wallet_delete_record'),
#     path('wallet_drop_guest/<int:pk1>/<int:pk2>/', views.WalletDropGuestView.as_view(), name='wallet_drop_guest'),
# ]


urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('market/<int:pk>/', views.MarketReview.as_view(), name='marketreview'),
    path('ticker/<int:pk>/', views.TickerReview.as_view(), name='tickerreview'),
    path('upload_csv/', views.CSVUploadView.as_view(), name='upload-csv'),
    path('about/', views.AboutUs.as_view(), name='about-us'),
    path('services/', views.Services.as_view(), name='services'),
    path('contact/', views.Contact.as_view(), name='contact'),
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
]
