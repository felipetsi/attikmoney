from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from .forms import forms, TypeAssetForm, AssetForm, DividendYieldForm, YieldTypeForm, BrokerForm, OrderForm, BrokerRateRuleForm, ImportTradesForm
from .models import AssetType, Asset, YieldType, DividendYield, Balance, Broker, Order, BrokerRateRule, Tax, Language
from django.db.models.functions import Floor
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from datetime import date
import pandas as pd

#from django.db.models import DecimalField
#from django.db.models.functions import Cast

# Create your views here.

@login_required
def order_list(request):
        context = {}
        user = request.user
        context['objects_list'] = Order.objects.filter(user=user)
        template_name = 'order_list.html'
        
        # Pagination
        page = request.GET.get('page', 1)

        paginator = Paginator(context['objects_list'], 10)
        try:
                context['objects_list'] = paginator.page(page)
        except PageNotAnInteger:
                context['objects_list'] = paginator.page(1)
        except EmptyPage:
                context['objects_list'] = paginator.page(paginator.num_pages)
        # End Pagination

        return render(request, template_name, context)
        
@login_required
def order_save(request, form, template_name):
        
        context = {}
        data = dict()
        user = request.user
        if request.method == 'POST':
                form = OrderForm(request.POST)
                if form.is_valid():
                        form = form.save(commit=False)
                        form.brokerrate = 0
                        form.emolument = 0
                        form.user = user
                        form.save()
                        messages.success(request, 'Created as successful')
                        form = OrderForm()
                        data['form_is_valid'] = True
                        object_list = Order.objects.filter(user=user)
                        #.order_by(('-operated_at'))
                        data['html_objects_list'] = render_to_string('order_list_itens.html', {
                                'objects_list': object_list
                        })
                else:
                        data['form_is_valid'] = False

        context['form'] = form

        data['html_objects'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

@login_required
def order_add(request):
        if request.method == 'POST':
                form = OrderForm(request.POST)
        else:
                form = OrderForm()
        template_name = 'order_add.html'
        return order_save(request, form, template_name)

@login_required
def order_update(request, pk):
        object_target = get_object_or_404(Order, pk=pk)
        if request.method == 'POST':
                form = OrderForm(request.POST, instance=object_target)
        else:
                form = OrderForm(instance=object_target)
        template_name = 'order_update.html'
        return order_save(request, form, template_name)

@login_required
def order_delete(request, pk):
    object_target = get_object_or_404(Order, pk=pk)
    context = {}
    data = dict()
    user = request.user
    if request.method == 'POST':
        object_target.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        object_list = Order.objects.filter(user=user)
        data['html_objects_list'] = render_to_string('order_list_itens.html', {
                'objects_list': object_list
        })
    else:
        context['order'] = object_target
        template_name = 'order_delete.html'
        data['html_objects'] = render_to_string(template_name, context, request=request,)
    return JsonResponse(data)

@login_required
def report_average(request):
        return render(request, 'report_average.html')

@login_required
def report_daily_profit_loss(request):
        return render(request, 'report_daily_profit_loss.html')

@login_required
def income_tax(request):
        return render(request, 'income_tax.html')

@login_required
def report_income_tax_position(request):
        return render(request, 'report_income_tax_position.html')

@login_required
def report_income_tax_profit_loss(request):
        return render(request, 'report_income_tax_profit_loss.html')

@login_required
def report_income_tax_non_taxable_profit_loss(request):
        return render(request, 'report_income_tax_non_taxable_profit_loss.html')

@login_required
def report_amount_income_tax_paid(request):
        return render(request, 'report_amount_income_tax_paid.html')

@login_required
def report_performance(request):
        return render(request, 'report_performance.html')

def asset_list(request):
        context = {}
        user = request.user
        context['objects_list'] = Asset.objects.filter(user=user)
        template_name = 'asset_list.html'
        
        # Pagination
        page = request.GET.get('page', 1)

        paginator = Paginator(context['objects_list'], 10)
        try:
                context['objects_list'] = paginator.page(page)
        except PageNotAnInteger:
                context['objects_list'] = paginator.page(1)
        except EmptyPage:
                context['objects_list'] = paginator.page(paginator.num_pages)
        # End Pagination

        return render(request, template_name, context)

@login_required
def asset_save(request, form, template_name):
        context = {}
        data = dict()
        user = request.user
        if request.method == 'POST':
                form = AssetForm(request.POST)
                if form.is_valid():
                        form = form.save(commit=False)
                        form.code = form.code.upper()
                        form.user = user
                        form.save()
                        messages.success(request, 'Created as successful')
                        form = AssetForm()
                        data['form_is_valid'] = True
                        object_list = Asset.objects.filter(user=user)
                        data['html_objects_list'] = render_to_string('asset/asset_list_itens.html', {
                                'objects_list': object_list
                        })
                else:
                        data['form_is_valid'] = False

        context['form'] = form
        
        data['html_objects'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

@login_required
def asset_add(request):
        if request.method == 'POST':
                form = AssetForm(request.POST)
        else:
                form = AssetForm()
        template_name = 'asset/asset_add.html'
        return asset_save(request, form, template_name)

@login_required
def asset_update(request, pk):
        object_target = get_object_or_404(Asset, pk=pk)
        if request.method == 'POST':
                form = AssetForm(request.POST, instance=object_target)
        else:
                form = AssetForm(instance=object_target)
        template_name = 'asset/asset_update.html'
        return asset_save(request, form, template_name)

@login_required
def asset_delete(request, pk):
    object_target = get_object_or_404(Asset, pk=pk)
    context = {}
    data = dict()
    user = request.user
    if request.method == 'POST':
        object_target.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        object_list = Asset.objects.filter(user=user)
        data['html_objects_list'] = render_to_string('asset/asset_list_itens.html', {
                'objects_list': object_list
        })
    else:
        context['object'] = object_target
        template_name = 'asset/asset_delete.html'
        data['html_objects'] = render_to_string(template_name, context, request=request,)
    return JsonResponse(data)

@login_required
def asset_type(request):
        context = {}
        user = request.user
        if request.method == 'POST':
                form = TypeAssetForm(request.POST)
                if form.is_valid():
                        form = form.save(commit=False)
                        form.user = user
                        form.save()
                        messages.success(request, 'Created as successful')
                        form = TypeAssetForm()
        else:
                form = TypeAssetForm()

        context['form'] = form
        context['objects_list'] = AssetType.objects.filter(user=user)
        template_name = 'asset_type.html'
        return render(request,template_name, context)

@login_required
def yield_type(request):
        context = {}
        user = request.user
        if request.method == 'POST':
                form = YieldTypeForm(request.POST)
                if form.is_valid():
                        form = form.save(commit=False)
                        form.user = user
                        form.save()
                        messages.success(request, 'Created as successful')
                        form = YieldTypeForm()
        else:
                form = YieldTypeForm()

        context['form'] = form
        context['objects_list'] = YieldType.objects.filter(user=user)
        template_name = 'yield_type.html'
        return render(request,template_name, context)

@login_required
def dividend_yield(request):
        context = {}
        user = request.user
        if request.method == 'POST':
                form = DividendYieldForm(request.POST or None)
                if form.is_valid():
                        form = form.save(commit=False)
                        form.user = user
                        form.save()
                        messages.success(request, 'Created as successful')
                        form = DividendYieldForm()
        else:
                form = DividendYieldForm()

        context['form'] = form
        context['objects_list'] = DividendYield.objects.filter(user=user)
        template_name = 'dividend_yield.html'
        return render(request,template_name, context)

@login_required
def broker(request):
        context = {}
        user = request.user
        if request.method == 'POST':
                form = BrokerForm(request.POST or None)
                if form.is_valid():
                        form = form.save(commit=False)
                        form.name = form.name.upper()
                        form.user = user
                        form.save()
                        messages.success(request, 'Created as successful')
                        form = BrokerForm()
        else:
                form = BrokerForm()

        context['form'] = form
        context['objects_list'] = Broker.objects.filter(user=user)
        template_name = 'broker.html'
        return render(request,template_name, context)

@login_required
def brokerraterule(request):
        context = {}
        user = request.user
        if request.method == 'POST':
                form = BrokerRateRuleForm(request.POST or None)
                if form.is_valid():
                        form = form.save(commit=False)
                        if form.greaterthan == None:
                                form.greaterthan = 0
                        
                        if form.lessthan == None:
                                form.lessthan = 999999
                        
                        form.user = user
                        form.save()
                        messages.success(request, 'Created as successful')
                        form = BrokerRateRuleForm()
        else:
                form = BrokerRateRuleForm()

        context['form'] = form
        context['objects_list'] = BrokerRateRule.objects.filter(user=user)
        template_name = 'brokerraterule.html'
        return render(request,template_name, context)

@login_required
def handle_uploaded_file(file):
        df=pd.DataFrame()
        df = pd.read_excel(file)
        for i in range(df.index.stop):
                if (type(df.iloc[i][1]) == int):
                        for f in range(14):
                                id = df.iloc[i][1]
                                stock = df.iloc[i][2]
                                operation_type = df.iloc[i][3]
                                volume = df.iloc[i][4]
                                value_in = df.iloc[i][5]
                                value_out = df.iloc[i][9]
                                print("Id:"+str(id)+ "\n"
                                        "Stock:"+str(stock)+ "\n"
                                        "Op. Type:"+str(operation_type)+ "\n"
                                        "Volume:"+str(volume)+ "\n"
                                        "Value in:"+str(value_in)+ "\n"
                                        "value_out:"+str(value_out))

@login_required
def importtrades(request):
        context = {}
        if request.method == 'POST':
                form = ImportTradesForm(request.POST, request.FILES)
                if form.is_valid():
                        handle_uploaded_file(request.FILES['file'])
                        messages.success(request, 'File imported as successful')
        else:
                form = ImportTradesForm()
        context['form'] = form
        template_name = 'importtrades.html'
        return render(request,template_name,context)

