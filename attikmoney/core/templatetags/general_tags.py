from django import template
from django.http import HttpResponse

register = template.Library()

@register.filter
def orderType(value):
    context=''
    if value == 'd':
        context = "Daytrade"
    else:
        context = 'Normal'
    return context

@register.filter
def yesNo(value):
    context=''
    if value == 'y':
        context = "Yes"
    else:
        context = 'No'
    return context

@register.filter
def real_money_mask(value):
    try:
        float(value)
        a = '{:,.2f}'.format(float(value))
        b = a.replace(',','v')
        c = b.replace('.',',')
        val_return = 'R$ '+c.replace('v','.')
        
    except:
        val_return = value
    return (val_return)