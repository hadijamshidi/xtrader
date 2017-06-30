import requests as r, json
from show.models import Company
from api.models import Stock
from data import redis
from task import dates

server_url = 'http://66.70.160.142:8000/mabna/api'


# Company
def get_companies_data(step=100):
    url = '/stock/companies'
    wrongs = []
    for i in range(0, 1400, step):
        print('request for getting Companies from {} until {}'.format(i, i + step))
        output = r.get(server_url, params={'url': url + '?_count=100&_skip={}'.format(i)}).text
        companies = json.loads(output)['data']
        w = add_companies_to_db(companies)
        wrongs.append(w)


def add_companies_to_db(companies):
    wrong_ids = []
    for index, company in enumerate(companies):
        data = company
        try:
            company_dict = dict(
                id1=data['id'] if 'id' in data else 0,
                name=data['name'] if 'name' in data else 'False',
                english_name=data['english_name'] if 'english_name' in data else 'False',
                short_name=data['short_name'] if 'short_name' in data else 'False',
                english_short_name=data['english_short_name'] if 'english_short_name' in data else 'False',
                trade_symbol=data['trade_symbol'] if 'trade_symbol' in data else 'False',
                english_trade_symbol=data['english_trade_symbol'] if 'english_trade_symbol' in data else 'False',
                state=data['state']['id'] if 'state' in data else 'False',
                exchange=data['exchange']['id'] if 'exchange' in data else 'False',
                categories=data['categories'][0]['id'] if 'categories' in data else 'False',
                metaversion=data['meta']['version'] if ('meta' in data and 'version' in data['meta'])else 'False',
            )
            Company(**company_dict).save()
        except Exception:
            wrong_ids.append(company['id'])
    return wrong_ids


def clean_duplicate_company():
    companys = Company.objects.all()
    for company in companys:
        check_company = Company.objects.filter(id1=company.id1)
        if len(check_company) > 1:
            original_company = check_company.first()
            check_company.delete()
            original_company.save()


def clean_company():
    clean_duplicate_company()
    companies = Company.objects.filter(exchange='False')
    for company in companies:
        stock = Stock.objects.filter(mabna_short_name=company.trade_symbol)
        stock.delete()
        company.delete()


# read historical price data:

def create_historical_table(num=0):
    stocks = Stock.objects.all()[num:]
    for index, stock in enumerate(stocks):
        data = get_historical_data_stock(stock, index + num)
        for key in data:
            redis.hset(stock.symbol_id, key, data[key])


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
    mabna_id = stock.mabna_id
    print('trying to get historical data for {} index of {} in stocks'.format(mabna_id, index))
    while condition:
        url = '/exchange/trades?instrument.id={}&_count={}&_skip={}&_sort=-date_time'.format(stock.mabna_id,
                                                                                             step, i)
        print('trying to get data from {} and {} days ago'.format(i, i + step))
        try:
            output = r.get('http://66.70.160.142/mabna/api', params={'url': url}).text
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
                        print('some problem happened during getting {} data at date: {}'.format(mabna_id,
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


def read_historical_data_from_server_db():
    history = r.get('http://66.70.160.142/api/history/').text
    history_data = json.loads(history)
    redis.flushall()
    for data in history_data:
        for symbol_id in data:
            for key in data[symbol_id]:
                redis.hset(symbol_id, key, data[symbol_id][key])


# Stock model
def get_stocks_data(step=100):
    url = '/exchange/instruments'
    wrong = []
    companies = Company.objects.all()
    for i, company in enumerate(companies):
        # print('request for getting Companies with english name {} for {}-th company with mabna id {}'.format(
        #     company.trade_symbol, i, company.id1))
        outputs = r.get(server_url,
                        params={'url': url + '?short_name={}&type=share'.format(company.trade_symbol)}).text
        try:
            stocks = json.loads(outputs)['data']
            # print('{} symbols found for {}'.format(len(symbols), company.trade_symbol))
            for stock in stocks:
                if stock['short_name'] == company.trade_symbol:
                    add_stock_to_db(stock)
                    # print('{} symbol and isin found'.format(company.trade_symbol))
                    # else:
                    #     print('{} bullshit symbol for symbol: {}'.format(symbol['short_name'], company.trade_symbol))
        except Exception:
            # print('failed to handle {}'.format(company.trade_symbol))
            wrong.append(company.trade_symbol)


def add_stock_to_db(stock):
    if stock['type'] == 'share':
        stock_data = dict(
            symbol_id=stock['code'],
            isin=stock['isin'],
            mabna_id=stock['id'],
            mabna_name=stock['name'],
            mabna_english_name=stock['english_name'],
            mabna_short_name=stock['short_name'],
            mabna_kind=stock['type'],
        )
        Stock(**stock_data).save()
        # print('{} added'.format(company['short_name']))


def read_stock_from_server_db():
    stocks_text = r.get('http://66.70.160.142/api/stock/').text
    stocks_data = json.loads(stocks_text)
    for stock in stocks_data:
        stock_dict = {}
        for key in stock:
            stock_dict[key] = stock[key]
        Stock(**stock_dict).save()
