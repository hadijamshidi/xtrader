from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required
# from account.forms import UserLoginForm
# from influxdb import DataFrameClient
# from bot import bot
# from .models import Symbol
# from . import indicator
# from . import data_handling as dh

# import json
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
# def symbol_search(request, query):
#     symbols = Symbol.objects.filter(symbol_name__istartswith=query, has_DB=True) \
#               | Symbol.objects.filter(eng_name__icontains=query, has_DB=True) \
#         # | Symbol.objects.filter(name__icontain=query)
#     symbol_max_results = 8
#     if symbols.count() < symbol_max_results:
#         symbols = symbols | Symbol.objects.filter(symbol_name__icontains=query, has_DB=True)
#     results = [ob.as_json() for ob in symbols]
#     mydict = dict(
#         items=results,
#     )
#     return HttpResponse(json.dumps(mydict, ensure_ascii=False).encode("utf8"),
#                         content_type="application/json; charset=utf-8")
#
#
# @login_required(login_url='/account/login/')
# def get_data(request, name):
#     if not request.user.username == 'aidin':
#         bot.send_message(request.user.username + ' search for symbol ' + name)
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
#
#
# def indicators_api(request):
#     if request.method == 'POST':
#         return JsonResponse(json.dumps(indicator.get_group_api()), safe=False)
#     else:
#         return JsonResponse(json.dumps({'api': 'null'}), safe=False)


# @login_required(login_url='/account/login/')
def display(request):
    # if not request.user.username == 'aidin':
    #     bot.send_message(request.user.username + ' goes to finance page!')
    # return render(request, 'applyTheme.html', {'username': request.user.username,'bool1':True,'bool2':True})
    return render(request, 'applyTheme.html')


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
# def back_test(request):
#     bot.send_details(request, 'finance')
#
#     if request.method == 'POST':
#         data = json.loads(request.POST['param'])
#         name = data['name']
#         res = json.loads(data['trades'])
#         result = dh.give_result_backtest(name, res, data['config'])
#         return JsonResponse(result, safe=False)
#     else:
#         return Http404('this is not a Post!')
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
