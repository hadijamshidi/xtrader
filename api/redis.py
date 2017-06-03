import redis

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
    # num = 54
    stocks = Stock.objects.all()[num:]
    for stock in stocks:
        print('stock number: {}'.format(num))
        print('creating database for {} calling: {}'.format(stock.symbol_id, stock.mabna_short_name))
        data = get_historical_data_stock(stock)
        for key in data:
            r.hset(stock.symbol_id, key, data[key])
        print('{} database created'.format(stock.symbol_id))
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
        print('request to get {} to {}'.format(i, i + step))
        url = '/exchange/trades?instrument.id={}&_count={}&_skip={}&_sort=-date_time'.format(stock.mabna_id,
                                                                                             step, i)
        output = re.get('http://66.70.160.142:8000/mabna/api', params={'url': url}).text
        history = json.loads(output)['data']
        if len(history) > 0:
            condition = len(history) == step
            print('condition: {}'.format(condition))
            for day in history:
                if 'date_time' in day:
                    historical_data['date'].append(day['date_time'])
                    historical_data['close'].append(day['close_price'])
                    historical_data['low'].append(day['low_price'])
                    historical_data['high'].append(day['high_price'])
                    historical_data['open'].append(day['open_price'])
                    historical_data['volume'].append(day['volume'])
                else:
                    print('no date time')
            i += step
        else:
            condition = False
            print('this stock has no database')
    return historical_data
