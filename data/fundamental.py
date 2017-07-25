from .crawl import IncomeIndex,RatioIndex,balanceIndex
from data.models import StockWatch as ss
from .models import Income,balanceSheet,Ratio
Balance_sheet={'سرمایه گذاری کوتاه مدت': 'short_term_investments', 'دارایی': 'total_assets', 'حقوق صاحبان سهام': 'equity', 'حساب دریافتنی': 'net_receivables', 'دارایی جاری': 'total_current_assets', 'وجه نقد': 'cash', 'سرمایه': 'capital', 'بدهی جاری': 'total_current_liabilities', 'سود انباشته': 'retained_earnings', 'سرمایه گذاری بلند مدت': 'long_term_investments', 'موجودی کالا': 'inventory', 'پیش  پرداخت': 'prepayment', 'دارایی نامشهود': 'intangible_assets', 'دارایی ثابت': 'property_plant_and_equipment', 'بدهی': 'total_liabilities', 'حساب پرداختنی': 'accounts_payable'}
incom =  {'سود ناخالص': 'gross_profit', 'سود عملیاتی': 'operating_income_or_loss', 'سود قبل مالیات': 'income_before_tax',
     'فروش': 'total_income', 'سود خالص': 'net_income', 'هزینه مالی': 'interest_expense'}
Ratio1 = {'بازده دارایی (درصد)': 'roa', 'دوره گردش حساب دریافتنی (روز)': 'accounts_receivable_turnover_ratio', 'دوره گردش حساب پرداختنی (روز)': 'accounts_payable_turnover_ratio', 'نقد': 'cash_ratio', 'جاری': 'current_ratio', 'بدهی(درصد)': 'da','بازده ح ص س (درصد)': 'roe', 'حاشیه سود خالص (درصد)': 'profit_margin', 'هزینه بهره به سود عملیاتی (درصد)': 'r_ebit', 'دوره گردش موجودی کالا(روز)': 'inventory_turnover_ratio', 'سود عملیاتی به سود ناخالص(درصد)': 'ebit_gross_profit','گردش دارای(بار)': 'sa', 'آنی': 'quick_ratio', 'حاشیه سود ناخالص (درصد)': 'gross_profit_margin', 'بدهی به ح ص س': 'de'}

# r= {k.lower(): v.lower()  for k, v in {"your": "DATA", "FROM": "above"}.items()}

wrong_symbol_ids = []

def createIncomTables(num=0):
    for stock in ss.objects.all():
        print(stock.InstrumentName)
        try:
            info = IncomeInfo(stock,stock.InstrumentName)
            print(info)
            # try:


            # except Exception:
            #     wrong_symbol_ids.append(dict(instrumentName=stock.InstrumentName,problem='on save'))
        except Exception:
            wrong_symbol_ids.append(dict(instrumentName=stock.InstrumentName, problem='fipiran'))
        if info:
            addIncomeTable(info)

def IncomeInfo(stock,InstrumentName):
        trades_data=IncomeIndex(InstrumentName)
        trades_dict = {}
        trades_dict['StockWatch'] = stock
        trades_dict['InstrumentName'] = InstrumentName
        for key in trades_data:

                trades_dict[incom[key]] = trades_data[key]
        return trades_dict

def addIncomeTable(info):
    Income(**info).save()
    print('successful progress')



def createBalanceTables(num=0):
    for stock in ss.objects.all():
        print(stock.InstrumentName)
        try:
            info = BalanceInfo(stock,stock.InstrumentName)
            print(info)
            # try:
            #     addbalanceTable(info)
            #
            # except Exception:
            #     wrong_symbol_ids.append(dict(instrumentName=stock.InstrumentName,problem='on save'))
        except Exception:
            wrong_symbol_ids.append(dict(instrumentName=stock.InstrumentName, problem='fipiran'))
        # if info:
        addbalanceTable(info)


def BalanceInfo(stock,InstrumentName):
        trades_data=balanceIndex(InstrumentName)
        trades_dict = {}
        trades_dict['StockWatch'] = stock
        trades_dict['InstrumentName'] = InstrumentName
        for key in trades_data:

                trades_dict[Balance_sheet[key]] = trades_data[key]
        return trades_dict

def addbalanceTable(info):
    balanceSheet(**info).save()
    print('successful progress')



def createRatioTables(num=0):
    for stock in ss.objects.all():
        print(stock.InstrumentName)
        info = RatioInfo(stock,stock.InstrumentName)
        # print(info)

        try:
            addRatioTable()

        except Exception:
            wrong_symbol_ids.append(dict(instrumentName=stock.InstrumentName,problem='on save'))
        # except Exception:
        #     wrong_symbol_ids.append(dict(instrumentName=stock.InstrumentName, problem='fipiran'))
        # if info:
        # if info:



def RatioInfo(stock,InstrumentName):
        try:
            trades_data=RatioIndex(InstrumentName)
        except Exception:
            return False
        trades_dict = {}
        trades_dict['StockWatch'] = stock
        trades_dict['InstrumentName'] = InstrumentName
        for key in trades_data:

                trades_dict[Ratio1[key]] = trades_data[key]
        return trades_dict

def addRatioTable(info):
    Ratio(**info).save()
    print('successful progress')
# TODO write clean function for duplicate above