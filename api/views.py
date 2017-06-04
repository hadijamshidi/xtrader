from django.shortcuts import render
from api.data import create_company_table , call_threads_for_marketWatch
from api.models import Stock
from django.http import HttpResponse
import json
# Create your views here.
def stock(request):
    stocks = Stock.objects.all()
    stocks_list = []
    for stock in stocks:
        stocks_list.append({'id':stock.id,'symbol_id':stock.symbol_id,'mabna_id':stock.mabna_id,
                            'mabna_name':stock.mabna_name,'mabna_english_name': stock.mabna_english_name,
                            'mabna_short_name':stock.mabna_short_name,'mabna_kind':stock.mabna_kind})
        print(stocks_list)
    return HttpResponse(json.dumps(stocks_list))
def company():
    call_threads_for_marketWatch()
    return render('my_programs.html',
                  {'regs': 0})