from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Manager classes
class AssetManager (models.Manager):
    def search(self, query):
        return self.get_queryset().filter(name__icontains=query)

class AssetTypeManager (models.Manager):
    def search(self, query):
        return self.get_queryset().filter(name__icontains=query)

class YieldTypeManager (models.Manager):
    def search(self, query):
        return self.get_queryset().filter(name__icontains=query)
class DividendYieldManager (models.Manager):
    def search(self, query):
        return self.get_queryset().filter(name__icontains=query)

class BalanceManager (models.Manager):
    def search(self, query):
        return self.get_queryset().filter(name__icontains=query)

class BrokerManager (models.Manager):
    def search(self, query):
        return self.get_queryset().filter(name__icontains=query)

class OrderManager (models.Manager):
    def search(self, query):
        return self.get_queryset().filter(name__icontains=query)

class BrokerRateRuleManager (models.Manager):
    def search(self, query):
        return self.get_queryset().filter(name__icontains=query)

class PositionManager (models.Manager):
    def search(self, query):
        return self.get_queryset().filter(name__icontains=query)

class TaxManager (models.Manager):
    def search(self, query):
        return self.get_queryset().filter(name__icontains=query)

class LanguageManager (models.Manager):
    def search(self, query):
        return self.get_queryset().filter(name__icontains=query)

                
# Database Classes
class AssetType(models.Model):
    CHOICE_IS_DEFAULT = [
        ('y','Yes'),
        ('n','No')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.SlugField('Name', max_length=100)
    is_default = models.CharField('Default', default='n', max_length=1, choices=CHOICE_IS_DEFAULT, blank=True, null=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    objects = AssetTypeManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Asset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    code = models.SlugField('Code', max_length=30)
    name = models.CharField('Corporate name', max_length=200, null=True, blank=True)
    cnpj = models.CharField('CNPJ', max_length=38, null=True, blank=True)
    type = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)
    objects = AssetManager()
    
    def __str__(self):
        return self.code

    class Meta:
        ordering = ['code']

class YieldType(models.Model):
    CHOICE_IS_DEFAULT = [
        ('y','Yes'),
        ('n','No')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField('Yield type', max_length=50)
    is_default = models.CharField('Default', default='n', max_length=1, choices=CHOICE_IS_DEFAULT, blank=True, null=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    objects = YieldTypeManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class DividendYield(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    yield_typpe = models.ForeignKey(YieldType, on_delete=models.CASCADE, default=1)
    value = models.FloatField('Value')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    paid_in = models.DateField('Paid in', editable=True)
    objects = DividendYieldManager()

    # class Meta:
    #     unique_together = (('user', 'asset'),)

class Balance(models.Model):
    CHOICE_IS_DEFAULT = [
        ('n','Normal'),
        ('d','Day trade')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    type = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    balance = models.FloatField('Balance value')
    tax_to_pay = models.FloatField('Tax to pay')
    type_operation = models.CharField('Operation type', max_length=1, choices=CHOICE_IS_DEFAULT)
    reference_date = models.DateField('Reference date')
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    objects = BalanceManager()

    # def __str__(self):
    #     return self.balance

    class Meta:
        ordering = ['created_at']

class Broker(models.Model):
    CHOICE_IS_DEFAULT = [
        ('y','Yes'),
        ('n','No')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.SlugField('Name', max_length=100)
    cnpj = models.CharField('CNPJ', max_length=38, null=True, blank=True)
    is_default = models.CharField('Is it defalt?', max_length=1, default='n', choices=CHOICE_IS_DEFAULT)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    objects = BrokerManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Order(models.Model):
    OPERATION_TYPE = [
        ('b','Buy'),
        ('s','Sale'),
        ('r','Rent')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    operation_type = models.CharField('Operation type', max_length=1, choices=OPERATION_TYPE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    amount = models.IntegerField('Amount')
    value = models.FloatField('Value')
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    brokerrate = models.FloatField('Broker rate')
    emolument = models.FloatField('Emolument', default=0)
    operated_at = models.DateField('Operation time')
    updated_at = models.DateTimeField('Updated at', auto_now=True)
    objects = OrderManager()
    
    def total(self):
        return self.amount * self.value
    
    class Meta:
        ordering = ['-updated_at']

class BrokerRateRule(models.Model):
    ORDER_TYPE = [
        ('d','Daytrade'),
        ('n','Normal'),
        ('r','Rent')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    ordertype = models.CharField('Order type', max_length=1, choices=ORDER_TYPE)
    assettype = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    greaterthan = models.FloatField('Greater than', null=True, blank=True)
    lessthan = models.FloatField('Less than', null=True, blank=True)
    rate = models.FloatField('Broker rate')
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)
    objects = BrokerRateRuleManager()

class Position(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    type = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    balance = models.FloatField('Balance')
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    regarding_at = models.DateTimeField('Regarding at')
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    objects = PositionManager()
        
    # def __str__(self):
    #     return self.value

    class Meta:
        ordering = ['created_at']

class Tax(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField('Name', max_length=30)
    reference_date = models.DateField('Reference date')
    value = models.FloatField('Value')
    interest_rate = models.FloatField('Value')
    payment_date = models.DateField('Reference date')
    objects = TaxManager()
        
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Language(models.Model):
    name = models.SlugField('Name', max_length=50, null=False, blank=False)
    value = models.TextField('Value', null=False, blank=False)
    language = models.CharField('Lang', max_length=2, null=False, blank=False)
    objects = LanguageManager()
        
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']