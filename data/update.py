from data.fundamental import Fundamental
from data.stockwatch import update_stock_watch
from data.update_history import update_history_with_farabixo
from django.http import HttpResponse
from data import fundamental
from data import stockwatch
from data.historicalprice import add_new_history
from data.models import StockWatch, MarketWatch, BalanceSheet, Income, Ratio


def update_all_data(only_history=False):
    if only_history:
        return update_history_with_farabixo(update_stock_watch=False)
    update_stock_watch()
    f = Fundamental()
    for table in ['ratio', 'income', 'balance', 'marketwatch']:
        f.update(table)
    return update_history_with_farabixo(update_stock_watch=False)


def add_symbol(symbol_id):
    is_exist = StockWatch.objects.filter(SymbolId=symbol_id).count()
    if is_exist >= 1:
        return "This Symbol is exist."
    stockwatch.addStockWatchTable(stockwatch.stockWatchInfo(symbol_id))
    stock = StockWatch.objects.get(SymbolId=symbol_id)
    fundamental.addBalanceTable(fundamental.BalanceInfo(stock, stock.InstrumentName))
    fundamental.addIncomeTable(fundamental.IncomeInfo(stock, stock.InstrumentName))
    fundamental.addRatioTable(fundamental.RatioInfo(stock, stock.InstrumentName))
    fundamental.addMarketWatchTable(fundamental.marketwatchinfo(stock))
    add_new_history(stock)
    return "Your stock added successfully."


def remove_symbol(symbol_id):
    # symbol_id = request.GET['symbol_id']
    stock = StockWatch.objects.filter(SymbolId=symbol_id)
    StockWatch.objects.filter(SymbolId=symbol_id).delete()
    MarketWatch.objects.filter(stockWatch=stock).delete()
    BalanceSheet.objects.filter(SymbolId=symbol_id).delete()
    Ratio.objects.filter(SymbolId=symbol_id).delete()
    Income.objects.filter(SymbolId=symbol_id).delete()
    return "Removed Successfully."
