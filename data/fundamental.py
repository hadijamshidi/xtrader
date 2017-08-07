from .models import Income, BalanceSheet, Ratio, MarketWatch
from .crawl import IncomeIndex, RatioIndex, balanceIndex
from data.models import StockWatch
from data import backup

Balance_sheet = backup.Balance_sheet
income = backup.income
Ratio1 = backup.Ratio

wrong_symbol_ids = []


def createIncomeTables(num=0):
    for i, stock in enumerate(StockWatch.objects.all()):
        if i >= num:
            print(i)
            try:
                info = IncomeInfo(stock, stock.InstrumentName)
                if info:
                    addIncomeTable(info)
            except Exception:
                wrong_symbol_ids.append(dict(instrumentName=stock.InstrumentName, problem='fipiran income table'))


def IncomeInfo(stock, InstrumentName):
    trades_data = IncomeIndex(InstrumentName)
    trades_dict = dict(StockWatch=stock, InstrumentName=InstrumentName, SymbolId=stock.SymbolId)
    for key in trades_data:
        trades_dict[income[key]] = trades_data[key]
    return trades_dict


def addIncomeTable(info):
    Income(**info).save()
    print('successful progress')


def createBalanceTables(num=0):
    for i, stock in enumerate(StockWatch.objects.all()):
        if i >= num:
            print(i)
            try:
                info = BalanceInfo(stock, stock.InstrumentName)
                if info:
                    addBalanceTable(info)
            except Exception:
                wrong_symbol_ids.append(dict(instrumentName=stock.InstrumentName, problem='fipiran balance'))


def BalanceInfo(stock, InstrumentName):
    trades_data = balanceIndex(InstrumentName)
    trades_dict = dict(StockWatch=stock, InstrumentName=InstrumentName, SymbolId=stock.SymbolId)
    for key in trades_data:
        trades_dict[Balance_sheet[key]] = trades_data[key]
    return trades_dict


def addBalanceTable(info):
    BalanceSheet(**info).save()
    print('successful progress')


def createRatioTables(num=0):
    for i, stock in enumerate(StockWatch.objects.all()):
        if i >= num:
            print(i)
            try:
                info = RatioInfo(stock, stock.InstrumentName)
                if info:
                    addRatioTable(info)
            except Exception:
                wrong_symbol_ids.append(dict(instrumentName=stock.InstrumentName, problem='fipiran ratio'))


def RatioInfo(stock, InstrumentName):
    try:
        trades_data = RatioIndex(InstrumentName)
    except Exception:
        return False
    trades_dict = dict(StockWatch=stock, InstrumentName=InstrumentName, SymbolId=stock.SymbolId)
    for key in trades_data:
        trades_dict[Ratio1[key]] = trades_data[key]
    return trades_dict


def addRatioTable(info):
    Ratio(**info).save()
    print('successful progress')


# TODO: wrong functions !!!
def cleanduplicateRatio():
    for row in Ratio.objects.all():
        if Ratio.objects.filter(SymbolId=row.SymbolId).count() > 1:
            row.delete()


def cleanduplicatebalanceSheet():
    for row in BalanceSheet.objects.all():
        if BalanceSheet.objects.filter(SymbolId=row.SymbolId).count() > 1:
            row.delete()


def cleanduplicateIncome():
    for row in Income.objects.all():
        if Income.objects.filter(SymbolId=row.SymbolId).count() > 1:
            row.delete()


def createMarcketwatchTables(num=0):
    for i, stock in enumerate(StockWatch.objects.all()):
        if i >= num:
            print(i)
            try:
                info = marketwatchinfo(stock)
                if info:
                    addMaketWatchTabe(info)
            except Exception:
                wrong_symbol_ids.append(dict(instrumentName=stock.InstrumentName, problem='create marketwatch'))


def marketwatchinfo(stock):
    mstock = stock.read()
    try:
        mincome = Income.objects.filter(SymbolId=stock.SymbolId).first().read()
    except Exception:
        mincome = {}
    try:
        mbalanceSheet = BalanceSheet.objects.filter(SymbolId=stock.SymbolId).first().read()
    except Exception:
        mbalanceSheet = {}
    try:
        mratio = Ratio.objects.filter(SymbolId=stock.SymbolId).first().read()
    except Exception:
        mratio = {}
    rmincome = {'income_' + k: v for k, v in mincome.items() if
                k not in ['InstrumentName', 'StockWatch_id', 'SymbolId', 'id']}
    rmbalanceSheet = {'balanceSheet_' + k: v for k, v in mbalanceSheet.items() if
                      k not in ['InstrumentName', 'StockWatch_id', 'SymbolId', 'id']}
    rmratio = {'ratio_' + k: v for k, v in mratio.items() if
               k not in ['InstrumentName', 'StockWatch_id', 'SymbolId', 'id']}
    rmstock = {'stockwatch_' + k: v for k, v in mstock.items() if k not in ['id']}
    try:
        info = {**rmstock, **rmincome, **rmbalanceSheet, **rmratio}
        return info
        # MarketWatch(**rmstock, **rmincome, **rmbalanceSheet, **rmratio).save()
    except Exception:
        return False


def addMaketWatchTabe(info):
    MarketWatch(**info).save()


def fullgetdata():
    from .stockwatch import createStockWatchTables, cleanduplicate
    createStockWatchTables()
    cleanduplicate()
    createRatioTables()
    cleanduplicateRatio()
    createBalanceTables()
    cleanduplicatebalanceSheet()
    createIncomeTables()
    cleanduplicateIncome()
    createStockWatchTables()


class Fundamental:
    @staticmethod
    def create_tables():
        fullgetdata()

    @staticmethod
    def update(table, num=0):
        table = table.lower()
        if table == 'ratio':
            update_ratio_tables(num)
        elif table == 'balance':
            update_balance_tables(num)
        elif table == 'income':
            update_income_tables(num)
        elif table == 'marketwatch':
            update_market_watch_tables(num)
        else:
            print('wrong table')


def update_ratio_tables(num=0):
    for i, stock in enumerate(StockWatch.objects.all()):
        if i >= num:
            print('try to update index: {}'.format(i))
            try:
                info = RatioInfo(stock, stock.InstrumentName)
                if info:
                    model = Ratio.objects.get(SymbolId=stock.SymbolId)
                    update_model(model, info)
            except Exception:
                wrong_symbol_ids.append(dict(instrumentName=stock.InstrumentName, problem='update ratio'))


def update_balance_tables(num):
    for i, stock in enumerate(StockWatch.objects.all()):
        if i >= num:
            print(i)
            try:
                info = BalanceInfo(stock, stock.InstrumentName)
                if info:
                    model = Income.objects.get(SymbolId=stock.SymbolId)
                    update_model(model, info)
            except Exception:
                wrong_symbol_ids.append(dict(instrumentName=stock.InstrumentName, problem='fipiran balance'))


def update_income_tables(num):
    for i, stock in enumerate(StockWatch.objects.all()):
        if i >= num:
            print(i)
            try:
                info = IncomeInfo(stock, stock.InstrumentName)
                if info:
                    model = Income.objects.get(SymbolId=stock.SymbolId)
                    update_model(model, info)
            except Exception:
                wrong_symbol_ids.append(dict(instrumentName=stock.InstrumentName, problem='update income table'))


def update_market_watch_tables(num):
    for i, stock in enumerate(StockWatch.objects.all()):
        if i >= num:
            print(i)
            try:
                info = marketwatchinfo(stock)
                if info:
                    model = MarketWatch.objects.get(stockwatch_SymbolId=stock.SymbolId)
                    update_model(model, info)
            except Exception:
                wrong_symbol_ids.append(dict(instrumentName=stock.InstrumentName, problem='update market watch table'))



def update_model(model, data):
    for key in data:
        model.__setattr__(key, data[key])
    model.save()
    print('{} updated successfully'.format(model.id))
