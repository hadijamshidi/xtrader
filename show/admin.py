from django.contrib import admin
from show.models import company,intradaytrades
# Register your models here.
class Company_Admin(admin.ModelAdmin):
    list_display = ['id1', 'name',  'english_name', 'short_name','english_short_name','trade_symbol','state','exchange','categories']
    list_filter = ['name']

    # inlines = [ManagementInline]
admin.site.register(company, Company_Admin)
class Intradaytrades_Admin(admin.ModelAdmin):
    list_display = ['id1', 'trade',  'instrument', 'date_time','close_price','real_close_price','volume','value','metaversion']
    list_filter = ['trade']

    # inlines = [ManagementInline]
admin.site.register(intradaytrades, Intradaytrades_Admin)