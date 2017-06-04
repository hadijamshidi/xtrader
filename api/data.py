from api.models import Stock, MarketWatch
from show.models import Company
import requests as r
import json
from threading import Thread

server_url = 'http://66.70.160.142:8000/mabna/api'


def get_data_companies():
    url = '/exchange/instruments'
    step = 100
    wrong = []
    companies = Company.objects.all()
    for i, company in enumerate(companies):
        print('request for getting Companies with english name {} for {}-th company with mabna id {}'.format(
            company.trade_symbol, i, company.id1))
        outputs = r.get(server_url,
                        params={'url': url + '?short_name={}&type=share'.format(company.trade_symbol)}).text
        try:
            symbols = json.loads(outputs)['data']
            print('{} symbols found for {}'.format(len(symbols), company.trade_symbol))
            for symbol in symbols:
                if symbol['short_name'] == company.trade_symbol:
                    create_company_table_new(symbol)
                    print('{} symbol and isin found'.format(company.trade_symbol))
                else:
                    print('{} bullshit symbol for symbol: {}'.format(symbol['short_name'], company.trade_symbol))
        except Exception:
            print('failed to handle {}'.format(company.trade_symbol))
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
        print('{} added'.format(company['short_name']))


def create_company_table(companies, i):
    print(len(companies))
    wrong_ids = []
    for index, company in enumerate(companies):
        print('trying to add company number: {} type:{}'.format(i + index, company['type']))
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
            print('added')
            new_company.save()
        else:
            wrong_ids.append(company['code'])
            print('{} is not share'.format(company['code']))
    return wrong_ids


def call_threads_for_marketWatch():
    login_data = {
        'UserName': 'farabi_hadi',
        'Password': 'h159753159753H'
    }
    user = r.session()
    user.post('http://api.farabixo.com/api/account/repo/login', data=login_data)
    stocks = Stock.objects.all()
    wrong = get_market_watch_data(stocks, user, 0)
    # for i in range(0, 600, step):
    #     discription = 'thread for {} until {}'.format(i, i + step)
    #     t = Thread(target=get_market_watch_data, name=discription,
    #                args=(stocks[i:i + step], user, i))
    #     t.start()
    #     # t.join()
    # print('finish')
    return wrong


def get_market_watch_data(stocks, user, i):
    wrong_symbol_ids = []
    for index, stock in enumerate(stocks):
        symbol_id = stock.symbol_id
        print('trying to get data for symbol index: {} with mabna id: {}'.format(i + index, stock.mabna_id))
        output = user.get('http://api.farabixo.com/api/pub/GetSymbol', params={'SymbolId': symbol_id}).text
        try:
            trades_data = json.loads(output)
            # print(trades_data)
            if symbol_id == trades_data['SymbolId']:
                trades_dict = {}
                all_name = MarketWatch.__dict__.keys()
                for i in all_name:
                    if i not in ['__doc__', 'MultipleObjectsReturned', '_meta', '__module__', 'id', '__str__',
                                 'DoesNotExist']:

                        # wrong_symbol_ids.append('difrrent ids at {}'.format(symbol_id))
                        trades_dict[i] = trades_data[i]
                        for i in range(1, 4):
                            j = trades_data['BidAsk'][i]['RowPlace']
                            trades_dict['pd' + str(j)] = trades_data['BidAsk'][i]['AskPrice']
                            trades_dict['zd' + str(j)] = trades_data['BidAsk'][i]['AskNumber']
                            trades_dict['qd' + str(j)] = trades_data['BidAsk'][i]['AskQuantity']
                            trades_dict['po' + str(j)] = trades_data['BidAsk'][i]['BidPrice']
                            trades_dict['zo' + str(j)] = trades_data['BidAsk'][i]['BidNumber']
                            trades_dict['qo' + str(j)] = trades_data['BidAsk'][i]['BidQuantity']

                # trades_dict = dict(
                #             symbol_id=trades_data['SymbolId'],
                #             closing_price=trades_data['ClosingPrice'],
                #             first_trade_price=trades_data['FirstTradePrice'],
                #             last_trade_price=trades_data['LastTradePrice'],
                #             lowest_trade_price=trades_data['LowestTradePrice'],
                #             highest_trade_price=trades_data['HighestTradePrice']
                #             # isin
                #         )
                new_marketWatch = MarketWatch(**trades_dict)
            else:
                print('different ids at {}'.format(symbol_id))
                wrong_symbol_ids.append(dict(id=symbol_id, problem='different ids'))
        except Exception:
            print('failed to json.loads output at symbol id: {}'.format(symbol_id))
            # print('symbol id: {} has some problem please check later!'.format(symbol_id))
            wrong_symbol_ids.append(dict(id=symbol_id, problem='failed to json.loads'))

    return wrong_symbol_ids


def readstock():


    x=r.get('http://66.70.160.142/api/stock/').text
    print(x)
    return x

