from django.urls import path
#from django.urls import include
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('dashboard.html', views.dashboard, name='dashboard'),
    #path('django_plotly_dash/', include('django_plotly_dash.urls')),
]