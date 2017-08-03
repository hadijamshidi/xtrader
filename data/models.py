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
            description='description',
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
    stockwatch_SymbolId = models.CharField(max_length=80)

    stockwatch_InstrumentName = models.CharField(max_length=80)
    stockwatch_InstrumentTitle = models.CharField(max_length=80)
    stockwatch_InstrumentCode = models.CharField(max_length=80)
    stockwatch_InstrumentStateCode = models.CharField(max_length=50)
    stockwatch_InstrumentStateTitle = models.CharField(max_length=50)
    stockwatch_BaseQuantity = models.BigIntegerField(null=True,blank=True)

    stockwatch_pd1 = models.DecimalField(max_digits=7, decimal_places=1)
    stockwatch_zd1 = models.IntegerField()
    stockwatch_qd1 = models.BigIntegerField()
    stockwatch_po1 = models.DecimalField(max_digits=7, decimal_places=1)
    stockwatch_zo1 = models.IntegerField()
    stockwatch_qo1 = models.BigIntegerField()
    stockwatch_pd2 = models.DecimalField(max_digits=7, decimal_places=1)
    stockwatch_zd2 = models.IntegerField()
    stockwatch_qd2 = models.BigIntegerField()
    stockwatch_po2 = models.DecimalField(max_digits=7, decimal_places=1)
    stockwatch_zo2 = models.IntegerField()
    stockwatch_qo2 = models.BigIntegerField()
    stockwatch_pd3 = models.DecimalField(max_digits=7, decimal_places=1)
    stockwatch_zd3 = models.IntegerField()
    stockwatch_qd3 = models.BigIntegerField()
    stockwatch_po3 = models.DecimalField(max_digits=7, decimal_places=1)
    stockwatch_zo3 = models.IntegerField()
    stockwatch_qo3 = models.BigIntegerField()

    # BidAsk = models.

    stockwatch_BuyGroupCount = models.IntegerField()
    stockwatch_BuyGroupVolume = models.BigIntegerField()
    stockwatch_BuyGroupVolumePercentage = models.FloatField()

    stockwatch_BuyFirmCount = models.IntegerField()
    stockwatch_BuyFirmVolume = models.BigIntegerField()
    stockwatch_BuyFirmVolumePercentage = models.FloatField()

    stockwatch_BuyIndividualCount = models.IntegerField()
    stockwatch_BuyIndividualVolume = models.BigIntegerField()
    stockwatch_BuyIndividualVolumePercentage = models.FloatField()

    stockwatch_SellFirmCount = models.IntegerField()
    stockwatch_SellFirmVolume = models.BigIntegerField()
    stockwatch_SellFirmVolumePercentage = models.FloatField()

    stockwatch_SellIndividualCount = models.IntegerField()
    stockwatch_SellIndividualVolume = models.BigIntegerField()
    stockwatch_SellIndividualVolumePercentage = models.FloatField()

    stockwatch_ClosingPrice = models.DecimalField(max_digits=7, decimal_places=1)
    stockwatch_ClosingPriceVariation = models.DecimalField(max_digits=7, decimal_places=1)
    stockwatch_ClosingPriceVariationPercent = models.DecimalField(max_digits=4, decimal_places=2)

    stockwatch_CompanyName = models.CharField(max_length=50)
    stockwatch_ExchangeName = models.CharField(max_length=50)
    stockwatch_ExchangeCode = models.CharField(max_length=50)

    # TODO: change default value  to constant
    stockwatch_LastTradeDate = models.DateField(default=timezone.now)

    stockwatch_FirstTradePrice = models.DecimalField(max_digits=7, decimal_places=1)
    stockwatch_LastTradePrice = models.DecimalField(max_digits=7, decimal_places=1)

    stockwatch_ReferencePrice = models.DecimalField(max_digits=7, decimal_places=1)
    stockwatch_ReferencePriceVariation = models.DecimalField(max_digits=7, decimal_places=1)
    stockwatch_ReferencePriceVariationPercent = models.DecimalField(max_digits=4, decimal_places=2)

    stockwatch_YearHighestTradePrice = models.DecimalField(max_digits=7, decimal_places=1)
    stockwatch_YearLowestTradePrice = models.DecimalField(max_digits=7, decimal_places=1)

    stockwatch_MinimumOrderQuantity = models.BigIntegerField()
    stockwatch_MaximumOrderQuantity = models.BigIntegerField()

    stockwatch_LowerPriceThreshold = models.DecimalField(max_digits=7, decimal_places=1)
    stockwatch_UpperPriceThreshold = models.DecimalField(max_digits=7, decimal_places=1)

    stockwatch_LowestTradePrice = models.DecimalField(max_digits=7, decimal_places=1)
    stockwatch_HighestTradePrice = models.DecimalField(max_digits=7, decimal_places=1)

    stockwatch_PreviousDayPrice = models.DecimalField(max_digits=7, decimal_places=1)
    stockwatch_TotalNumberOfSharesTraded = models.BigIntegerField()
    stockwatch_TotalNumberOfTrades = models.BigIntegerField()
    stockwatch_TotalTradeValue = models.BigIntegerField()
    stockwatch_Eps = models.IntegerField()
    stockwatch_PricePerEarningGroup = models.DecimalField(max_digits=4, decimal_places=2)
    stockwatch_PricePerEarning = models.DecimalField(max_digits=4, decimal_places=2)
    stockwatch_FreeFloatPercent = models.DecimalField(max_digits=4, decimal_places=2)
    stockwatch_MonthAverageVolume = models.BigIntegerField()
    stockwatch_InstrumentMarketValue = models.BigIntegerField()
    stockwatch_NumberOfSharesOrBonds = models.BigIntegerField()

    ratio_current_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='جاری', null=True,
                                              blank=True)
    ratio_quick_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='آنی', null=True, blank=True)
    ratio_cash_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='نقد', null=True, blank=True)
    ratio_da = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='بدهی (درصد)', null=True, blank=True)
    ratio_de = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='بدهی به ح ص س', null=True, blank=True)
    ratio_sa = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='گردش دارای (بار)', null=True,
                                   blank=True)
    ratio_accounts_receivable_turnover_ratio = models.IntegerField(verbose_name='دوره گردش دریافتنی (روز)', null=True,
                                                                   blank=True)
    ratio_accounts_payable_turnover_ratio = models.DecimalField(max_digits=5, decimal_places=2,
                                                                verbose_name='حاشیه سود خالص (درصد)', null=True,
                                                                blank=True)
    ratio_inventory_turnover_ratio = models.DecimalField(max_digits=5, decimal_places=2,
                                                         verbose_name='دوره گردش موحودی ', null=True, blank=True)
    ratio_profit_margin = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='حاشیه سود خالص (درصد)',
                                              null=True, blank=True)
    ratio_gross_profit_margin = models.DecimalField(max_digits=5, decimal_places=2,
                                                    verbose_name='حاشیه سود ناخالص (درصد)', null=True, blank=True)
    ratio_ebit_gross_profit = models.DecimalField(max_digits=5, decimal_places=2,
                                                  verbose_name='سود عملیاتی به سود ناخالص (درصد)', null=True,
                                                  blank=True)
    ratio_r_ebit = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='هزینه بهره به سود عملیاتی (درصد)',
                                       null=True, blank=True)
    ratio_roa = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='بازده دارایی (درصد)', null=True,
                                    blank=True)
    ratio_roe = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='بازده ح ص س (درصد)', null=True,
                                    blank=True)

    income_total_income = models.IntegerField(verbose_name='فروش', null=True, blank=True)
    income_gross_profit = models.IntegerField(verbose_name='سود ناخالص', null=True, blank=True)
    income_operating_income_or_loss = models.IntegerField(verbose_name='سود عملیاتی', null=True, blank=True)
    income_interest_expense = models.IntegerField(verbose_name='هزینه های مالی ', null=True, blank=True)
    income_income_before_tax = models.IntegerField(verbose_name='سود قبل از مالیات', null=True, blank=True)
    income_net_income = models.IntegerField(verbose_name='سود خالص', null=True, blank=True)

    balanceSheet_cash = models.IntegerField(verbose_name='وجه نقد', null=True, blank=True)
    balanceSheet_net_receivables = models.IntegerField(verbose_name='حساب های دریافتی', null=True, blank=True)
    balanceSheet_short_term_investments = models.IntegerField(verbose_name='سرمایه های کوتاه مدت', null=True,
                                                              blank=True)
    balanceSheet_total_current_assets = models.IntegerField(verbose_name='دارایی های جاری ', null=True, blank=True)
    balanceSheet_inventory = models.IntegerField(verbose_name='موجودی کالا', null=True, blank=True)
    balanceSheet_long_term_investments = models.IntegerField(verbose_name='سرمایه گذاری بلند مدت', null=True,
                                                             blank=True)
    balanceSheet_property_plant_and_equipment = models.IntegerField(verbose_name='دادای های ثابت', null=True,
                                                                    blank=True)
    balanceSheet_intangible_assets = models.IntegerField(verbose_name='دارایی های نامشهود', null=True, blank=True)
    balanceSheet_total_assets = models.IntegerField(verbose_name='دارایی ', null=True, blank=True)
    balanceSheet_accounts_payable = models.IntegerField(verbose_name='حساب های پرداختنی', null=True, blank=True)
    balanceSheet_total_current_liabilities = models.IntegerField(verbose_name='بدهی جاری ', null=True, blank=True)
    balanceSheet_total_liabilities = models.IntegerField(verbose_name='بدهی', null=True, blank=True)
    balanceSheet_capital = models.IntegerField(verbose_name='سرمایه', null=True, blank=True)
    balanceSheet_retained_earnings = models.IntegerField(verbose_name='سود انباشته', null=True, blank=True)
    balanceSheet_equity = models.IntegerField(verbose_name='حقوق صاحبان سرمایه', null=True, blank=True)
    balanceSheet_prepayment = models.IntegerField(verbose_name='پیش پرداخت', null=True, blank=True)

    def __str__(self):
        return self.stockwatch_SymbolId

    def to_dict(self):
        obj_dict = {'stockwatch_SymbolId': self.stockwatch_SymbolId}
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
            symbol_id=self.stockwatch_SymbolId,
            kind='kind',
            category=self.ExchangeName,
            symbol_name=self.InstrumentName,
            name=self.InstrumentName,
            description='description',
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
