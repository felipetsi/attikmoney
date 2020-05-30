from django.urls import path
from .views import report_income_tax_month, report_position

app_name = 'report'
urlpatterns = [
    path('report_income_tax_month.html', report_income_tax_month, name='report_income_tax_month'),
    path('report_position.html', report_position, name='report_position'),
]
#    path('asset', asset_list, name='asset_list'),
#    path('asset/add', asset_add, name='asset_add'),
#    path('asset/update/<int:pk>', asset_update, name='asset_update'),
#    path('asset/delete/<int:pk>', asset_delete, name='asset_delete'),