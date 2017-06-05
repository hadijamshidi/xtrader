from django.db.models.functions import datetime

from api.models import Stock,MarketWatch
from django.http import HttpResponse
from api import redis
import json


# Create your views here.
def stock(request):
    stocks = Stock.objects.all()
    stocks_list = []
    for stock in stocks:
        stocks_list.append({'id':stock.id,'symbol_id':stock.symbol_id,'mabna_id':stock.mabna_id,
                            'mabna_name':stock.mabna_name,'mabna_english_name': stock.mabna_english_name,
                            'mabna_short_name':stock.mabna_short_name,'mabna_kind':stock.mabna_kind})
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
            symbol_history_dict[symbol_id][key] = redis.hget(name=symbol_id, key=key)
        histories.append(symbol_history_dict)
    return HttpResponse(json.dumps(histories))
def update_history(request):
    c=MarketWatch.objects.all()
    for m in c:

        if str(m.LastTradeDate) == str(datetime.datetime.today())[:10]:
            #TO DO
            pass
