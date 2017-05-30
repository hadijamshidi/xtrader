from django.contrib import admin
from show.models import Company, Intradaytrades , Isin


# Register your models here.
def getdata(self, request, queryset):

    import show.getData as f
    f.company_data(1,500)


getdata.short_description = ('گرفتن اطاعات شرکت')
def getdataisin(self, request, queryset):

    import show.getData as f
    f.isin_data(1,2)


getdataisin.short_description = ('گرفتن اطاعات نماد')



class Company_Admin(admin.ModelAdmin):
    list_display = ['id1', 'name', 'english_name', 'short_name', 'english_short_name', 'trade_symbol', 'state',
                    'exchange', 'categories']
    list_filter = ['categories']
    actions = [getdata]

    # inlines = [ManagementInline]


admin.site.register(Company, Company_Admin)


class Intradaytrades_Admin(admin.ModelAdmin):
    list_display = ['company','instrument', 'date_time', 'close_price', 'real_close_price', 'volume', 'value', 'metaversion']
    list_filter = ['close_price']

    # inlines = [ManagementInline]


admin.site.register(Intradaytrades, Intradaytrades_Admin)
class  Isin_Admin(admin.ModelAdmin):
    list_display = ['company','name', 'code', 'english_name', 'isin']
    actions = [getdataisin]

    # inlines = [ManagementInline]


admin.site.register(Isin, Isin_Admin)

