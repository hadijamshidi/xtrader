from django.db import models
# from datetime import datetime
from django.utils import timezone

# Create your models here.
class Stock(models.Model):
    symbol_id = models.CharField(max_length=80, unique=True)
    isin = models.CharField(max_length=80)
    mabna_id = models.CharField(max_length=80)
    mabna_name = models.CharField(max_length=80)
    mabna_english_name = models.CharField(max_length=80)
    mabna_short_name = models.CharField(max_length=80)
    mabna_kind = models.CharField(max_length=80, default='Nan')

    def as_json(self):
        return dict(
            id=self.mabna_id,
            # TODO: be careful
            symbol_id=self.symbol_id,
            eng_name=self.mabna_english_name,
            # eng_name=self.symbol_id,
            kind='kind',
            category='سهام',
            symbol_name=self.mabna_short_name, name=self.mabna_name,
            description= self.mabna_name,
            title=self.mabna_short_name,
        )

    def __str__(self):
        return self.symbol_id


class MarketWatch(models.Model):
    # isin = models.CharField(max_length=80)
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
    LastTradeDate = models.DateField(default=timezone.now())

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


class Status(models.Model):
    market_watch = models.CharField(max_length=50)
    job = models.CharField(max_length=50)
    market_watch_updating_permission = models.CharField(max_length=50, default='allowed')
    number_of_requests = models.IntegerField(default=0)

    def permision(self):
        if self.market_watch_updating_permission == 'allowed':
            return True
        else:
            return False
