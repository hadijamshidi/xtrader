from finance import data_handling
from django.http import HttpResponse, JsonResponse
import json
from . import strategy, scan, marketwatch
from finance import data_handling as dh, indicator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseNotFound
from accounts.forms import AuthenticationForm


from data.dates import Check
# Create your views here.

import inspect
from django.shortcuts import render
from django.shortcuts import render, redirect
all_functions = dict(inspect.getmembers(data_handling, inspect.isfunction))


def calculate_indicators(request):
    data = json.loads(request.GET['param'])
    kind = data['kind'].lower()
    function = all_functions['give_result_' + kind]
    result = function(data)
    return JsonResponse(result, safe=False)


def save_strategy(request):
    data = json.loads(request.GET['param'])
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
    if request.method == 'GET':
        data = json.loads(request.GET['param'])
        result = data_handling.give_update_indicators(data)
        return JsonResponse(result, safe=False)
    else:
        return JsonResponse('only GET', safe=False)


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



def indicators_api(request):
    if request.method == 'GET':
        return JsonResponse(json.dumps(indicator.get_group_api()), safe=False)
    else:
        return JsonResponse(json.dumps({'api': 'null'}), safe=False)
def back_test(request):
    if request.method == 'GET':
        data = json.loads(request.GET['param'])
        name = data['name']
        res = json.loads(data['trades'])
        result = dh.give_result_backtest(name, res, data['config'])
        return JsonResponse(result, safe=False)
    else:
        return Http404('this is not a GET!')


@login_required(login_url='accounts:userena_signin')
def display(request):
    return render(request, 'applyTheme.html', {'SymbolId': 'IRO1IKCO0001', 'username': request.user.username})


def about_us(request):
    return render(request, 'aboutus.html', {'username': request.user.username})


def index(request):
    login_status = True if not request.user.username else False
    return render(request, 'newindex.html',
                  {'form': AuthenticationForm, 'login_status': login_status, 'username': request.user.username}
                  )
def stockwatch(request,SymbolId):
    if not SymbolId:
        return redirect('/stockwatch/IRO1IKCO0001')
    from data.models import StockWatch as st
    stock = st.objects.get(SymbolId=SymbolId)
    stockWatchDict = {'SymbolId': stock.SymbolId, 'title':stock.InstrumentName}
    return render(request, 'stockwatch.html', stockWatchDict)