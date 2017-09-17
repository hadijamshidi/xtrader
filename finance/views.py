from finance import data_handling, volume
from django.http import HttpResponse, JsonResponse
import json
from . import strategy, scan, marketwatch
from finance import data_handling as dh, indicator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseNotFound
from accounts.forms import AuthenticationForm
import requests as r
from xtrader.localsetting import farabi_login_data
from data.backup import filters_data
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import inspect
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

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


@login_required(login_url='accounts:userena_signin')
def market_watch(request):
    return render(request, 'marketwatch.html', get_user(request))


def getfilters(request):
    return HttpResponse(json.dumps(filters_data))


def filtermarket(request):
    filters = json.loads(request.GET['filters'])
    # order_by = request.GET['sort_by']
    # print(order_by)
    from data import dates as d
    last = d.Check().last_market()
    from data.models import MarketWatch
    stocks = MarketWatch.objects.filter(stockWatch__LastTradeDate=last).order_by('-stockWatch__TotalTradeValue')
    if len(filters) > 0:
        D = {}
        for f in filters:
            d = json.loads(f)
            D = {**D, **d}
        stocks = stocks.filter(**D)
    paginator = Paginator(stocks, 10)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        stocks = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = 1
        stocks = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.num_pages
        stocks = paginator.page(paginator.num_pages)
    d = {'last':paginator.num_pages, 'former':paginator.num_pages-1,'former2':paginator.num_pages-2}
    return render(request, 'marketwatchTable.html', {'stocks': stocks, **d})


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
    return render(request, 'back.html', {'SymbolId': 'IRO1IKCO0001', **get_user(request=request)})


def about_us(request):
    return render(request, 'aboutus.html', {'username': request.user.username})


def index(request):
    login_status = True if not request.user.username else False
    return render(request, 'newindex.html',
                  {'form': AuthenticationForm, 'login_status': login_status, 'username': request.user.username}
                  )


@login_required(login_url='accounts:userena_signin')
def stockwatch(request, SymbolId):
    if not SymbolId:
        return redirect('/stockwatch/IRO1IKCO0001')
    from data.models import StockWatch as st
    stock = st.objects.filter(SymbolId=SymbolId).first()
    stockWatchDict = {'SymbolId': stock.SymbolId, 'title': stock.InstrumentName, **get_user(request)}
    return render(request, 'stockwatch.html', stockWatchDict)


def get_user(request):
    username = request.user.username
    user = User.objects.get_by_natural_key(username=username)
    name = user.get_full_name()
    url = '/media/pictures/hadi.jpeg' if username == 'hadi' else 'https://www.awicons.com/free-icons/download/application-icons/dragon-soft-icons-by-artua.com/png/512/User.png'
    return {'name': name, 'img_url': url}


def farabi(request):
    return render(request, 'farabi.html', get_user(request))


def ssl(request):
    return HttpResponse('_4__Dydo_r-Odxp9vmfg6O0yztz4wubxg1pI_hjN61w.roFR2cIPsmsvrAbcUKyEWeWbhw-5q0XtVPqbbDoFZzs')


def trade(request):
    data = request.GET['order']
    data = json.loads(data)
    user = r.session()
    user.post('http://api.farabixo.com/api/account/repo/login', data=farabi_login_data)
    orderId = user.post('http://api.farabixo.com/api/pub/AddOrder', data=data)
    return HttpResponse(orderId.text)


def portfo(request):
    portfo = []
    if request.user.username == 'broker':
        user = r.session()
        user.post('http://api.farabixo.com/api/account/repo/login', data=farabi_login_data)
        portfo = user.get('http://api.farabixo.com/api/pub/GetAssetList').text
        portfo = json.loads(portfo)
    return render(request, 'portfo.html', {'portfo': portfo})


def orders(request):
    orders = []
    # orders = [
    #     {'OrderState': 'درصف', 'OrderId': 5645, 'OrderSideId': 'فروش', 'SymbolId': 'IR6451313', 'InstrumentName': 'تست',
    #      'Quantity': 'Quantity', 'Price': 'Price'}]
    if request.user.username == 'broker':
        user = r.session()
        user.post('http://api.farabixo.com/api/account/repo/login', data=farabi_login_data)
        orders = user.get('http://api.farabixo.com/api/pub/GetOrderList').text
        orders = json.loads(orders)
        for order in orders:
            order['OrderSideId'] = 'خرید' if order['OrderSideId'] == 1 else 'فروش'
    return render(request, 'orders.html', {'orders': orders})


def account_status(request):
    user = r.session()
    user.post('http://api.farabixo.com/api/account/repo/login', data=farabi_login_data)
    account = user.get('http://api.farabixo.com/api/pub/GetAccountState').text
    # return render(request, 'status.html', {'account': json.loads(account)})
    return HttpResponse(account)


# {'WithdrawableMoneyRemain': 2089426.0, 'BlokedValue': 0.0, 'WithdrawableBlockedMoney': 0.0, 'CreditMoney': 0.0, 'CreditBlockedMoney': 0.0, 'TotalAsset': 2619560.0, 'NonWithdrawableMoneyRemain': 0.0, 'CreditMoneyRemain': 0.0, 'PercentageProfit': 26.0, 'Profit': 109384.0, 'BuyingPower': 2089426.0, 'NonWithdrawableBlockedMoney': 0.0}


def cancelOrder(request):
    user = r.session()
    user.post('http://api.farabixo.com/api/account/repo/login', data=farabi_login_data)
    output = user.post('http://api.farabixo.com/api/pub/CancelOrder', data={'OrderId': request.GET['OrderId']}).text
    return HttpResponse(output)


def editOrder(request):
    user = r.session()
    user.post('http://api.farabixo.com/api/account/repo/login', data=farabi_login_data)
    data = json.loads(request.GET['order'])
    print(data)
    output = user.post('http://api.farabixo.com/api/pub/ModifyOrder', data=data).text
    return HttpResponse(output)


def test_volume(request):
    return render(request, 'test_volume.html', {'SymbolId': 'IRO1IKCO0001', **get_user(request=request)})


def manage_volume(request):
    data = json.loads(request.GET['param'])
    result = volume.run_test(data)
    # print(result['history'])
    return render(request, 'volumetest.html', result)


def testAPI(request):
    return render(request, 'testAPI.html', {'SymbolId': 'IRO1IKCO0001', **get_user(request=request)})
