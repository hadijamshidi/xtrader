import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render
from accounts.forms import AuthenticationForm
from data.models import StockWatch as Symbol
from finance import data_handling as dh, indicator


# from main import indicator


def ssl(request):
    return HttpResponse('ODxZzdF8g1qVVcaBy7TTYI9PwVWD_65sFjIlPpDq2Oo.k6aH7_MEwQSb7bHkMzEABjDvdGgv8H5p7iYRvDVGzNE')


def symbol_search(request, query):
    symbols = Symbol.objects.filter(mabna_short_name__istartswith=query) \
              | Symbol.objects.filter(mabna_english_name__icontains=query) \
        # | Symbol.objects.filter(name__icontain=query)
    symbol_max_results = 8
    if symbols.count() < symbol_max_results:
        symbols = symbols | Symbol.objects.filter(mabna_name__icontains=query)
    results = [ob.as_json() for ob in symbols]
    mydict = dict(
        items=results,
    )
    return HttpResponse(json.dumps(mydict, ensure_ascii=False).encode("utf8"),
                        content_type="application/json; charset=utf-8")


def get_data(request, name):
    from data import redis
    import pandas as pd
    data_dict = redis.load_history(name)
    df = pd.DataFrame(data=data_dict, index=data_dict['date'])
    df = df.loc[:, ['date', 'open', 'high', 'low', 'close', 'volume']]
    # stock = Symbol.objects.get(symbol_id=name)
    stock_information = dict(
        # per_name=stock.mabna_short_name,
        # measurement_name=name,
        # name=stock.mabna_name,
        per_name='خودرو',
        measurement_name=name,
        name='خودرو',
    )
    stock_history = df.to_json(orient='values')
    stock_information['items'] = stock_history
    return JsonResponse(json.dumps(stock_information), safe=False)


def indicators_api(request):
    if request.method == 'POST':
        return JsonResponse(json.dumps(indicator.get_group_api()), safe=False)
    else:
        return JsonResponse(json.dumps({'api': 'null'}), safe=False)


@login_required(login_url='accounts:userena_signin')
def display(request):
    return render(request, 'applyTheme.html', {'SymbolId': 'IRO1IKCO0001', 'username': request.user.username})


def index(request):
    login_status = True if not request.user.username else False
    return render(request, 'index.html',
                  {'form': AuthenticationForm, 'login_status': login_status, 'username': request.user.username}
                  )


def back_test(request):
    if request.method == 'POST':
        data = json.loads(request.POST['param'])
        name = data['name']
        res = json.loads(data['trades'])
        print(data['config'])
        result = dh.give_result_backtest(name, res, data['config'])
        return JsonResponse(result, safe=False)
    else:
        return Http404('this is not a Post!')


def about_us(request):
    return render(request, 'aboutus.html', {'username': request.user.username})


def stockwatch(request, SymbolId):
    stockWatchDict = {}
    return render(request, 'aboutus.html', stockWatchDict)
