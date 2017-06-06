from api.models import Stock, Status
from django.http import HttpResponse
from api import redis
import json
from datetime import datetime


# Create your views here.
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
            symbol_history_dict[symbol_id][key] = redis.hget(name=symbol_id, key=key)
        histories.append(symbol_history_dict)
    return HttpResponse(json.dumps(histories))


def marketwatch(request):
    if Status.objects.get(job='server').market_watch == 'ready':
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


def update_MarketWatch(request):
    from api import testdate
    if Status.objects.get(job='server').number_of_requests == 0:
        testdate.update_MarketWatch()
    else:
        return HttpResponse('workers are working')
        # returnadmin.site.register(MarketWatch)
