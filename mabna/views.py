from django.shortcuts import render
# Create your views here.
from django.http import JsonResponse, HttpResponse
import json, requests
from xtrader import localsetting as local


def get(request):
    if local.client['job'] == 'dev':
        result = dict()
        for k in request.GET:
            result[k] = request.GET[k]
        r = requests.get(local.client['url'] + '/maban/api', params=result)
    if local.client['job'] == 'server':
        r = requests.get(local.client['url'] + request.GET['url'], headers=local.client['auth'])
    return HttpResponse(json.dumps(r))
