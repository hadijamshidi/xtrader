import bs4 as b
import requests as r

def clean(value, kind='number'):
    if value[-1] == ' ':
        value = value[:-1]
    if value[0] == ' ':
        value = value[1:]
    if kind == 'number':
        value = value.replace(',','')
        if value[0] == '(':
            value = eval('(-'+value[1:])
        else:
            value = eval(value)
    return value


def crawler(url, data):
    page = r.get(url, params=data)
    soup = b.BeautifulSoup(page.content, "html.parser")
    tbody = soup.find_all('tr')
    result = {}
    title = ''
    for tr in tbody[1:]:
        for i, td in enumerate(tr):
            if i == 1:
                title = clean(td.string,'string')
            if i == 21:
                result[title] = clean(td.string)
    return result


def balanceIndex(symbol='خودرو'):
    url = 'http://www.fipiran.com/Symbol/BalanceType1210Year'
    data = {'symbolpara': symbol}
    return crawler(url, data)


def IncomeIndex(symbol='خودرو'):
    data = {'symbolpara': symbol}
    url = 'http://www.fipiran.com/Symbol/IncomeType1210Year'
    return crawler(url=url, data=data)



def RatioIndex(symbol='خودرو', year=1395):
    data = {'symbolpara': symbol}
    url = 'http://www.fipiran.com/Symbol/RatioType1210Year'
    return crawler(url=url, data=data)


# def CGARIndex(symbol='خودرو', year=1395):
#     url = 'http://www.fipiran.com/Symbol/CGAR1210Year'
#     params = {'symbolpara': symbol}
#     return crawler(url=url, data=params, method='get')
