"""
	module tasks:
		read from APIs, add to data base, updateing, and api for reading from data base
"""
from xtrader.localsetting import farabi_login_data
# from data.models import StockWatch
import requests as r
from data import backup
import json
# groups = backup.symbol_dict
# server_url = 'http://66.70.160.142:8000/mabna/api'
symbol_ids = backup.all_ids
wrong_symbol_ids = []
new_group = {}


def createStockWatchTables(num=0):
    for i, symbol_id in enumerate(symbol_ids):
        if i >= num:
            print('stock watch for index: {}'.format(i))
            info = stockWatchInfo(symbol_id)
            if info:
                addStockWatchTable(info)


def stockWatchInfo(symbol_id):
    user = r.session()
    user.post('http://api.farabixo.com/api/account/repo/login', data=farabi_login_data)
    print('trying to get data for symbol with id: {}'.format(symbol_id))
    output = user.get('http://api.farabixo.com/api/pub/GetSymbol', params={'SymbolId': symbol_id}).text
    try:
        trades_data = json.loads(output)
    except Exception:
        wrong_symbol_ids.append(dict(id=symbol_id, problem='failed to json loads', data=output))
        return False
    if trades_data['InstrumentTitle'][:4]!= 'ح . ':
        trades_dict = {}
        for key in trades_data:
            if key not in ['BidAsk', 'LastTradeDate']:
                trades_dict[key] = trades_data[key]
        try:
            trades_dict['LastTradeDate'] = trades_data['LastTradeDate'][:10]
        except Exception:
            wrong_symbol_ids.append(dict(id=symbol_id, problem='no LastTradeDate'))
            return False

        for BidAsk in trades_data['BidAsk']:
            row = BidAsk['RowPlace']
            trades_dict['pd' + str(row)] = BidAsk['AskPrice']
            trades_dict['zd' + str(row)] = BidAsk['AskNumber']
            trades_dict['qd' + str(row)] = BidAsk['AskQuantity']
            trades_dict['po' + str(row)] = BidAsk['BidPrice']
            trades_dict['zo' + str(row)] = BidAsk['BidNumber']
            trades_dict['qo' + str(row)] = BidAsk['BidQuantity']
    else:
        wrong_symbol_ids.append(dict(id=symbol_id, problem='ح . '))
        return False
    return trades_dict


def addStockWatchTable(table):
    print('successful progress')
    # StockWatch(**info).save()


def check_wrong_symbols():
    for symbol in backup.wrong_symbol_ids:
        findSymbolID(symbol['symbol'])


def read_portfo():
    user = r.session()
    user.post('http://api.farabixo.com/api/account/repo/login', data=farabi_login_data)
    # print('trying to get data for symbol: {} with id: {}'.format(symbol, symbol_id))
    # output = user.get('http://api.farabixo.com/api/pub/GetWatchList').text
    # data = eval(output)
    # print(data)
    Id = 93633
    output = user.get('http://api.farabixo.com/api/pub/GetWatchListSymbol', params={'watchListId': Id}).text
    # print(output)
    import json
    data = json.loads(output)
    print(data)
    symbols = {}
    for i, symbol in enumerate(data):
        symbol_name = symbol['InstrumentName']
        if symbol_name not in symbols:
            print(i, symbol_name)
            symbols[symbol_name] = symbol['SymbolId']
        else:
            print('namad tekrari: {}'.format(symbol_name))
    print(symbols)
