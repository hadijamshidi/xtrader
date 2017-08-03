from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(StockWatch)
admin.site.register(Ratio)
admin.site.register(Income)
admin.site.register(BalanceSheet)
admin.site.register(MarketWatch)

