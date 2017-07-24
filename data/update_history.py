from data.models import StockWatch as MarketWatch
from datetime import datetime, timedelta
from data import redis, manage_data as data
import requests as r
from data import dates
from xtrader.localsetting import farabi_login_data


# from task.update_history import update_history as h
# use farabixo


def update_history_with_farabixo(num=0, update_market_watch=True):
    updated_stocks = get_updated_stocks_symbol_ids(num, update_market_watch=update_market_watch)
    update_stocks_with_farabixo(updated_stocks, num) if not dates.Check().is_history_updated() else print('updated')
    return 'finish'


def get_updated_stocks_symbol_ids(num=0, update_market_watch=True):
    if update_market_watch:
        data.call_threads_for_marketWatch()
    symbols = MarketWatch.objects.filter(LastTradeDate=dates.Check().last_market()).values('SymbolId')
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
    user = r.session()
    user.post('http://api.farabixo.com/api/account/repo/login', data=farabi_login_data)
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
        updateHistory(symbol_id, today_data, index + num)


def updateHistory(symbol_id, today_data, index):
    for key in today_data:
        try:
            history = redis.hget(name=symbol_id, key=key)
            history.append(today_data[key])
            try:
                redis.hset(name=symbol_id, key=key, value=history)
            except Exception:
                print('problem at set data redis for symbolId: {} and index: {}'.format(symbol_id, index))
        except Exception:
            print('problem at loading from redis for symbolId: {} and index: {}'.format(symbol_id, index))
