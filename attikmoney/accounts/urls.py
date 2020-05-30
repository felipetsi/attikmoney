from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView

from .views import *

app_name = 'accounts'
urlpatterns = [
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('register.html', register, name='register'),
    path('forgot-password.html', forgotpassword, name='forgotpassword'),
    path('logout',LogoutView.as_view(next_page='accounts:login'), name='logout'),
]