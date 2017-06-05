from django.contrib import admin

# Register your models here.
from api.models import Stock,MarketWatch


class Stock_Admin(admin.ModelAdmin):
    list_display = ['symbol_id', 'isin', 'mabna_id', 'mabna_name', 'mabna_english_name', 'mabna_short_name', 'mabna_kind']

admin.site.register(Stock, Stock_Admin)
class MarketWatch_Admin(admin.ModelAdmin):
    list_display = ['SymbolId', 'LastTradeDate', 'FirstTradePrice']

admin.site.register(MarketWatch, MarketWatch_Admin)