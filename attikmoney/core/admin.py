from django.contrib import admin

from .models import *
# Register your models here.
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name','is_default','created_at']
    search_fields = ['name']

admin.site.register(AssetType)
admin.site.register(Asset)
admin.site.register(DividendYield)
admin.site.register(Balance)
admin.site.register(Broker)
admin.site.register(Order)
admin.site.register(BrokerRateRule)
admin.site.register(Position)
admin.site.register(Tax)
admin.site.register(Language)
