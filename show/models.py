from django.db import models

# Create your models here.
class company(models.Model):
    id1 = models.IntegerField(verbose_name='id')
    name = models.CharField(max_length=80,verbose_name='نام شرکت')
    english_name = models.CharField(max_length=80,verbose_name='نام انگلیسی شرکت')
    short_name = models.CharField(max_length=80,verbose_name='نام کوتاه شرکت')
    english_short_name = models.CharField(max_length=80,verbose_name='نام کوتاه انگلیسی شرکت')
    trade_symbol = models.CharField(max_length=80,verbose_name='نماد معاملاتی')
    english_trade_symbol = models.CharField(max_length=80,verbose_name='نماد معاملاتی انگلیسی')
    state = models.CharField(max_length=80,verbose_name='وضعیت شرکت')
    exchange = models.CharField(max_length=80,verbose_name='بازار معاملاتی')
    categories = models.CharField( max_length=80,verbose_name='دسته بندی‌ها')
    metaversion = models.CharField(max_length=80,verbose_name='اطلاعات رکورد')
class intradaytrades(models.Model):
    id1 = models.IntegerField(verbose_name='id')
    trade = models.CharField(max_length=80,verbose_name='معامله روزانه')
    instrument = models.CharField(max_length=80,verbose_name='نماد')
    date_time = models.CharField(max_length=80,verbose_name='زمان انجام معامله')
    close_price = models.CharField(max_length=80,verbose_name='آخرین قیمت')
    real_close_price = models.CharField(max_length=80,verbose_name='قیمت پایانی')
    volume = models.CharField(max_length=80,verbose_name='تعداد معامله شده')
    value = models.CharField(max_length=80,verbose_name='ارزش معامله شده')
    metaversion = models.CharField(max_length=80,verbose_name='اطلاعات رکورد')
    def update(self):
        import requests as a
        r = a.get("http://66.70.160.142:8000/mabna/api",
                  params={'url': '/exchange/intradaytrades?_sort=meta.version&meta.version='+str(self.metaversion)+'&meta.version_op=gt'})
