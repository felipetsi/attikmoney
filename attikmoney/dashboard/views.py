from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from attikmoney.core.models import Position, Broker, Order, Asset, AssetType
from pandas import DataFrame as df
from plotly.offline import plot
from plotly import graph_objs as go
from django.db.models import Avg, Count, Min, Sum
from datetime import date, datetime

#from attikmoney.core.models import Order, Balance, AssetType, Asset, Broker, Position

# Create your views here.
@login_required
def dashboard(request):
        user = request.user
        context = {}
        amount = {}
        wallet = {}

        context['graph_time'] = datetime.now()
        # Amount function - Get total amount values
        try:
                amountorder = amountOrders(user)
        except:
                amountorder = {}
                amountorder['orderDayB'] = 0
                amountorder['orderDayS'] = 0
                amountorder['wallet'] = 0
                amountorder['operatedMonth'] = 0
        amount['orderDayB'] = amountorder['orderDayB']
        amount['orderDayS'] = amountorder['orderDayS']
        amount['wallet'] = amountorder['wallet']
        amount['operatedMonth'] = amountorder['operatedMonth']

        # Wallet list
        try:
                context['walletlist_div'] = walletList(user)
        except:
                context['walletlist_div'] = ''

        # Type Allocation
        #try:
        context['type_allocation_div'] = typeAllocation(user)
        #except:
        #        context['type_allocation_div'] = ''

        # Generate graphs      
        try:
                context['position_div'] = position(request.user)
        except:
                context['position_div'] = ''

        template_name = 'dashboard.html'
        return render(request, template_name, context)

def amountOrders(user):
        context = {}
        context['orderDayB'] = Order.objects.filter(user = user, operation_type = 'b', operated_at = date.today()).values('id').count()
        context['orderDayS'] = Order.objects.filter(user = user, operation_type = 's', operated_at = date.today()).values('id').count()
        lastDayPos = Position.objects.filter(user = user).values('created_at__day').last()
        lastMontPos = Position.objects.filter(user = user).values('created_at__month').last()
        lastYearPos = Position.objects.filter(user = user).values('created_at__year').last()
        context['wallet'] = Position.objects.filter(
                user = user, 
                created_at__day = lastDayPos['created_at__day'], 
                created_at__month = lastMontPos['created_at__month'], 
                created_at__year = lastYearPos['created_at__year']
        ).values('id').count()
        
        orders = Order.objects.filter(
                user = user, 
                operated_at__month = datetime.now().month, 
                operated_at__year = datetime.now().year
        ).values('value', 'amount')

        context['operatedMonth'] = 0

        for order in orders:
                context['operatedMonth'] += order['value'] * order['amount']

        return(context)

def walletList(user):
        columns_name = ['asset','broker','type','balance']
        # Create the DataFrame to recive the data
        context = df(columns=columns_name)
        graphs={}
        
        # Get all Brokers
        broker_list = Broker.objects.filter(user=user).values('id')
        for broker_loop in broker_list:
                # Get All Assets
                asset_list = Asset.objects.filter(user=user).values('id','type','code').order_by('code').distinct()
                # Check balance of each Asset
                for asset in asset_list:
                        assetCode = asset['code']
                        assetType = AssetType.objects.get(pk=asset['type'])
                        broker = Broker.objects.get(pk=broker_loop['id'])
                        # Check the balance of each Asset
                        balance_buy = Order.objects.filter(
                                user=user, 
                                operation_type='b',
                                asset=asset['id'],
                                broker=broker
                                ).aggregate(Sum('amount'))

                        balance_sale = Order.objects.filter(
                                user=user, 
                                operation_type='s',
                                asset=asset['id'],
                                broker=broker
                                ).aggregate(Sum('amount'))
                        
                        try:
                                balance = balance_buy['amount__sum'] - balance_sale['amount__sum']
                        except:
                                if balance_sale['amount__sum'] == None:
                                        balance_sale['amount__sum'] = 0
                                if balance_buy['amount__sum'] == None:
                                        balance_buy['amount__sum'] = 0
                                
                                balance = balance_buy['amount__sum'] - balance_sale['amount__sum']
                                
                        if balance != 0:
                                context = context.append(df([[assetCode,broker,assetType,balance]], columns=columns_name))

        # Wallet graph:
        trace = go.Pie(labels = context['asset'], values = context['balance'])
        data = [trace]
        layout = go.Layout(title='Asset allocation')
        fig = go.Figure(data=data, layout=layout)

        wallet_div = plot(fig, output_type='div', include_plotlyjs=False)

        return(wallet_div)

def position(user):
        columns_name = ('broker','balance')
        data = df(columns=(columns_name))
        position_list = Position.objects.values('broker').annotate(Sum('balance')).order_by('-broker')
        for position in position_list:
                data = data.append(df([[Broker.objects.filter(
                                        pk=position['broker']
                                ).values('name')[0]['name'],
                                position['balance__sum']]],
                        columns=columns_name))

        x_data = data['broker']
        y_data = data['balance']

        layout = dict(
                title='Position',
                xaxis=dict(range=[min(x_data), max(x_data)]),
                yaxis=dict(range=[min(y_data), max(y_data)]),
        )

        fig = go.Figure(data=[go.Bar(x=x_data, y=y_data)], layout=layout)

        position_div = plot(fig, output_type='div', include_plotlyjs=False)
        return(position_div)

def totalBalance(user):
        columns_name = ('broker','balance')
        data = df(columns=(columns_name))
        position_list = Position.objects.values('broker').annotate(Sum('balance')).order_by('-broker')
        for position in position_list:
                data = data.append(df([[Broker.objects.filter(
                                        pk=position['broker']
                                ).values('name')[0]['name'],
                                position['balance__sum']]],
                        columns=columns_name))

        x_data = data['broker']
        y_data = data['balance']

        layout = dict(
                title='Position',
                xaxis=dict(range=[min(x_data), max(x_data)]),
                yaxis=dict(range=[min(y_data), max(y_data)]),
        )

        fig = go.Figure(data=[go.Bar(x=x_data, y=y_data)], layout=layout)

        position_div = plot(fig, output_type='div', include_plotlyjs=False)
        return(position_div)

def typeAllocation(user):
        columns_name = ['type','balance']
        # Create the DataFrame to recive the data
        context = df(columns=columns_name)

        #reference_date=Position.objects.filter(user=user).values('regarding_at').last()
        #ref_day = int(reference_date['regarding_at'].strftime('%d'))
        #ref_month = int(reference_date['regarding_at'].strftime('%m'))
        #ref_year = int(reference_date['regarding_at'].strftime('%Y'))

        assetType = AssetType.objects.filter(user=user).values('id', 'name')
        for type in assetType:
                try:
                        balance = Position.objects.filter(
                                user=user,
                                type=type['id'], 
                                #regarding_at=date(ref_year, ref_month, ref_day)
                                #regarding_at=date(ref_year, ref_month, ref_day)
                        ).values('balance').last()
                        balance = balance['balance']
                except:
                        balance = 0
                context = context.append(df([[type['name'],balance]], columns=columns_name))

        # Allocation by type graph:
        trace = go.Pie(labels = context['type'], values = context['balance'])
        data = [trace]
        layout = go.Layout(title='Type allocation')
        fig = go.Figure(data=data, layout=layout)

        type_alloc_div = plot(fig, output_type='div', include_plotlyjs=False)

        return(type_alloc_div)