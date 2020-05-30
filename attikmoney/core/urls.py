#from django.contrib import admin
from django.urls import path
from .views import order_list, order_add, order_update, report_average, report_daily_profit_loss, income_tax
from .views import report_income_tax_position, report_income_tax_profit_loss, report_income_tax_non_taxable_profit_loss, report_amount_income_tax_paid
from .views import asset_type, yield_type, dividend_yield, broker, brokerraterule, order_delete, asset_add, asset_update, asset_delete, asset_list

app_name = 'core'
urlpatterns = [
    path('order', order_list, name='order_list'),
    path('order/add', order_add, name='order_add'),
    path('order/update/<int:pk>', order_update, name='order_update'),
    path('order/delete/<int:pk>', order_delete, name='order_delete'),

    path('asset', asset_list, name='asset_list'),
    path('asset/add', asset_add, name='asset_add'),
    path('asset/update/<int:pk>', asset_update, name='asset_update'),
    path('asset/delete/<int:pk>', asset_delete, name='asset_delete'),

    path('report_average.html', report_average, name='report_average'),
    path('report_daily_profit_loss.html', report_daily_profit_loss, name='report_daily_profit_loss'),
    path('income_tax.html', income_tax, name='income_tax'),
    path('report_income_tax_position.html', report_income_tax_position, name='report_income_tax_position'),
    path('report_income_tax_profit_loss.html', report_income_tax_profit_loss, name='report_income_tax_profit_loss'),
    path('report_income_tax_non_taxable_profit_loss.html', report_income_tax_non_taxable_profit_loss, name='report_income_tax_non_taxable_profit_loss'),
    path('report_amount_income_tax_paid.html', report_amount_income_tax_paid, name='report_amount_income_tax_paid'),
    path('asset_type.html', asset_type, name='asset_type'),
    path('yield_type.html', yield_type, name='yield_type'),
    path('dividend_yield.html', dividend_yield, name='dividend_yield'),
    path('broker.html', broker, name='broker'),
    path('brokerraterule.html', brokerraterule, name='brokerraterule'),
]