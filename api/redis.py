import redis
from api import data

r = redis.StrictRedis(host='localhost', port=6379, db=0)


def set(name, value):
    return r.set(name=name, value=value)


def get(name):
    return r.get(name=name).decode()


def hset(name, key, value):
    return r.hset(name=name, key=key, value=value)


def hget(name, key):
    return r.hget(name=name, key=key).decode()


def delete(names):
    return r.delete(*names)


def keys():
    return r.keys()


def load_history(name):
    needs = ['date', 'open', 'high', 'low', 'close', 'volume']
    data_dict = dict()
    for need in needs:
        data_dict[need] = eval(r.hget(name=name, key=need))[::-1]
    date = [data.jalali_to_timestamp(day) for day in data_dict['date']]
    data_dict['date'] = date
    return data_dict


def flushall():
    return r.flushall()


# read historical data:

import requests as re, threading
from api.models import Stock
import json


# def call_threads_for_history():
#     num = 54
#     stocks = Stock.objects.all()
#     t1 = threading.Thread(target=create_historical_table, args=(stocks[num:200],))
#     t1.start()
#     t2 = threading.Thread(target=create_historical_table, args=(stocks[200:400],))
#     t2.start()
#     t3 = threading.Thread(target=create_historical_table, args=(stocks[400:600],))
#     t3.start()


def create_historical_table(num):
    stocks = Stock.objects.all()[num:]
    for stock in stocks:
        data = get_historical_data_stock(stock)
        for key in data:
            r.hset(stock.symbol_id, key, data[key])
        num += 1


def get_historical_data_stock(stock):
    step = 100
    historical_data = dict(
        date=[],
        close=[],
        low=[],
        high=[],
        open=[],
        volume=[],
    )
    condition = True
    i = 0
    while condition:
        url = '/exchange/trades?instrument.id={}&_count={}&_skip={}&_sort=-date_time'.format(stock.mabna_id,
                                                                                             step, i)
        output = re.get('http://66.70.160.142:8000/mabna/api', params={'url': url}).text
        history = json.loads(output)['data']
        if len(history) > 0:
            condition = len(history) == step
            for day in history:
                if 'date_time' in day:
                    historical_data['date'].insert(0, day['date_time'])
                    historical_data['close'].insert(0, day['close_price'])
                    historical_data['low'].insert(0, day['low_price'])
                    historical_data['high'].insert(0, day['high_price'])
                    historical_data['open'].insert(0, day['open_price'])
                    historical_data['volume'].insert(0, day['volume'])
            i += step
        else:
            condition = False
    return historical_data


def clean_historical_data_stock():
    from api import redis as r
    import json
    incorrect_keys = []
    for keys in r.keys():
        close_price = r.hget(keys, 'close')
        close_price = json.loads(close_price)
        if len(close_price) < 30:
            incorrect_keys.append(keys)
    return incorrect_keys
