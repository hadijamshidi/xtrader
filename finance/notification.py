from numpy.ma.core import _check_mask_axis

from .models import Strategy
from . import data_handling as dh
import inspect, pandas as pd, numpy as np

all_functions = dict(inspect.getmembers(dh, inspect.isfunction))


def scan_market():
    strategys = Strategy.objects.all()
    for strategy in strategys:
        strategy = strategy.loads()
        for SymbolId in strategy['watch_list']:
            first_kind_dict = {}
            first = False
            second_kind_dict = {}
            second = False
            final_dict = {}
            for index, strategy_filter in enumerate(strategy['filters']):
                strategy_filter['stock_name'] = SymbolId
                function = all_functions['give_result_' + strategy_filter['kind']]
                result = eval(function(strategy_filter))
                if result['type'] == 'first':
                    first_kind_dict['filter-first {}'.format(index)] = make_list_ready(result['result'])
                    first = True
                if result['type'] == 'second':
                    second_kind_dict['filter-second {}'.format(index)] = make_list_ready(result['result'])
                    second = True
            if first:
                print('it has first type')
                first = check_first_kind(first_kind_dict)
                final_dict['first'] = first
            if second:
                print('it has second type')
                second = check_second_type(second_kind_dict)
                final_dict['second'] = second
            final = final_check(final_dict)
            backtest = dh.give_result_backtest(name=SymbolId, res=final,
                                               config={'take profit': '0', 'stop loss': '0',
                                                       'initial deposit': '1000000'})
            backtest = eval(backtest)['result']
            last = len(backtest)
            # print(len())
            print(backtest['{}'.format(last)])
            print(backtest['{}'.format(last)]['sell'])


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
