# from task import update_history as up
from api.models import MarketWatch, Stock
from datetime import datetime, timedelta
from finance.models import Strategy
from django.contrib.auth.models import User
from . import data_handling as dh, notification as notif
import inspect


def scan_market(user_name, strategy_name):
    filters = find_strategy_filters(user_name, strategy_name)
    symbol_ids = find_symbol_ids()
    scan_result = {'buy': [], 'sell': []}
    for id_index, symbol_id in enumerate(symbol_ids):
        first_kind_dict, second_kind_dict, final_dict = {}, {}, {}
        first, second, bad_symbol = False, False, False
        for index, strategy_filter in enumerate(filters):
            print('filter: {}, for symbol: {}'.format(index, id_index))
            strategy_filter['symbol_id'] = symbol_id
            try:
                result = calculate_filter_result(strategy_filter)
            except Exception:
                print('bad symbol !! filter: {}, for symbol: {}'.format(index, id_index))
                bad_symbol = True
                continue
            if result['type'] == 'first':
                first_kind_dict['filter-first {}'.format(index)] = notif.make_list_ready(result['result'])
                first = True
            if result['type'] == 'second':
                second_kind_dict['filter-second {}'.format(index)] = notif.make_list_ready(result['result'])
                second = True
        if first:
            final_dict['first'] = notif.check_first_kind(first_kind_dict)
        if second:
            final_dict['second'] = notif.check_second_type(second_kind_dict)
        if not bad_symbol:
            final = notif.final_check(final_dict)
            if final[-1] != 0:
                scan_result['buy'].append(create_dict(symbol_id)) if final[-1] == 1 else scan_result['sell'].append(
                    create_dict(symbol_id))
    return scan_result

def find_strategy_filters(user_name, strategy_name):
    trader = User.objects.get_by_natural_key(username=user_name)
    strategy = Strategy.objects.get(trader=trader, name=strategy_name).loads()
    return strategy['filters']


def find_symbol_ids():
    symbol_ids = MarketWatch.objects.filter(LastTradeDate=str(datetime.today() - timedelta(1))[:10]).values('SymbolId')
    return [symbol_id['SymbolId'] for symbol_id in symbol_ids]


def calculate_filter_result(strategy_filter):
    all_functions = dict(inspect.getmembers(dh, inspect.isfunction))
    function = all_functions['give_result_' + strategy_filter['kind'].lower()]
    return eval(function(strategy_filter))


def create_dict(symbol_id):
    return Stock.objects.get(symbol_id=symbol_id).as_json()
