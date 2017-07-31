from finance import data_handling
from django.http import HttpResponse, JsonResponse
import json
from . import strategy, scan, marketwatch
from data.dates import Check
# Create your views here.

import inspect
from django.shortcuts import render

all_functions = dict(inspect.getmembers(data_handling, inspect.isfunction))


def calculate_indicators(request):
    data = json.loads(request.POST['param'])
    kind = data['kind'].lower()
    function = all_functions['give_result_' + kind]
    result = function(data)
    return JsonResponse(result, safe=False)


def save_strategy(request):
    data = json.loads(request.POST['param'])
    result = strategy.add_strategy_to_db(data, request.user)
    return HttpResponse(result)


def get_strategy_names(request):
    names = strategy.load_strategy_names(request.user)
    return JsonResponse(json.dumps(names), safe=False)


def load_strategy(request):
    strategy_name = request.GET['name']
    filters = strategy.load_strategy_from_db(request.user, strategy_name)
    return JsonResponse(json.dumps(filters), safe=False)


def scan_market(request):
    strategy_name = request.GET['name']
    scan_result = scan.scan_market(request.user, strategy_name)
    return JsonResponse(json.dumps(scan_result), safe=False)


def update_indicators(request):
    if request.method == 'POST':
        data = json.loads(request.POST['param'])
        result = data_handling.give_update_indicators(data)
        return JsonResponse(result, safe=False)
    else:
        return JsonResponse('only post', safe=False)


def market_watch(request):
    return render(request, 'marketwatch.html')



def filtermarket(request):
    filters = json.loads(request.GET['filters'])
    query = ' and '.join(filters) if len(filters) != 0 else '1=1'
    from data.models import MarketWatch
    results = MarketWatch.objects.raw('select * from data_MarketWatch WHERE {}'.format(query))
    if len(filters) == 0:
        results = MarketWatch.objects.all()
    results = [r.read() for r in results]
    return HttpResponse(json.dumps(results))
