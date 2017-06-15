from task import update_history as up
from api.models import MarketWatch
from datetime import datetime, timedelta
from finance.models import Strategy
from django.contrib.auth.models import User


def scan_market(user_name, strategy_name):
    filters = find_strategy_filters(user_name, strategy_name)
    symbol_ids = find_symbol_ids()
    for symbol_id in symbol_ids:
        for given_filter in filters:
            given_filter['symbol_id'] = symbol_id

    pass


def find_strategy_filters(user_name, strategy_name):
    trader = User.objects.get_by_natural_key(username=user_name)
    strategy = Strategy.objects.get(trader=trader, name=strategy_name).loads()
    return strategy['filters']


def find_symbol_ids():
    symbol_ids = MarketWatch.objects.filter(LastTradeDate=str(datetime.today() - timedelta(1))).values('SymbolId')
    return [symbol_id['SymbolId'] for symbol_id in symbol_ids]