from api.models import Stock, MarketWatch
from show.models import Company
import requests as r
import json
from api import redis
from threading import Thread

server_url = 'http://66.70.160.142:8000/mabna/api'


def get_data_companies():
    url = '/exchange/instruments'
    step = 100
    wrong = []
    companies = Company.objects.all()
    for i, company in enumerate(companies):
        # print('request for getting Companies with english name {} for {}-th company with mabna id {}'.format(
        #     company.trade_symbol, i, company.id1))
        outputs = r.get(server_url,
                        params={'url': url + '?short_name={}&type=share'.format(company.trade_symbol)}).text
        try:
            symbols = json.loads(outputs)['data']
            # print('{} symbols found for {}'.format(len(symbols), company.trade_symbol))
            for symbol in symbols:
                if symbol['short_name'] == company.trade_symbol:
                    create_company_table_new(symbol)
                    # print('{} symbol and isin found'.format(company.trade_symbol))
                    # else:
                    #     print('{} bullshit symbol for symbol: {}'.format(symbol['short_name'], company.trade_symbol))
        except Exception:
            # print('failed to handle {}'.format(company.trade_symbol))
            wrong.append(company.trade_symbol)


# create_company_table(symbols, i)

# for i in range(0, 800, step):
#     print('request for getting Companies from {} until {}'.format(i, i + step))
#     output = r.get(server_url, params={'url': url + '?type=share&_count=100&_skip={}'.format(i)}).text
#     companies = json.loads(output)['data']
#     create_company_table(companies, i)
def create_company_table_new(company):
    if company['type'] == 'share':
        company_data = dict(
            symbol_id=company['code'],
            isin=company['isin'],
            mabna_id=company['id'],
            mabna_name=company['name'],
            mabna_english_name=company['english_name'],
            mabna_short_name=company['short_name'],
            mabna_kind=company['type'],
        )
        new_company = Stock(**company_data)
        new_company.save()
        # print('{} added'.format(company['short_name']))


def create_company_table(companies, i):
    # print(len(companies))
    wrong_ids = []
    for index, company in enumerate(companies):
        # print('trying to add company number: {} type:{}'.format(i + index, company['type']))
        if company['type'] == 'share':
            company_data = dict(
                symbol_id=company['code'],
                isin=company['isin'],
                mabna_id=company['id'],
                mabna_name=company['name'],
                mabna_english_name=company['english_name'],
                mabna_short_name=company['short_name'],
                mabna_kind=company['type'],
            )
            new_company = Stock(**company_data)
            # print('added')
            new_company.save()
        else:
            wrong_ids.append(company['code'])
            # print('{} is not share'.format(company['code']))
    return wrong_ids


def call_threads_for_marketWatch():
    login_data = {
        'UserName': 'farabi_hadi',
        'Password': 'h159753159753H'
    }
    user = r.session()
    user.post('http://api.farabixo.com/api/account/repo/login', data=login_data)
    MarketWatch.objects.all().delete()
    stocks = Stock.objects.all()
    # wrong = get_market_watch_data(stocks, user, 0)
    step = 150
    for i in range(0, 600, step):
        discription = 'thread for {} until {}'.format(i, i + step)
        t = Thread(target=get_market_watch_data, name=discription,
                   args=(stocks[i:i + step], user, i))
        # t.setDaemon(True)
        t.start()

    # # t.join()
    return 'finish'


def get_market_watch_data(stocks, user, i):
    wrong_symbol_ids = []
    for index, stock in enumerate(stocks):
        symbol_id = stock.symbol_id
        # print('trying to get data for symbol index: {} with mabna id: {}'.format(i + index, stock.mabna_id))
        output = user.get('http://api.farabixo.com/api/pub/GetSymbol', params={'SymbolId': symbol_id}).text
        try:
            trades_data = json.loads(output)
        except Exception:
            wrong_symbol_ids.append(dict(id=symbol_id, problem='failed to json loads'))
            continue
        # print(trades_data)
        if symbol_id == trades_data['SymbolId']:
            trades_dict = {}
            for key in trades_data:
                if key not in ['BidAsk', 'LastTradeDate']:
                    trades_dict[key] = trades_data[key]
            try:
                trades_dict['LastTradeDate'] = trades_data['LastTradeDate'][:10]
            except Exception:
                wrong_symbol_ids.append(dict(id=symbol_id, problem='no LastTradeDate'))
            for BidAsk in trades_data['BidAsk']:
                row = BidAsk['RowPlace']
                trades_dict['pd' + str(row)] = BidAsk['AskPrice']
                trades_dict['zd' + str(row)] = BidAsk['AskNumber']
                trades_dict['qd' + str(row)] = BidAsk['AskQuantity']
                trades_dict['po' + str(row)] = BidAsk['BidPrice']
                trades_dict['zo' + str(row)] = BidAsk['BidNumber']
                trades_dict['qo' + str(row)] = BidAsk['BidQuantity']
        else:
            # print('different ids at {}'.format(symbol_id))
            wrong_symbol_ids.append(dict(id=symbol_id, problem='different ids'))
            # wrong_symbol_ids.append(dict(id=symbol_id, problem='failed to json.loads'))
        try:
            MarketWatch(**trades_dict).save()
        except Exception:
            wrong_symbol_ids.append(dict(id=symbol_id, problem='failed to save'))
    return wrong_symbol_ids


def read_stock():
    stocks_text = r.get('http://66.70.160.142/api/stock/').text
    stocks_data = json.loads(stocks_text)
    for stock in stocks_data:
        stock_dict = {}
        for key in stock:
            stock_dict[key] = stock[key]
        Stock(**stock_dict).save()


def read_history():
    history = r.get('http://66.70.160.142/api/history/').text
    history_data = json.loads(history)
    # print(history)
    for data in history_data:
        for symbol_id in data:
            for key in data[symbol_id]:
                # print(symbol_id,key)
                redis.hset(symbol_id, key, data[symbol_id][key])


def jalali_to_timestamp(jalali_date):
    from . import jalali
    jdate = "{}/{}/{}".format(jalali_date[:4], jalali_date[4:6], jalali_date[6:8])
    gorgeain_date = jalali.Persian(jdate).gregorian_string("{}/{}/{}")
    import time
    import datetime
    timestamp = time.mktime(datetime.datetime.strptime(gorgeain_date, "%Y/%m/%d").timetuple())
    date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print('conveted from {} to timestamp: {} which is equal to {}'.format(jalali_date, timestamp, date))
    return timestamp
