# from task import update_history as up
from data.models import StockWatch as MarketWatch
from data import dates, update_history
from finance.models import Strategy
from django.contrib.auth.models import User
from . import data_handling as dh
import inspect
import pandas as pd
import numpy as np

all_functions = dict(inspect.getmembers(dh, inspect.isfunction))

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
                first_kind_dict['filter-first {}'.format(index)] = make_list_ready(result['result'])
                first = True
            if result['type'] == 'second':
                second_kind_dict['filter-second {}'.format(index)] = make_list_ready(result['result'])
                second = True
        if first:
            final_dict['first'] = check_first_kind(first_kind_dict)
        if second:
            final_dict['second'] = check_second_type(second_kind_dict)
        if not bad_symbol:
            final = final_check(final_dict)
            if final[-1] == 1:
                scan_result['buy'].append(create_dict(symbol_id))
                if not first:
                    scan_result['sell'].append(create_dict(symbol_id))
            if final[-1] == -1:
                scan_result['sell'].append(create_dict(symbol_id))
    return scan_result


def find_strategy_filters(user_name, strategy_name):
    trader = User.objects.get_by_natural_key(username=user_name)
    strategy = Strategy.objects.get(trader=trader, name=strategy_name).loads()
    return strategy['filters']


def find_symbol_ids():
    symbol_ids = MarketWatch.objects.filter(LastTradeDate=dates.Check().last_market()).values('SymbolId')
    return [symbol_id['SymbolId'] for symbol_id in symbol_ids]


def calculate_filter_result(strategy_filter):
    function = all_functions['give_result_' + strategy_filter['kind'].lower()]
    return eval(function(strategy_filter))


def create_dict(symbol_id):
    return Stock.objects.get(symbol_id=symbol_id).as_json()



# notification.py:
# from finance.notification import scan_market as s
def make_orders(update_market_watch=True):
    strategys = Strategy.objects.all()
    today_symbol_ids = update_history.get_updated_stocks_symbol_ids(num=0, update_market_watch=update_market_watch)
    orders = []
    for strategy_org in strategys:
        strategy = strategy_org.loads()
        strategy_orders = []
        for SymbolId in filter(lambda x: True if x in today_symbol_ids else False, strategy['watch_list']):
            first_kind_dict, second_kind_dict, final_dict = {}, {}, {}
            first, second = False, False
            for index, strategy_filter in enumerate(strategy['filters']):
                strategy_filter['symbol_id'] = SymbolId
                function = all_functions['give_result_' + strategy_filter['kind']]
                result = eval(function(strategy_filter))
                if result['type'] == 'first':
                    first_kind_dict['filter-first {}'.format(index)] = make_list_ready(result['result'])
                    first = True
                if result['type'] == 'second':
                    second_kind_dict['filter-second {}'.format(index)] = make_list_ready(result['result'])
                    second = True
            if first:
                final_dict['first'] = check_first_kind(first_kind_dict)
            if second:
                final_dict['second'] = check_second_type(second_kind_dict)
            final = final_check(final_dict)
            backtest = dh.give_result_backtest(name=SymbolId, res=final,
                                               config={'take profit': '0', 'stop loss': '0',
                                                       'initial deposit': '1000000'})
            backtest = eval(backtest)['result']
            history_len = len(final)
            last_trade = backtest['{}'.format(len(backtest))]
            for trade in ['buy', 'sell']:
                if last_trade[trade]['date'] == '{}'.format(history_len - 1):
                    if last_trade[trade]['action'] != 'Not Sold Yet':
                        strategy_orders.append(
                            {'symbol_id': SymbolId, 'trade': trade, 'action': last_trade[trade]['action']}
                        )
        if len(strategy_orders) > 0:
            orders.append({'strategy': strategy_org, 'orders': strategy_orders})
    return orders


def check_first_kind(results):
    magic_number = len(results)
    first = pd.DataFrame(results)
    result = first.sum(axis=1)
    check = result.apply(lambda x: 0 if (x < magic_number and x > -magic_number) else x)
    check = check.replace([magic_number, -magic_number], [1, -1])
    return np.asarray(check)


def check_second_type(results):
    second = pd.DataFrame(results)
    result = second.product(axis=1)
    return np.asarray(result)


def final_check(final_dict):
    df = pd.DataFrame(data=final_dict)
    return np.asarray(df.product(axis=1))


def make_list_ready(unready_list):
    return [x[0] for x in eval(unready_list)]
