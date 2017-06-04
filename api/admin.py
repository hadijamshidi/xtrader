from django.contrib import admin

# Register your models here.
from api.models import Stock

admin.site.register(Stock)
admin.site.register(MarketWatch)