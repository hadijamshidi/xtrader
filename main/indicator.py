from django.conf import settings
# TODO: handle db
# from influxdb import DataFrameClient
import pandas as pd
import numpy as np
import talib
from api import redis
columns = ['<TIME>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>']
fields = ['Open', 'High', 'Low', 'Close', 'Volume']

# TODO: replace ...
# host = settings.INFLUX_DB['host']
# port = settings.INFLUX_DB['port']
# user = settings.INFLUX_DB['user']
# password = settings.INFLUX_DB['password']
# db_name = settings.INFLUX_DB['db_name']


class Indicator:
    def __init__(self, name=None, tail=None):
        if name:
            self.set_symbol(name, tail)
        else:
            self.name = ''
            self.df = pd.DataFrame()
            self.inputs = dict()

    def set_symbol(self, name, tail=None):
        self.SymbolId = name
        self.name = name
        self.df = self.load_db(tail)
        self.inputs = dict()
        for c in self.df.columns:
            if c != 'time':
                self.inputs[c] = np.asarray(self.df[c], dtype='f8')

    def load_db(self, tail=None):
        db = redis.load_history(self.SymbolId)
        df = pd.DataFrame(db)
        # measurement_name = self.name
        # TODO: replace client
        # client = DataFrameClient(host, port, user, password, db_name)
        # if not tail:
        #     query_text = "Select * from {pointname}".format(pointname=measurement_name)
        #     # df = client.query(query_text)[measurement_name]
        # else:
        #     query_text = "Select * from {pointname} order by time DESC LIMIT {tail}".format(pointname=measurement_name,
                                                                                            # tail=tail)
            # df = client.query(query_text)[measurement_name].iloc[::-1]
        # df['<TIME>'] = df.index
        df.index = df['date']
        df = df.loc[:, ['date', 'open', 'high', 'low', 'close', 'volume']]
        df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
        return df

    def ichimoku(self, *args, **kwargs):
        # print('ichimoku')
        # print('args')
        # print(args)
        # print('kwargs')
        # print(kwargs)
        # conversion line period
        cl = float(kwargs['conversionLineperiod'])
        # base line
        bl = float(kwargs['BaseLineperiod'])
        # Sen span B
        ssB = float(kwargs['LagingB'])

        variable = {'function_name': 'MAX', 'price': 'high', 'timeperiod': cl}
        hh = pd.DataFrame(self.indicator_calculator(**variable))
        variable = {'function_name': 'MIN', 'price': 'low', 'timeperiod': cl}
        ll = pd.DataFrame(self.indicator_calculator(**variable))
        Tenkan = ((ll + hh) / 2)
        outdf = pd.DataFrame(Tenkan)

        variable = {'function_name': 'MAX', 'price': 'high', 'timeperiod': bl}
        hh = pd.DataFrame(self.indicator_calculator(**variable), copy=True)
        variable = {'function_name': 'MIN', 'price': 'low', 'timeperiod': bl}
        ll = pd.DataFrame(self.indicator_calculator(**variable), copy=True)
        kijun = ((ll + hh) / 2)

        senkouA = (Tenkan + kijun) / 2
        outdf['Kijun-sen'] = kijun
        outdf['Senkou Span A'] = senkouA.shift(bl)

        variable = {'function_name': 'MAX', 'price': 'high', 'timeperiod': ssB}
        hh = pd.DataFrame(self.indicator_calculator(**variable), copy=True)
        variable = {'function_name': 'MIN', 'price': 'low', 'timeperiod': ssB}
        ll = pd.DataFrame(self.indicator_calculator(**variable), copy=True)
        senkouB = ((ll + hh) / 2)
        outdf['Senkou Span B'] = senkouB.shift(bl)

        # variable = {'function_name': 'close', 'shift': 52}
        ls = pd.DataFrame(self.inputs['close'])
        ls.index = outdf.index
        ls = pd.DataFrame(ls.shift(-bl), copy=True)
        outdf['Chikou Span'] = ls
        # print('ls:')
        # print(outdf.tail(10))
        outdf.columns = ['Tenkan-sen', 'Kijun-sen', 'Senkou Span A', 'Senkou Span B', 'Chikou Span']
        # print(outdf.tail(10))
        # outdf['Tenkan-sen'] = Tenkan
        # print(outdf.tail(55))
        # print(((Tenkan2+Tenkan)/2).tail(10))
        return outdf

    def indicator_calculator(self, function_name, symbol_name=None, tail=None, *args, **kwargs):
        if symbol_name:
            self.set_symbol(symbol_name, tail)

        if function_name.lower() in self.df.columns:
            outdf = pd.DataFrame(self.df[function_name.lower()])
            outdf.columns = ['real']
        elif function_name.lower() == 'ichimoku':
            outdf = self.ichimoku(self.inputs, *args, **kwargs)
        elif function_name.lower() == 'signal_line':
            c = 0
            if len(args) != 0:
                c = args[0]
            if kwargs:
                c = kwargs['value']
            outdf = pd.DataFrame(c * np.ones([len(self.df), 1]),
                                 index=self.df.index, columns=['real'])
        else:
            fun = talib.abstract.Function(function_name.upper())
            output = fun(self.inputs, *args, **kwargs)
            # to handle multi Dimensional output
            outdf = pd.DataFrame()
            if isinstance(output[0], np.ndarray):
                for o in output:
                    outdf = pd.concat([outdf, pd.DataFrame(o, index=self.df.index)], axis=1)
            else:
                outdf = pd.concat([outdf, pd.DataFrame(output, index=self.df.index)], axis=1)

            outdf.columns = fun.output_names
            outdf = outdf.apply(lambda x: round(x, 2))
        return outdf


def get_parameter(function_name):
    fun = talib.abstract.Function(function_name)
    md = dict()
    for t in list(fun.get_parameters().items()):
        md[t[0]] = t[1]
    return md


Rename_group_name_dic = {
    'fields': 'Historical Data',
    'Volume Indicators': 'Volume Indicators',
    'Overlap Studies': 'Trend Indicators',
    'Volatility Indicators': 'Volatility Indicators',
    'Momentum Indicators': 'Momentum Indicators',
    'Pattern Recognition': None,
    'Statistic Functions': None,
    'Price Transform': None,
    'Cycle Indicators': None,
    'Math Transform': None,
    'Math Operators': None,
}

Bad_indicators = ['MAVP']


def get_group_api():
    # add signal lines to api
    mdic = dict(
        signal_line=dict(
            fun_name='signal_line',
            params=dict(value=0),
            settings=dict(shift=0),
            outputs=dict(real=['line', 'solid'])
        )
    )
    # add ohlcv to api
    for field_name in fields:
        mdic[field_name] = dict(
            fun_name=field_name.lower(),
            settings=dict(shift=0),
            outputs=dict(real=['line', 'solid'])
        )
    mdic['Volume']['outputs']['real'][0] = 'column'
    # add talib functions
    dic = dict()
    # keys are group names
    # value are indicators in a group
    for key, value in talib.get_function_groups().items():
        key = Rename_group_name_dic[key]
        if key:
            idic = dict()
            for fun_name in value:
                if fun_name not in Bad_indicators:
                    name = fun_name + '(' + talib.abstract.Function(fun_name).info['display_name'] + ')'
                    idic[name] = dict(
                        fun_name=fun_name,
                        settings=dict(
                            shift=0
                        )
                    )
                    idic[name]['params'] = get_parameter(fun_name)
                    output_dic = dict()
                    for li in list(talib.abstract.Function(fun_name).output_flags.items()):
                        output_dic[li[0]] = ['line', 'solid']
                        if li[1][0] == 'Histogram':
                            output_dic[li[0]][0] = 'column'
                        elif li[1][0] == 'Dashed Line':
                            output_dic[li[0]][1] = 'Dash'
                        elif li[1][0] == 'star':
                            output_dic[li[0]][1] = 'Dot'
                    idic[name]['outputs'] = output_dic
            dic[key] = idic
    dic['Historical Data'] = mdic
    return dic


def get_ti_api():
    dic = dict(
        signal_line=dict(
            fun_name='signal_line',
            params=dict(value=0),
            settings=dict(shift=0),
            outputs=dict(real=['line', 'solid'])
        )
    )

    for field_name in fields:
        dic[field_name] = dict(
            fun_name=field_name.lower(),
            settings=dict(
                shift=0
            ),
            outputs=dict(real=['line', 'solid'])
        )
    dic['Volume']['outputs']['real'][0] = 'column'
    for fun_name in talib.get_functions():
        if fun_name not in Bad_indicators:
            name = fun_name + '(' + talib.abstract.Function(fun_name).info['display_name'] + ')'
            dic[name] = dict(
                fun_name=fun_name,
                settings=dict(
                    shift=0
                )
            )
            dic[name]['params'] = get_parameter(fun_name)
            output_dic = dict()
            for li in list(talib.abstract.Function(fun_name).output_flags.items()):
                output_dic[li[0]] = ['line', 'solid']
                if li[1][0] == 'Histogram':
                    output_dic[li[0]][0] = 'column'
                elif li[1][0] == 'Dashed Line':
                    output_dic[li[0]][1] = 'Dash'
                elif li[1][0] == 'star':
                    output_dic[li[0]][1] = 'Dot'
            dic[name]['outputs'] = output_dic
    return dic


def add_time(df):
    outdf = pd.concat([pd.DataFrame(df.index, index=df.index), df], axis=1)
    outdf.columns = ['time'] + list(df.columns)
    return outdf


def to_json(df):
    return add_time(df).to_json(orient='values')


def read_json(json):
    df = pd.read_json(json)
    df = df.set_index(df[0]).iloc[:, 1:]
    return df


if __name__ == "__main__":
    # mt = Indicator(name='IranKhodro_D_SH')
    # # d = dict(
    # #     value=10,
    # # )
    # # o1 = mt.indicator_calculator('signal_line', **d)
    # # print(o1)
    # o2 = mt.indicator_calculator('SMA')
    # s = talib.abstract.Function('SMA')
    # t = list(s.output_flags.items())
    # print(t)
    print(get_ti_api())
