from django.urls import path
from .views import login_page, register_page, index, logout_page, deposit, withdraw, transactions, \
    export_users_xls, oauth_login

urlpatterns = [
    path('', index, name='index'),
    path('deposit/', deposit, name='deposit'),
    path('withdraw/', withdraw, name='withdraw'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_page, name='logout'),
    path('transactions/', transactions, name='transactions'),
    path('export/xls/', export_users_xls, name='export_users_xls'),
    path('oauth-login/', oauth_login, name='oauth_login'),
]