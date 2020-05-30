from attikmoney.core.models import AssetType, Asset, Broker, Order, BrokerRateRule
from django.contrib.auth.models import User
from django.db.models.functions import Floor
from django.db.models import Sum
from datetime import datetime
        
def checkEmolument(total, ordertype):
        if ordertype == 'd':
            # Daytrade Emolument
            emolumentRate = 0.00023006
        else:
            # Normal Emolument
            emolumentRate = 0.00030506
        
        emolument = total * emolumentRate
        return (emolument)

def checkBrokerRate(brokerid, total, ordertype, user):
        tax = 1.096500 
        rate_value = BrokerRateRule.objects.filter( 
                user=user,
                broker=brokerid,
                ordertype=ordertype,
                greaterthan__lte=total,
                lessthan__gte=total,
        ).get()
        return (Floor(rate_value.rate * tax))

def calculateOrdersRates():
    #Calculate Orders Rates
    user_list = User.objects.all()
    for user in user_list:
        for op_type in 'bs': #for each b-Buy and each s-sell
            if op_type == 'b':
                op_type_opsite = 's'
            else:
                op_type_opsite = 'b'
            
            operated_today = Order.objects.filter(
                    user=user,
                    operation_type=op_type,
                    brokerrate=0).values('id','amount','asset','broker','value','operated_at')
            for order in operated_today:
                try:
                    order_pair = Order.objects.filter(
                        user=user,
                        asset=order['asset'],
                        operated_at=order['operated_at'],
                        operation_type=op_type_opsite).aggregate(Sum('amount'))
                    if order_pair['amount__sum'] >= 1:
                        ordertype = 'd'
                    else:
                        ordertype = 'n'
                except:
                    ordertype = 'n'
                
                total = (order['amount'] * order['value'])

                # Order target to update
                ot = Order.objects.get(pk=order['id'])
                ot.emolument = checkEmolument(total, ordertype)
                ot.brokerrate = checkBrokerRate(order['broker'], total, ordertype, user)
                ot.save()
    print(str(datetime.now())+" - Orders rates calculated.")