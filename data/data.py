from threading import Thread

import requests as r, json

from api.models import Stock, MarketWatch

server_url = 'http://66.70.160.142:8000/mabna/api'


def call_threads_for_marketWatch():
    login_data = {
        'UserName': 'farabi_hadi',
        'Password': 'h159753159753H'
    }
    user = r.session()
    user.post('http://api.farabixo.com/api/account/repo/login', data=login_data)
    MarketWatch.objects.all().delete()
    stocks = Stock.objects.all()
    return get_market_watch_data(stocks=stocks, user=user)
    # for i in range(0, 600, step):
    #     discription = 'thread for {} until {}'.format(i, i + step)
    #     t = Thread(target=get_market_watch_data, name=discription,
    #                args=(stocks[i:i + step], user, i))
    #     t.start()


def get_market_watch_data(stocks, user):
    wrong_symbol_ids = []
    for index, stock in enumerate(stocks):
        symbol_id = stock.symbol_id
        print('trying to get data for symbol index: {} with mabna id: {}'.format(index, stock.mabna_id))
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
