from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, Http404
from finance.models import Strategy

# Create your views here.


def show_trader_strategy(request, trader, strategy):
    return HttpResponse('good')
    # pass
