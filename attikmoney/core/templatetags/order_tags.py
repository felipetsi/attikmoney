from django import template
from django.http import HttpResponse
from attikmoney.core.models import Order
from django.db.models import Sum
from django.db.models import FloatField

register = template.Library()

@register.filter
def operationtype(value):
    context=''
    if value == 'b':
        context = "Buy"
    else:
        context = 'Sale'
    return context

@register.filter
def operationtypeicon(value):
    context=''
    if value == 'b':
        context = 'fas fa-shopping-cart'
    else:
        context = 'fas fa-cart-arrow-down'
    return context

@register.filter
def checkBalannce(asset):
    context = ''
    balAsset = 0
    balAssetBuy = Order.objects.filter( 
                        #user=User,
                        asset=asset,
                        operation_type='b'
                ).aggregate(amount=Sum('amount', output_field=FloatField()))
    balAssetSale = Order.objects.filter( 
                        #user=User,
                        asset=asset,
                        operation_type='s'
                ).aggregate(amount=Sum('amount', output_field=FloatField()))
    
    if balAssetBuy['amount'] == None:
        balAssetBuy['amount'] = 0
    if balAssetSale['amount'] == None:
        balAssetSale['amount'] = 0

    balAsset = int(balAssetBuy['amount']) - int(balAssetSale['amount'])
    
    if balAsset == 0:
        context = 'far fa-check-circle'
    elif balAsset > 0:
        context = 'fas fa-plus-circle'
    else:
        context = 'fas fa-minus-circle'
    
    return context