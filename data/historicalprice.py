import requests as r, json
from data import redis, dates
from data.models import StockWatch

server_url = 'http://66.70.160.142:8000/data/mabna/'


# read historical price data:
def create_historical_table(num=0):
    stocks = StockWatch.objects.all()[num:]
    for index, stock in enumerate(stocks):
        add_new_history(stock, index + num)


def add_new_history(stock, index=0):
    data = get_historical_data_stock(stock, index)
    for key in data:
        redis.hset(stock.SymbolId, key, data[key])


def get_historical_data_stock(stock, index, step=100):
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
    SymbolId = stock.SymbolId
    name = stock.InstrumentName
    print('get historical data for {}-th stock with SymbolId:{} = {} '.format(index, SymbolId, name))
    mabna_id = find_mabna_id(SymbolId)
    if not mabna_id:
        print('error in mabna id')
        condition = False
    while condition:
        url = '/exchange/trades?instrument.id={}&_count={}&_skip={}&_sort=-date_time'.format(mabna_id,
                                                                                             step, i)
        print('trying to get data from {} and {} days ago'.format(i, i + step))
        try:
            output = r.get(server_url, params={'url': url}).text
        except Exception:
            print('problem at sending request either on server or mabna')
            condition = False
            continue
        try:
            history = json.loads(output)['data']
        except Exception:
            condition = False
            continue
        if len(history) > 0:
            condition = len(history) == step
            for day in history:
                if 'date_time' in day:
                    try:
                        prices = [day['close_price'], day['low_price'], day['high_price'], day['open_price']]
                        historical_data['date'].insert(0, dates.to_timestamp(date=day['date_time'], mode='mabna'))
                        historical_data['close'].insert(0, day['close_price'])
                        historical_data['low'].insert(0, min(prices))
                        historical_data['high'].insert(0, max(prices))
                        historical_data['open'].insert(0, day['open_price'])
                        historical_data['volume'].insert(0, day['volume'])
                    except Exception:
                        print('some problem happened during getting {} data at date: {}'.format(SymbolId,
                                                                                                day['date_time']))
            i += step
        else:
            condition = False
    return historical_data


def find_bad_historical_data():
    incorrect_keys = []
    for keys in redis.keys():
        close_price = redis.hget(keys, 'close')
        if len(close_price) < 30:
            incorrect_keys.append(keys)
    return incorrect_keys


database_history = ''


def read_historical_data_from_server_db(auto=False):
    database_history = ''
    if auto:
        database_history = r.get('https://xtrader.ir/data/history/', verify=False).text
    history = database_history
    history_data = json.loads(history)
    redis.flushall()
    for data in history_data:
        for symbol_id in data:
            for key in data[symbol_id]:
                redis.hset(symbol_id, key, data[symbol_id][key])


def find_mabna_id(SymbolId):
    url = '/exchange/instruments?code={}'.format(SymbolId)
    try:
        output = r.get(server_url, params={'url': url}).text
        data = json.loads(output)['data']
        if len(data) == 1:
            mabna_id = data[0]['id']
            return mabna_id
        else:
            return False
    except Exception:
        return False


'''
from data import historicalprice as h
h.create_historical_table()

'''
