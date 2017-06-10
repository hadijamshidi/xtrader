from django.shortcuts import render
from finance import data_handling
from django.http import HttpResponse, JsonResponse
import json
# Create your views here.

# def get_function(name):
#     return all_functions['give_result_' + name.lower()]


# @shared_task
# def calc_filter(kind, data, get_json=True):
#     fun = get_function(kind)
#     # print('calc filter done :p')
#     return fun(data, None, get_json)

import inspect
all_functions = dict(inspect.getmembers(data_handling, inspect.isfunction))

def calculate_indicators(request):
    data = json.loads(request.POST['param'])
    kind = data['kind'].lower()
    # print(kind)
    # print(data)
    function = all_functions['give_result_' + kind]
    result = function(data)
    # res = Filter.make_filter(data).calculate()
    return JsonResponse(result,safe=False)