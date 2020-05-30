from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from attikmoney.core.models import Order, Balance, AssetType, Asset, Broker, Position
from django.db.models.functions import Floor
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
import datetime
import pandas as pd
from django.db.models import Avg, Count, Min, Sum

# Create your views here.

# Return the last day of month
def last_day(year,month):
        try:
                datetime.date(year, month, 31)
                day = 31
        except:
                day = 0
        if day == 0:
                try:
                        datetime.date(year, month, 30)
                        day = 30
                except:
                        day = 0
                if day == 0:
                        try:
                                datetime.date(year, month, 29)
                                day = 29
                        except:
                                day = 0
                        if day == 0:
                                day = 28
        return day

# Calculate Income Tax
def calculate_income_tax(type, totalvalue):
        return_value = 0
        if type == 'd':
                return_value = totalvalue * 0.2
        else:
                return_value = totalvalue * 0.15
        return totalvalue

# Verify amount to calculate income tax
@login_required
def check_balance_order(request,month,year):
        context = {}
        context['total_operated'] = 0
        context['d_total_sale'] = 0
        context['d_total_buy'] = 0
        context['n_total_sale'] = 0
        context['n_total_buy'] = 0
        context['d_total_income_tax'] = 0
        context['n_total_income_tax'] = 0
        context['period'] = str(month)+"/"+str(year)

        user = request.user

        day = last_day(year,month)

        assetType = AssetType.objects.filter( user=user, name='Stock')

        total_operated = 0
        orders_month = Order.objects.filter(
                user=user, 
                operated_at__gte=datetime.date(year, month, 1), 
                operated_at__lte=datetime.date(year, month, day),
                ).values('id', 'amount', 'value', 'operation_type')

        for order in orders_month:
                total_operated += (order['amount'] * order['value'])

        context['total_operated'] = total_operated
        if total_operated > 20000: # limit to pay income tax obligation
                #Reset final variables
                global_income_tax_daytrade = 0
                global_income_tax_normal = 0
                t_balance_daytrade = 0
                t_balance_normal = 0

                # Reset sum_buy values. The sum_sale don't need to reset each loop.
                sum_amount_asset_buy = 0
                sum_t_value_asset_buy = 0
                sum_operations_buy = 0
                sum_amount_asset_sale = 0
                sum_t_value_asset_sale = 0
                sum_operations_sale = 0

                asset_operated = Order.objects.filter(
                        user=user,
                        operated_at__gte=datetime.date(year, month, 1), 
                        operated_at__lte=datetime.date(year, month, day)
                        ).values('asset').order_by('asset').distinct()

                for asset in asset_operated:

                        # Check Sale's order
                        asset_operations_sale = Order.objects.filter(
                                user=user, 
                                operation_type='s', 
                                asset=asset['asset'],
                                operated_at__gte=datetime.date(year, month, 1), 
                                operated_at__lte=datetime.date(year, month, day)
                                ).values('amount', 'value', 'operated_at', 'brokerrate', 'emolument')

                        ## CHECK DAY TRADE OPERATIONS

                        for operation_sale in asset_operations_sale:
                                # Reset sum_buy values. The sum_sale don't need to reset each loop.
                                sum_amount_asset_buy = 0
                                sum_t_value_asset_buy = 0
                                sum_operations_buy = 0
                                sum_amount_asset_sale = 0
                                sum_t_value_asset_sale = 0
                                sum_operations_sale = 0
                                # Get Buy's Orders
                                asset_operations_buy = Order.objects.filter(
                                        user=user, 
                                        operation_type='b', 
                                        asset=asset['asset'],
                                        operated_at=operation_sale['operated_at'],
                                        ).values('amount', 'value', 'operated_at', 'brokerrate', 'emolument')
                                
                                for operation_buy in asset_operations_buy:
                                        # Get Sale's Orders
                                        asset_operations_sale_inside = Order.objects.filter(
                                                user=user, 
                                                operation_type='s', 
                                                asset=asset['asset'],
                                                operated_at=operation_buy['operated_at'],
                                                ).values('amount', 'value', 'operated_at', 'brokerrate', 'emolument')
                                        for sale_same_day in asset_operations_sale_inside:
                                                # Sum Sale's data
                                                sum_amount_asset_sale += sale_same_day['amount']
                                                sum_t_value_asset_sale += sale_same_day['amount'] * sale_same_day['value']
                                                sum_operations_sale += sale_same_day['brokerrate'] + sale_same_day['emolument']
                                                
                                        # Sum Buy's data 
                                        sum_amount_asset_buy += operation_buy['amount']
                                        sum_t_value_asset_buy += operation_buy['amount'] * operation_buy['value']
                                        sum_operations_buy += operation_buy['brokerrate'] + operation_buy['emolument']
                        
                        # Load context
                        context['d_total_sale'] += sum_t_value_asset_sale
                        context['d_total_buy'] += sum_t_value_asset_buy

                        # Calculate mean price of buy and sale
                        mean_price_buy =  (sum_t_value_asset_buy / sum_amount_asset_buy) if sum_amount_asset_buy != 0 else 0
                        mean_price_sale =  (sum_t_value_asset_sale / sum_amount_asset_sale) if sum_amount_asset_sale != 0 else 0

                        if sum_amount_asset_buy > sum_amount_asset_sale:
                                # Use the sum_amount_asset_sale as reference to calculate equal, the buy and the sale
                                t_balance_daytrade = ( (mean_price_buy * sum_amount_asset_sale - mean_price_sale * sum_amount_asset_sale) -
                                                (sum_operations_buy + sum_operations_sale) )
                                global_income_tax_daytrade += calculate_income_tax('d', t_balance_daytrade)
                        else:
                                # Use the sum_amount_asset_buy as reference to calculate equal, the buy and the sale
                                t_balance_daytrade = ( (mean_price_buy * sum_amount_asset_buy - mean_price_sale * sum_amount_asset_buy) -
                                                (sum_operations_buy + sum_operations_sale) )
                                global_income_tax_daytrade += calculate_income_tax('d', t_balance_daytrade)

                        ## END - CHECK DAY TRADE OPERATIONS
                        
                        ## CHECK NORMAL OPERATIONS
                        for operation_sale in asset_operations_sale:
                                # Reset sum_buy values. The sum_sale don't need to reset each loop.
                                sum_amount_asset_buy = 0
                                sum_t_value_asset_buy = 0
                                sum_operations_buy = 0

                                # Sum sale's data
                                sum_amount_asset_sale = operation_sale['amount']
                                sum_t_value_asset_sale = operation_sale['amount'] * operation_sale['value']
                                sum_operations_sale = operation_sale['brokerrate'] + operation_sale['emolument']

                                # Get Buy's Orders
                                asset_operations_buy = Order.objects.filter(
                                        user=user, 
                                        operation_type='b', 
                                        asset=asset['asset'],
                                        # DIFERENCE operated_at=operation_sale['operated_at']
                                        ).values('amount', 'value', 'brokerrate', 'emolument').order_by('-operated_at')
                                
                                for operation_buy in asset_operations_buy:
                                        # Sum buy's data 
                                        sum_amount_asset_buy += operation_buy['amount']
                                        sum_t_value_asset_buy += operation_buy['amount'] * operation_buy['value']
                                        sum_operations_buy += operation_buy['brokerrate'] + operation_buy['emolument']

                                        if sum_amount_asset_buy >= sum_amount_asset_sale:
                                                break

                        # Load context
                        context['n_total_sale'] += sum_t_value_asset_sale
                        context['n_total_buy'] += sum_t_value_asset_buy

                        # Calculate mean price of buy and sale
                        mean_price_buy =  (sum_t_value_asset_buy / sum_amount_asset_buy) if sum_amount_asset_buy != 0 else 0
                        mean_price_sale =  (sum_t_value_asset_sale / sum_amount_asset_sale) if sum_amount_asset_sale != 0 else 0
                        
                        if sum_amount_asset_buy > sum_amount_asset_sale:
                                # Use the sum_amount_asset_sale as reference to calculate equal, the buy and the sale
                                t_balance_normal = ( (mean_price_buy * sum_amount_asset_sale - mean_price_sale * sum_amount_asset_sale) -
                                                (sum_operations_buy + sum_operations_sale) )
                                global_income_tax_normal += calculate_income_tax('n', t_balance_normal)
                        else:
                                # Use the sum_amount_asset_buy as reference to calculate equal, the buy and the sale
                                t_balance_normal = ( (mean_price_buy * sum_amount_asset_buy - mean_price_sale * sum_amount_asset_buy) -
                                                (sum_operations_buy + sum_operations_sale) )
                                global_income_tax_normal += calculate_income_tax('n', t_balance_normal)

                        ## END - CHECK NORMAL OPERATIONS
                
                # Verify income tax to pay
                # Reset Variables
                global_balance_daytrade = 0
                global_balance_normal = 0
                
                ## DAY TRADE
                balance_tax = Balance.objects.filter(
                                        user=user, 
                                        type=1,
                                        type_operation='d',
                                        reference_date__lte=datetime.date(year, month, day)
                                        ).values('balance')
                
                for balance in balance_tax:
                        global_balance_daytrade += balance['balance']

                if (global_balance_daytrade + global_income_tax_daytrade) > 0: # Calculate income tax if greater 0
                        tax_to_pay_daytrade = calculate_income_tax('d', (global_balance_daytrade + global_income_tax_daytrade))
                else:
                        tax_to_pay_daytrade = 0
                # Load context
                context['d_total_income_tax'] += tax_to_pay_daytrade

                ## Normal
                balance_tax = Balance.objects.filter(
                                        user=user, 
                                        type=1,
                                        type_operation='n',
                                        reference_date__lte=datetime.date(year, month, day)
                                        ).values('balance')
                
                for balance in balance_tax:
                        global_balance_normal += balance['balance']

                if (global_balance_normal + global_income_tax_normal) > 0: # Calculate income tax if greater 0
                        tax_to_pay_normal = calculate_income_tax('n', (global_balance_normal + global_income_tax_normal))
                else:
                        tax_to_pay_normal = 0
                # Load context
                context['n_total_income_tax'] += tax_to_pay_normal

                # Save month balance
                ## Day Trade
                assetTypeStock = AssetType.objects.filter(
                        user=user,
                        name='Stock'
                )[0]

                balance_daytrade = Balance(
                        user=user, 
                        type=assetTypeStock, 
                        balance=global_balance_daytrade, 
                        type_operation='d',
                        reference_date=datetime.date(year, month, 1),
                        tax_to_pay=tax_to_pay_daytrade
                        )
                balance_daytrade.save()
                ## Normal
                balance_normal = Balance(
                        user=user, 
                        type=assetTypeStock, 
                        balance=global_balance_daytrade, 
                        type_operation='n',
                        reference_date=datetime.date(year, month, 1),
                        tax_to_pay=tax_to_pay_normal
                        )
                balance_normal.save()
        return context

@login_required
def report_income_tax_month(request):
        year = datetime.datetime.now().year
        context = pd.DataFrame(columns=['total_operated','d_total_sale','d_total_buy','n_total_sale','n_total_buy','d_total_income_tax','n_total_income_tax','period'])
        for month in range(1, 13): # range from 1 to 12.
                context = context.append(check_balance_order(request,month,year), ignore_index=True)
        template_name = 'report_income_tax_month.html'
        return render(request,template_name,{'DataFrame': context})

@login_required
def report_position(request):
        
        user = request.user

        columns_name = ['asset','broker','type','balance']
        context = pd.DataFrame(columns=columns_name)
        
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
                                context = context.append(pd.DataFrame([[assetCode,broker,assetType,balance]], columns=columns_name))
                                position_row = Position(
                                        user=user, 
                                        type=assetType,
                                        balance=balance,
                                        broker=broker
                                )
                                position_row.save()

        template_name = 'report_position.html'
        return render(request,template_name,{'DataFrame': context})