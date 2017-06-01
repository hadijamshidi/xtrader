from django.db import models


# Create your models here.
class Stock(models.Model):
    symbol_id = models.CharField(max_length=80, unique=True)
    isin = models.CharField(max_length=80)
    mabna_id = models.CharField(max_length=80)
    mabna_name = models.CharField(max_length=80)
    mabna_english_name = models.CharField(max_length=80)
    mabna_short_name = models.CharField(max_length=80)
    mabna_kind = models.CharField(max_length=80, default='Nan')


class MarketWatch(models.Model):
    # isin = models.CharField(max_length=80)
    symbol_id = models.CharField(max_length=80)
    # TODO: setting FloatField for tow decimal: 1.22 and handle decimal and optional Fields

    # instrument_name = models.CharField(max_length=80)
    # instrument_title = models.CharField(max_length=80)
    # instrument_code = models.CharField(max_length=80)
    # instrument_state_code = models.CharField(max_length=50)
    # instrument_state_title = models.CharField(max_length=50)
    # base_quantity = models.FloatField()
    # TODO: BidAsk model:
    # BidAsk = models.

    # buy_group_count = models.IntegerField()
    # buy_group_volume = models.BigIntegerField()
    # buy_group_volume_percentage = models.FloatField()
    #
    # buy_firm_count = models.IntegerField()
    # buy_firm_volume = models.BigIntegerField()
    # buy_firm_volume_percentage = models.FloatField()
    #
    # buy_individual_count = models.IntegerField()
    # buy_individual_volume = models.BigIntegerField()
    # buy_individual_volume_percentage = models.FloatField()
    #
    # sell_firm_count = models.IntegerField()
    # sell_firm_volume = models.BigIntegerField()
    # sell_firm_volume_percentage = models.FloatField()
    #
    # sell_individual_count = models.IntegerField()
    # sell_individual_volume = models.BigIntegerField()
    # sell_individual_volume_percentage = models.FloatField()

    closing_price = models.IntegerField()
    # closing_price_variation = models.IntegerField()
    # closing_price_variation_percent = models.FloatField()

    # company_name = models.CharField(max_length=50)
    # exchange_name = models.CharField(max_length=50)
    # exchange_code = models.CharField(max_length=50)

    # last_trade_date = models.DateField()

    first_trade_price = models.IntegerField()
    last_trade_price = models.IntegerField()

    # reference_price = models.IntegerField()
    # reference_price_variation = models.IntegerField()
    # reference_price_variation_percent = models.FloatField()

    # year_highest_trade_price = models.IntegerField()
    # year_lowest_trade_price = models.IntegerField()
    #
    # MinimumOrderQuantity = models.BigIntegerField()
    # MaximumOrderQuantity = models.BigIntegerField()
    #
    # LowerPriceThreshold = models.IntegerField()
    # UpperPriceThreshold = models.IntegerField()

    lowest_trade_price = models.IntegerField()
    highest_trade_price = models.IntegerField()

    # previous_day_price = models.IntegerField()
    # total_number_of_shares_traded = models.BigIntegerField()
    # total_number_of_trades = models.BigIntegerField()
    # total_trade_value = models.BigIntegerField()
    # eps = models.IntegerField()
    # price_per_earning_group = models.FloatField()
    # price_per_earning = models.FloatField()
    # free_float_percent = models.FloatField()
    # month_average_volume = models.BigIntegerField()
    # instrument_market_value = models.BigIntegerField()
    # number_of_shares_or_bonds = models.BigIntegerField()
