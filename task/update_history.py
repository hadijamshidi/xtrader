from api.models import MarketWatch
from datetime import datetime,timedelta
from data import redis, data
import requests as r
from task import dates


# from task.update_history import update_history as h
# use farabixo


def update_history_with_farabixo(num=0):
    updated_stocks = get_updated_stocks_symbol_ids(num)
    update_stocks_with_farabixo(updated_stocks, num)
    return 'finish'


def get_updated_stocks_symbol_ids(num=0, update_market_watch=True):
    if update_market_watch:
        data.call_threads_for_marketWatch()
    symbols = MarketWatch.objects.filter(LastTradeDate=str(datetime.today())[:10]).values('SymbolId')
    # TODO: check time better
    # if not symbols.exists():
    #     symbols = MarketWatch.objects.filter(LastTradeDate=str(datetime.today()-timedelta(1))[:10]).values('SymbolId')
    keys = redis.keys()
    keys = [key.decode() for key in keys]
    symbol_ids = []
    for symbol in symbols[num:]:
        if symbol['SymbolId'] in keys:
            symbol_ids.append(symbol['SymbolId'])
        else:
            print('{} is a dangerous symbol check it quickly'.format(symbol['SymbolId']))
    return symbol_ids


def login_farabi():
    login_data = {
        'UserName': 'farabi_hadi',
        'Password': 'h159753159753H'
    }
    user = r.session()
    user.post('http://api.farabixo.com/api/account/repo/login', data=login_data)
    return user


def update_stocks_with_farabixo(symbol_ids, num):
    user = login_farabi()
    for index, symbol_id in enumerate(symbol_ids):
        try:
            output = user.get('http://api.farabixo.com/api/pub/GetSymbol', params={'SymbolId': symbol_id}).text
            output = eval(output)
        except Exception:
            print('problem at sending request of SymbolId: {} and num {}'.format(symbol_id, index + num))
            continue

        historical_data_keys = dict(
            date='LastTradeDate',
            close='ClosingPrice',
            low='LowestTradePrice',
            high='HighestTradePrice',
            open='FirstTradePrice',
            volume='TotalNumberOfSharesTraded',
        )
        today_data = dict()
        try:
            for key in historical_data_keys:
                today_data[key] = output[historical_data_keys[key]]
        except Exception:
            print('problem at creating today_data dict of SymbolId: {} and num {}'.format(symbol_id, index + num))
            continue
        today_data['date'] = dates.to_timestamp(date=today_data['date'], mode='farabi')
        update_history(symbol_id, today_data, index + num)


def update_history(symbol_id, today_data, index):
    for key in today_data:
        try:
            history = eval(redis.hget(name=symbol_id, key=key))
            history.append(today_data[key])
            try:
                redis.hset(name=symbol_id, key=key, value=history)
            except Exception:
                print('problem at set data redis for symbolId: {} and index: {}'.format(symbol_id, index))
        except Exception:
            print('problem at loading from redis for symbolId: {} and index: {}'.format(symbol_id, index))

# def update_history_with_mabna():
#     updated_stocks = get_updated_stocks()
#     update_stocks(updated_stocks)
#     return 'finish'
#
#
# def get_updated_stocks():
#     data.call_threads_for_marketWatch()
#     symbols = MarketWatch.objects.filter(LastTradeDate=str(datetime.today())[:10]).values('SymbolId')
#     symbols_dict = []
#     for symbol in symbols:
#         SymbolId = symbol['SymbolId']
#         mabna_id = Stock.objects.filter(symbol_id=SymbolId).first().mabna_id
#         symbol_dict = {'mabna_id': mabna_id, 'SymbolId': SymbolId}
#         symbols_dict.append(symbol_dict)
#     return symbols_dict
#
#
# def update_stocks(symbols_dict, step=50):
#     historical_data_keys = dict(
#         date='date_time',
#         close='close_price',
#         low='low_price',
#         high='high_price',
#         open='open_price',
#         volume='volume',
#     )
#     for symbol_dict in symbols_dict:
#         data = get_updated_data(symbol_dict['mabna_id'])
#         for key in historical_data_keys:
#             SymbolId = symbol_dict['SymbolId']
#             last = eval(redis.hget(SymbolId, key))
#             last.append(data[historical_data_keys[key]])
#             redis.hset(SymbolId, key, last)
#
#
# def get_updated_data(mabna_id):
#     url = '/exchange/trades?instrument.id={}&_sort=-date_time&_count=1'.format(mabna_id)
#     output = r.get('http://66.70.160.142/mabna/api', params={'url': url}).text
#     data = json.loads(output)['data'][0]
#     return data
