"""
	module tasks:
		read from APIs, add to data base, updateing, and api for reading from data base
"""
from xtrader.localsetting import farabi_login_data
from data.models import StockWatch
from data.crawl import epss
import requests as r
from data import backup
import json

symbol_ids = backup.all_ids
wrong_symbol_ids = []
new_group = {}


def createStockWatchTables(num=0):
    for i, symbol_id in enumerate(symbol_ids):
        if i >= num:
            print('stock watch for index: {}'.format(i))
            info = stockWatchInfo(symbol_id)
            # if info:
                # try:
            addStockWatchTable(info)
                # except Exception:
                #     wrong_symbol_ids.append(dict(id=symbol_id, problem='on save'))


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
    if trades_data['InstrumentTitle'][:4] != 'ح . ':
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
    try:
        Eps = epss(trades_dict['InstrumentName'])
        trades_dict['Eps'] = Eps
        if Eps != 0: trades_dict['PricePerEarning'] = trades_dict['ClosingPrice']/Eps
    except Exception:
        wrong_symbol_ids.append(dict(id=symbol_id, problem='no Eps'))
    return trades_dict


def addStockWatchTable(info):
    StockWatch(**info).save()
    print('successful progress')


def read_portfo():
    user = r.session()
    user.post('http://api.farabixo.com/api/account/repo/login', data=farabi_login_data)
    Id = 93633
    output = user.get('http://api.farabixo.com/api/pub/GetWatchListSymbol', params={'watchListId': Id}).text
    data = json.loads(output)
    symbols = {}
    for i, symbol in enumerate(data):
        symbol_name = symbol['InstrumentName']
        if symbol_name not in symbols:
            symbols[symbol_name] = symbol['SymbolId']
        else:
            print('namad tekrari: {}'.format(symbol_name))


def cleanduplicate():
    for row in StockWatch.objects.all():
        if StockWatch.objects.filter(SymbolId=row.SymbolId).count() > 1:
            row.delete()


def update_eps():
    stocks = StockWatch.objects.all()
    from data.crawl import epss
    for stock in stocks:
        InstrumentName = stock.InstrumentName
        try:
            stock.Eps = epss(InstrumentName)
            stock.save()
            print(InstrumentName, epss(InstrumentName))
        except Exception:
            print('failed {}'.format(InstrumentName))
