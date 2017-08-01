# from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from xtrader import localsetting as local
import requests
import json
from datetime import datetime
from django.http import HttpResponse
from data import redis
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .models import StockWatch as Symbol
from django.http import JsonResponse


def mabnaAPI(request):
    if local.client['job'] == 'dev':
        result = dict()
        for k in request.GET:
            result[k] = request.GET[k]
        r = requests.get(local.client['url'] + '/maban/api', params=result)
    if local.client['job'] == 'server':
        r = requests.get(local.client['url'] + request.GET['url'], headers=local.client['auth'])
    return HttpResponse(r)


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


def stockwatch(request, SymbolId):
    stock = Symbol.objects.get(SymbolId=SymbolId)
    return HttpResponse(json.dumps(stock.read()))


def symbol_search(request, query):
    symbols = Symbol.objects.filter(InstrumentName__istartswith=query)
    # | Symbol.objects.filter(mabna_english_name__icontains=query) \
    # | Symbol.objects.filter(name__icontain=query)
    symbol_max_results = 8
    if symbols.count() < symbol_max_results:
        symbols = symbols | Symbol.objects.filter(InstrumentName__icontains=query)
    results = [ob.as_json() for ob in symbols]
    mydict = dict(
        items=results,
    )
    return HttpResponse(json.dumps(mydict, ensure_ascii=False).encode("utf8"),
                        content_type="application/json; charset=utf-8")


def get_data(request, SymbolId):
    from data import redis
    import pandas as pd
    data_dict = redis.load_history(SymbolId)
    df = pd.DataFrame(data=data_dict, index=data_dict['date'])
    df = df.loc[:, ['date', 'open', 'high', 'low', 'close', 'volume']]
    stock = Symbol.objects.get(SymbolId=SymbolId)
    stock_information = dict(
        # per_name=stock.mabna_short_name,
        # measurement_name=name,
        # name=stock.mabna_name,
        per_name=stock.InstrumentName,
        measurement_name=stock.SymbolId,
        name=stock.InstrumentName,
    )
    stock_history = df.to_json(orient='values')
    stock_information['items'] = stock_history
    return JsonResponse(json.dumps(stock_information), safe=False)
