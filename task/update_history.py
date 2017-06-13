from api.models import MarketWatch
from datetime import datetime
from data import redis, data
import requests as r
from task import dates


# from task.update_history import update_history as h
# use farabixo


def update_history_with_farabixo():
    updated_stocks = get_updated_stocks_symbol_ids()
    update_stocks_with_farabixo(updated_stocks)
    return 'finish'


def get_updated_stocks_symbol_ids():
    data.call_threads_for_marketWatch()
    symbols = MarketWatch.objects.filter(LastTradeDate=str(datetime.today())[:10]).values('SymbolId')
    symbol_ids = [symbol['SymbolId'] for symbol in symbols]
    return symbol_ids


def login_farabi():
    login_data = {
        'UserName': 'farabi_hadi',
        'Password': 'h159753159753H'
    }
    user = r.session()
    user.post('http://api.farabixo.com/api/account/repo/login', data=login_data)
    return user


def update_stocks_with_farabixo(symbol_ids):
    user = login_farabi()
    for symbol_id in symbol_ids:
        output = user.get('http://api.farabixo.com/api/pub/GetSymbol', params={'SymbolId': symbol_id}).text
        output = eval(output)
        historical_data_keys = dict(
            date='LastTradeDate',
            close='ClosingPrice',
            low='LowestTradePrice',
            high='HighestTradePrice',
            open='FirstTradePrice',
            volume='TotalNumberOfSharesTraded',
        )
        today_data = dict()
        for key in historical_data_keys:
            today_data[key] = output[historical_data_keys[key]]
        today_data['date'] = dates.to_timestamp(date=today_data['date'], mode='farabi')
        update_history(symbol_id, today_data)


def update_history(symbol_id, today_data):
    for key in today_data:
        history = eval(redis.hget(name=symbol_id, key=key))
        history.append(today_data[key])
        redis.hset(name=symbol_id, key=key, value=history)

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
