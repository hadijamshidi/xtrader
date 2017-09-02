from django.db import models
from django.utils import timezone


class StockWatch(models.Model):
    SymbolId = models.CharField(max_length=80)

    InstrumentName = models.CharField(max_length=80)
    InstrumentTitle = models.CharField(max_length=80)
    InstrumentCode = models.CharField(max_length=80)
    InstrumentStateCode = models.CharField(max_length=50)
    InstrumentStateTitle = models.CharField(max_length=50)
    BaseQuantity = models.BigIntegerField()

    pd1 = models.DecimalField(max_digits=7, decimal_places=1)
    zd1 = models.IntegerField()
    qd1 = models.BigIntegerField()
    po1 = models.DecimalField(max_digits=7, decimal_places=1)
    zo1 = models.IntegerField()
    qo1 = models.BigIntegerField()
    pd2 = models.DecimalField(max_digits=7, decimal_places=1)
    zd2 = models.IntegerField()
    qd2 = models.BigIntegerField()
    po2 = models.DecimalField(max_digits=7, decimal_places=1)
    zo2 = models.IntegerField()
    qo2 = models.BigIntegerField()
    pd3 = models.DecimalField(max_digits=7, decimal_places=1)
    zd3 = models.IntegerField()
    qd3 = models.BigIntegerField()
    po3 = models.DecimalField(max_digits=7, decimal_places=1)
    zo3 = models.IntegerField()
    qo3 = models.BigIntegerField()

    # BidAsk = models.

    BuyGroupCount = models.IntegerField()
    BuyGroupVolume = models.BigIntegerField()
    BuyGroupVolumePercentage = models.FloatField()

    BuyFirmCount = models.IntegerField()
    BuyFirmVolume = models.BigIntegerField()
    BuyFirmVolumePercentage = models.FloatField()

    BuyIndividualCount = models.IntegerField()
    BuyIndividualVolume = models.BigIntegerField()
    BuyIndividualVolumePercentage = models.FloatField()

    SellFirmCount = models.IntegerField()
    SellFirmVolume = models.BigIntegerField()
    SellFirmVolumePercentage = models.FloatField()

    SellIndividualCount = models.IntegerField()
    SellIndividualVolume = models.BigIntegerField()
    SellIndividualVolumePercentage = models.FloatField()

    ClosingPrice = models.DecimalField(max_digits=7, decimal_places=1)
    ClosingPriceVariation = models.DecimalField(max_digits=7, decimal_places=1)
    ClosingPriceVariationPercent = models.DecimalField(max_digits=4, decimal_places=2)

    CompanyName = models.CharField(max_length=50)
    ExchangeName = models.CharField(max_length=50)
    ExchangeCode = models.CharField(max_length=50)

    # TODO: change default value  to constant
    LastTradeDate = models.DateField(default=timezone.now)

    FirstTradePrice = models.DecimalField(max_digits=7, decimal_places=1)
    LastTradePrice = models.DecimalField(max_digits=7, decimal_places=1)

    ReferencePrice = models.DecimalField(max_digits=7, decimal_places=1)
    ReferencePriceVariation = models.DecimalField(max_digits=7, decimal_places=1)
    ReferencePriceVariationPercent = models.DecimalField(max_digits=4, decimal_places=2)

    YearHighestTradePrice = models.DecimalField(max_digits=7, decimal_places=1)
    YearLowestTradePrice = models.DecimalField(max_digits=7, decimal_places=1)

    MinimumOrderQuantity = models.BigIntegerField()
    MaximumOrderQuantity = models.BigIntegerField()

    LowerPriceThreshold = models.DecimalField(max_digits=7, decimal_places=1)
    UpperPriceThreshold = models.DecimalField(max_digits=7, decimal_places=1)

    LowestTradePrice = models.DecimalField(max_digits=7, decimal_places=1)
    HighestTradePrice = models.DecimalField(max_digits=7, decimal_places=1)

    PreviousDayPrice = models.DecimalField(max_digits=7, decimal_places=1)
    TotalNumberOfSharesTraded = models.BigIntegerField()
    TotalNumberOfTrades = models.BigIntegerField()
    TotalTradeValue = models.BigIntegerField()
    Eps = models.IntegerField()
    PricePerEarningGroup = models.DecimalField(max_digits=4, decimal_places=2)
    PricePerEarning = models.DecimalField(max_digits=4, decimal_places=2)
    FreeFloatPercent = models.DecimalField(max_digits=4, decimal_places=2)
    MonthAverageVolume = models.BigIntegerField()
    InstrumentMarketValue = models.BigIntegerField()
    NumberOfSharesOrBonds = models.BigIntegerField()

    def __str__(self):
        return self.SymbolId

    def to_dict(self):
        obj_dict = {'SymbolId': self.SymbolId}
        return obj_dict

    def dict(self, keys, date):
        d = {}
        if str(self.LastTradeDate) == date:
            for key in keys:
                try:
                    d[key] = float(self.__getattribute__(key))
                except Exception:
                    d[key] = self.__getattribute__(key)
            return d
        else:
            return 'wrong symbol'

    def as_json(self):
        return dict(
            symbol_id=self.SymbolId,
            kind=self.InstrumentStateTitle,
            category=self.ExchangeName,
            symbol_name=self.InstrumentName,
            name=self.CompanyName,
            description=self.CompanyName,
            title='title',
        )

    def read(self):
        data = {}
        for key in self.__dict__:
            if key[0] != '_':
                try:
                    data[key] = float(self.__getattribute__(key))
                except Exception:
                    value = self.__getattribute__(key)
                    if value == None:
                        data[key] = 0
                    else:
                        data[key] = str(value)
        return data


class BalanceSheet(models.Model):
    StockWatch = models.ForeignKey(StockWatch, verbose_name='سهم ')
    SymbolId = models.CharField(max_length=80, null=True, blank=True)
    InstrumentName = models.CharField(max_length=80)
    cash = models.IntegerField(verbose_name='وجه نقد', null=True, blank=True)
    net_receivables = models.IntegerField(verbose_name='حساب های دریافتی', null=True, blank=True)
    short_term_investments = models.IntegerField(verbose_name='سرمایه های کوتاه مدت', null=True, blank=True)
    total_current_assets = models.IntegerField(verbose_name='دارایی های جاری ', null=True, blank=True)
    inventory = models.IntegerField(verbose_name='موجودی کالا', null=True, blank=True)
    long_term_investments = models.IntegerField(verbose_name='سرمایه گذاری بلند مدت', null=True, blank=True)
    property_plant_and_equipment = models.IntegerField(verbose_name='دادای های ثابت', null=True, blank=True)
    intangible_assets = models.IntegerField(verbose_name='دارایی های نامشهود', null=True, blank=True)
    total_assets = models.IntegerField(verbose_name='دارایی ', null=True, blank=True)
    accounts_payable = models.IntegerField(verbose_name='حساب های پرداختنی', null=True, blank=True)
    total_current_liabilities = models.IntegerField(verbose_name='بدهی جاری ', null=True, blank=True)
    total_liabilities = models.IntegerField(verbose_name='بدهی', null=True, blank=True)
    capital = models.IntegerField(verbose_name='سرمایه', null=True, blank=True)
    retained_earnings = models.IntegerField(verbose_name='سود انباشته', null=True, blank=True)
    equity = models.IntegerField(verbose_name='حقوق صاحبان سرمایه', null=True, blank=True)
    prepayment = models.IntegerField(verbose_name='پیش پرداخت', null=True, blank=True)
    def read(self):
        data = {}
        for key in self.__dict__:
            if key[0] != '_':
                try:
                    data[key] = float(self.__getattribute__(key))
                except Exception:
                    value = self.__getattribute__(key)
                    if value == None:
                        data[key] = 0
                    else:
                        data[key] = str(value)
        return data
class Income(models.Model):
    StockWatch = models.ForeignKey(StockWatch, verbose_name='سهم ')
    SymbolId = models.CharField(max_length=80, null=True, blank=True)
    InstrumentName = models.CharField(max_length=80)
    total_income = models.IntegerField(verbose_name='فروش', null=True, blank=True)
    gross_profit = models.IntegerField(verbose_name='سود ناخالص', null=True, blank=True)
    operating_income_or_loss = models.IntegerField(verbose_name='سود عملیاتی', null=True, blank=True)
    interest_expense = models.IntegerField(verbose_name='هزینه های مالی ', null=True, blank=True)
    income_before_tax = models.IntegerField(verbose_name='سود قبل از مالیات', null=True, blank=True)
    net_income = models.IntegerField(verbose_name='سود خالص', null=True, blank=True)
    def read(self):
        data = {}
        for key in self.__dict__:
            if key[0] != '_':
                try:
                    data[key] = float(self.__getattribute__(key))
                except Exception:
                    value = self.__getattribute__(key)
                    if value == None:
                        data[key] = 0
                    else:
                        data[key] = str(value)
        return data


class Ratio(models.Model):
    StockWatch = models.ForeignKey(StockWatch, verbose_name='سهم ')
    SymbolId = models.CharField(max_length=80, null=True, blank=True)
    InstrumentName = models.CharField(max_length=80)
    current_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='جاری', null=True, blank=True)
    quick_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='آنی', null=True, blank=True)
    cash_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='نقد', null=True, blank=True)
    da = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='بدهی (درصد)', null=True, blank=True)
    de = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='بدهی به ح ص س', null=True, blank=True)
    sa = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='گردش دارای (بار)', null=True, blank=True)
    accounts_receivable_turnover_ratio = models.IntegerField(verbose_name='دوره گردش دریافتنی (روز)', null=True,
                                                             blank=True)
    accounts_payable_turnover_ratio = models.DecimalField(max_digits=5, decimal_places=2,
                                                          verbose_name='حاشیه سود خالص (درصد)', null=True, blank=True)
    inventory_turnover_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='دوره گردش موحودی ',
                                                   null=True, blank=True)
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='حاشیه سود خالص (درصد)', null=True,
                                        blank=True)
    gross_profit_margin = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='حاشیه سود ناخالص (درصد)',
                                              null=True, blank=True)
    ebit_gross_profit = models.DecimalField(max_digits=5, decimal_places=2,
                                            verbose_name='سود عملیاتی به سود ناخالص (درصد)', null=True, blank=True)
    r_ebit = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='هزینه بهره به سود عملیاتی (درصد)',
                                 null=True, blank=True)
    roa = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='بازده دارایی (درصد)', null=True, blank=True)
    roe = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='بازده ح ص س (درصد)', null=True, blank=True)
    def read(self):
        data = {}
        for key in self.__dict__:
            if key[0] != '_':
                try:
                    data[key] = float(self.__getattribute__(key))
                except Exception:
                    value = self.__getattribute__(key)
                    if value == None:
                        data[key] = 0
                    else:
                        data[key] = str(value)
        return data

class MarketWatch(models.Model):
    stockWatch = models.ForeignKey(StockWatch, null=True, blank=True)
    balanceSheet = models.ForeignKey(BalanceSheet, null=True, blank=True)
    ratio = models.ForeignKey(Ratio, null=True, blank=True)
    income = models.ForeignKey(Income, null=True, blank=True)

    def get_instrument_name(self):
        return self.stockWatch.InstrumentName

    def get_SymbolId(self):
        return self.stockWatch.SymbolId

    def get_CompanyName(self):
        return self.stockWatch.CompanyName
