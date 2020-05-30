from django import forms
from .models import AssetType, Asset, YieldType, DividendYield, Balance, Broker, Order, BrokerRateRule, Position,Tax, Language

class DateInput(forms.DateInput):
    input_type = 'date'
    
class TypeAssetForm(forms.ModelForm):
    class Meta:
        model = AssetType
        fields = ['name', 'is_default']

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['type', 'code', 'name','cnpj']

class YieldTypeForm(forms.ModelForm):
    class Meta:
        model = YieldType
        fields = ['name', 'is_default']

class DividendYieldForm(forms.ModelForm):
    class Meta:
        model = DividendYield
        fields = ['value', 'asset','paid_in']
        widgets = {
            'paid_in': DateInput()
        }

class BrokerForm(forms.ModelForm):
    class Meta:
        model = Broker
        fields = ['name', 'cnpj', 'is_default']
    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['operation_type','operated_at', 'asset', 'amount','value','broker']
        widgets = {
            'operated_at': DateInput()
        }

class BrokerRateRuleForm(forms.ModelForm):
    class Meta:
        model = BrokerRateRule
        fields = ['ordertype', 'assettype', 'broker', 'greaterthan', 'lessthan', 'rate']