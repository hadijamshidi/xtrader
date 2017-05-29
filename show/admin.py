from django.contrib import admin
from show.models import company,intradaytrades
# Register your models here.
def getdata(self, request, queryset):

    sendsms = request.POST.get('copmanyid')
    import show.getData as f
    f.company_data()


getdata.short_description = ('گرفتن اطاعات شرکت')

class Company_Admin(admin.ModelAdmin):
    list_display = ['id1', 'name',  'english_name', 'short_name','english_short_name','trade_symbol','state','exchange','categories']
    list_filter = ['name']
    actions = [getdata]

    # inlines = [ManagementInline]
admin.site.register(company, Company_Admin)
class Intradaytrades_Admin(admin.ModelAdmin):
    list_display = ['instrument', 'date_time','close_price','real_close_price','volume','value','metaversion']
    list_filter = ['close_price']

    # inlines = [ManagementInline]
admin.site.register(intradaytrades, Intradaytrades_Admin)
