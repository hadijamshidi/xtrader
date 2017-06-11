import json

from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render

from api.models import Stock as Symbol
from finance import data_handling as dh
from main import indicator


#
# influx_client = DataFrameClient(settings.INFLUX_DB['host'], settings.INFLUX_DB['port'], settings.INFLUX_DB['user'],
#                                 settings.INFLUX_DB['password'], settings.INFLUX_DB['db_name'])
#
#
# def aidin(request):
#     symbols = Symbol.objects.all()
#     return render(request, 'index.html', {'items': symbols, 'username': request.user.username})
#
#
# def item_detail(request, name):
#     try:
#         symbol = Symbol.objects.get(eng_name=name)
#         result = influx_client.query("SELECT * FROM {measurement_name}".format(measurement_name=name))
#
#         symbol_name = result[name]['<TICKER>'][0]
#         df = result[name]
#         df['<TIME>'] = df.index
#         df = df.loc[:, ['<TIME>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>']]
#
#         j = df.to_json(orient='values')
#     except Symbol.DoesNotExist:
#         raise Http404(
#             'This item does not exist!')
#     return render(request, 'item_datails.html',
#                   {'item': symbol, 'name': symbol_name, 'measurement_name': name, 'json': j,
#                    'username': request.user.username})
#
#
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


#
#
# @login_required(login_url='/account/login/')
def get_data(request, name):
    from data import redis
    from task import testdate
    import pandas as pd
    # needs = ['open', 'high', 'low', 'close','volume']
    # data_dict = dict()
    # for need in needs:
    #     data_dict[need] = json.loads(r.hget(name=name, key=need))
    # days = eval(r.hget(name=name, key='date'))[::-1]
    # date = [testdate.jalali_to_timestamp(day) for day in days]
    # data_dict['date'] = date
    # df = pd.DataFrame(data=data_dict, index=date)
    data_dict = redis.load_history(name)
    df = pd.DataFrame(data=data_dict,index=data_dict['date'])
    df = df.loc[:, ['date', 'open', 'high', 'low', 'close', 'volume']]
    stock = Symbol.objects.get(symbol_id=name)
    stock_information = dict(
        per_name=stock.mabna_short_name,
        measurement_name=name,
        name=stock.mabna_name,
    )
    stock_history = df.to_json(orient='values')

    stock_information['items'] = stock_history
    return JsonResponse(json.dumps(stock_information), safe=False)


# def get_data(request, name):
#     result = influx_client.query("SELECT * FROM {measurement_name}".format(measurement_name=name))
#     per_name = Symbol.objects.filter(eng_name=name).first().symbol_name
#
#     symbol_name = result[name]['<TICKER>'][0]
#     mydict = dict(
#         name=symbol_name,
#         measurement_name=name,
#         per_name=per_name
#     )
#
#     if request.method == 'GET':
#         df = result[name]
#         df['<TIME>'] = df.index
#         df = df.loc[:, ['<TIME>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>']]
#
#         j = df.to_json(orient='values')
#
#         mydict['items'] = j
#         return JsonResponse(json.dumps(mydict), safe=False)
#     else:
#         return JsonResponse(json.dumps(mydict), safe=False)


def indicators_api(request):
    if request.method == 'POST':
        return JsonResponse(json.dumps(indicator.get_group_api()), safe=False)
    else:
        return JsonResponse(json.dumps({'api': 'null'}), safe=False)


# @login_required(login_url='/account/login/')
def display(request):
    # if not request.user.username == 'aidin':
    #     bot.send_message(request.user.username + ' goes to finance page!')
    # return render(request, 'applyTheme.html', {'username': request.user.username,'bool1':True,'bool2':True})
    return render(request, 'applyTheme.html', {'SymbolId': 'IRO1IKCO0001'})

# @login_required(login_url='/account/login/')
# def display_item(request, stock_name):
#     q = Symbol.had_DB.filter(eng_name=stock_name)
#     if not q.exists():
#         return HttpResponseBadRequest("<h3><center>چنین نمادی وجود ندارد!</center></h3>")
#     else:
#         return render(request, 'applyTheme.html', {'username': request.user.username, 'symbol_name': stock_name})


# def index(request):
#     bot.send_details(request, 'index ')
#     return render(request, 'index.html', {'username': request.user.username, 'form': UserLoginForm})
#
#
# def calculate_indicators(request):
#     if request.method == 'POST':
#         data = json.loads(request.POST['param'])
#         print(data)
#         from main.tasks import calc_filter
#         # result = calc_filter(data)
#         result = calc_filter.delay(data).get()
#         return JsonResponse(result, safe=False)
#     else:
#         return Http404('this is not a Post!')
#
#
# def update_indicators(request):
#     if request.method == 'POST':
#         data = json.loads(request.POST['param'])
#         result = dh.give_update_indicators(data)
#         return JsonResponse(result, safe=False)
#     else:
#         return Http404('this is not a Post!')
#
#
# def amir(request):
#     if request.method == 'POST':
#         data = json.loads(request.POST['param'])
#         result = dh.amir(data)
#         return JsonResponse(result, safe=False)
#     else:
#         return Http404('this is not a Post!')
#
#
def back_test(request):
    if request.method == 'POST':
        data = json.loads(request.POST['param'])
        name = data['name']
        res = json.loads(data['trades'])
        result = dh.give_result_backtest(name, res, data['config'])
        return JsonResponse(result, safe=False)
    else:
        return Http404('this is not a Post!')
#
#
def about_us(request):
    # bot.send_details(request, 'about us')
    return render(request, 'aboutus.html', {'username': request.user.username})
#
#
# def test(request):
#     text = '<script src="//raw.githack.com/tahajahangir/jdate/master/jdate-class.js"></script><script>jd = new JDate(new Date(1990, 7, 30));console.log(jd);</script>'
#     return HttpResponse(text)
#
#
# def base(request):
#     return render(request, 'base.html', {'username': request.user.username})
