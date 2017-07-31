import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, redirect
# from django.shortcuts import
from data.models import StockWatch as Symbol
from finance import data_handling as dh, indicator


# from main import indicator