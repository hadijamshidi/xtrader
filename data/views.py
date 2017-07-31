# from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from xtrader import localsetting as local
import requests


import json
from datetime import datetime
from django.http import HttpResponse
from data import redis




def mabnaAPI(request):
    if local.client['job'] == 'dev':
        result = dict()
        for k in request.GET:
            result[k] = request.GET[k]
        r = requests.get(local.client['url'] + '/maban/api', params=result)
    if local.client['job'] == 'server':
        r = requests.get(local.client['url'] + request.GET['url'], headers=local.client['auth'])
    return HttpResponse(r)


def stock(request):
    stocks = Stock.objects.all()
    stocks_list = []
    for stock in stocks:
        stocks_list.append({'id': stock.id, 'symbol_id': stock.symbol_id, 'mabna_id': stock.mabna_id,
                            'mabna_name': stock.mabna_name, 'mabna_english_name': stock.mabna_english_name,
                            'mabna_short_name': stock.mabna_short_name, 'mabna_kind': stock.mabna_kind})
        print(stocks_list)
    return HttpResponse(json.dumps(stocks_list))


def history(request):
    symbol_ids = redis.keys()
    histories = []
    for symbol_id in symbol_ids:
        symbol_id = symbol_id.decode()
        symbol_history_dict = {}
        symbol_history_dict[symbol_id] = {}
        for key in ['date', 'close', 'open', 'high', 'low', 'volume']:
            try:
                symbol_history_dict[symbol_id][key] = redis.hget(name=symbol_id, key=key)
            except Exception:
                pass
        histories.append(symbol_history_dict)
    return HttpResponse(json.dumps(histories))


def marketwatch(request):
    if True:
        from api.models import MarketWatch
        query = request.GET['query']
        results = MarketWatch.objects.filter(LastTradeDate=str(datetime.today())[:10]).raw(
            'select * from api_marketwatch where {}'.format(query))
        final_result = []
        for result in results:
            final_result.append(result.to_dict())
        return HttpResponse(json.dumps(final_result))
    else:
        return HttpResponse('database is updating please try a min later')


def stockwatch(request, SymbolId):
    from data.models import StockWatch
    from data import stockwatch
    stock_data = stockwatch.stockWatchInfo(SymbolId)
    stock = StockWatch.objects.get(SymbolId=SymbolId)
    for key in stock_data:
        stock.__setattr__(key, stock_data[key])
    stock.save()
    # sw = StockWatch.objects.get(SymbolId=SymbolId)
    return HttpResponse(json.dumps(stock.read()))
