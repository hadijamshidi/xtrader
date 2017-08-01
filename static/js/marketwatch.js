/**
 * Created by hadi on 7/5/17.
 */
function show_filters_result(result) {
    var columns = {
        'num': 'ردیف',
        'stockwatch_InstrumentName': 'نماد', 'stockwatch_InstrumentTitle': 'نام',
        'stockwatch_TotalNumberOfTrades': 'تعداد',
        'stockwatch_TotalNumberOfSharesTraded': 'حجم', 'stockwatch_TotalTradeValue': 'ارزش',
        'stockwatch_PreviousDayPrice': 'دیروز', 'stockwatch_FirstTradePrice': 'اولین',
        'stockwatch_Eps': 'Eps',
        'stockwatch_PricePerEarning': 'P/E',
        'stockwatch_LastTradePrice': 'آخرین معامله', 'stockwatch_ReferencePriceVariationPercent': 'درصد آخرین معامله',
        'stockwatch_ReferencePriceVariation': 'تغییر آخرین معامله',
        'stockwatch_ClosingPrice': 'قیمت پایانی', 'stockwatch_ClosingPriceVariation': 'تغییر قیمت پایانی',
        'stockwatch_ClosingPriceVariationPercent': 'درصد  تغییر قیمت پایانی',
        'stockwatch_LowestTradePrice': 'کمترین', 'stockwatch_HighestTradePrice': 'بیشترین',
        'ratio_roa':'roa',
        'ratio_roe':'roe',
    };
    var place = document.getElementById("filters scan place");
    place.innerHTML = '';
    // creating table tag and attrs:
    var table = document.createElement("TABLE");
    table.setAttribute("id", "table");
    // table.setAttribute("style", "text-align:right");
    // table.setAttribute("class", "ui selectable inverted celled  table");
    place.appendChild(table);

    //creating tr for th tags:
    var tr = document.createElement('TR');
    Object.keys(columns).forEach(function (column) {
        var th = document.createElement('TH');
        th.appendChild(document.createTextNode(columns[column]));
        tr.appendChild(th);
    });
    table.appendChild(tr);

    // creating tr for td tags:
    // var div = document.createElement('table');
    // div.setAttribute('style', 'height: 400px; overflow: auto');
    var div = table;
    var num2 = 1;
    result.forEach(function (stock) {
        stock['num'] = num2;
        var tr = document.createElement('div');
        tr.setAttribute('class','divTableRow');
        if(num2 % 2 == 0) tr.setAttribute('style','background:#4d5068');
        num2 += 1;
        var num = 0;
        Object.keys(columns).forEach(function (column) {
            var td = document.createElement('div');
            td.setAttribute('class','divTableCell');
            if(num == 1){
                var a = document.createElement('a');
                a.appendChild(document.createTextNode(quick_check(stock[column])));
                a.setAttribute('href','/stockwatch/'+stock['stockwatch_SymbolId']);
                td.appendChild(a);
                tr.appendChild(td);

            }else{
                td.appendChild(document.createTextNode(quick_check(stock[column])));
                tr.appendChild(td);
            }
            num += 1;
        });
        div.appendChild(tr);
    });
    place.appendChild(div);
    place.appendChild(document.createElement('br'));
    place.style.display = 'block';
}

var filters_data = [
    {
        "benchmark": [0, 18, 25, 50, 75, 100, 200, 300],
        "target": [
            {'ratio_roe': 'ROE'},
            {'ratio_roa': 'ROA'},
            {'ratio_gross_profit_margin': 'حاشيه سود ناخالص'},
            {'ratio_profit_margin': 'حاشيه سود خالص'}
        ]
    },
    {
        "benchmark": [20, 40, 50, 60, 80],
        'target': [
            {'ratio_da': 'D/A'}
        ]
    },

    {
        'benchmark': [0.25, 0.5, 1, 2, 4,],
        'target': [
            {'ratio_de': 'D/E'}
        ]
    },

    {
        'benchmark': [0.1, 0, 5, 1, 1.25, 1.5, 1, 2],
        'target': [
            {'ratio_current_ratio': 'نسبت جاري'},
            {'ratio_quick_ratio': 'نسبت آني'}
        ]
    },

    {
        'benchmark': [0.1, 0, 25, 0.5, 0, 75, 0.9],
        'target': [
            {'ratio_cash_ratio': 'نسبت نقد'}
        ]
    },

    {
        'benchmark': [0.1, 0, 25, 0.5, 0, 75, 0.9],
        'target': [
            {'ratio_cash_ratio': 'نسبت نقد'}
        ]
    },

    {
         'benchmark': [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 20, 40, 80, 100],
         'target': [
             {'stockwatch_PricePerEarning': 'P/E'},
             {'stockwatch_PricePerEarningGroup': 'P/E گروه'},
         ]
    },
    {
         'benchmark': [-2000, -1000, 0, 200, 500, 1000, 2000],
         'target': [
             {'stockwatch_Eps': 'Eps'}
         ]
    },
    {
        'benchmark': [-4, -3, -2, -1, 0, 1, 2, 3, 4],
        'target': [
            {'stockwatch_ClosingPriceVariationPercent': 'درصد تغییر قیمت پایانی'},
            {'stockwatch_ReferencePriceVariationPercent': 'درصد تغییر آخرین معامله'},
        ]
    },
    {
        'benchmark': [25, 50, 75],
        'target': [
            {'stockwatch_BuyFirmVolumePercentage': 'درصد حجم خرید حقوقی'},
            {'stockwatch_BuyIndividualVolumePercentage': 'درصد حجم خرید حقیقی'},
            {'stockwatch_SellFirmVolumePercentage': 'درصد حجم فروش حقوقی'},
            {'stockwatch_SellIndividualVolumePercentage': 'درصد حجم فروش حقیقی'},
        ]
    },
    {
        'benchmark': [10, 100000, 500000, 1000000, 5000000],
        'target': [
            {'stockwatch_BaseQuantity': 'حجم مبنا'},
            // {'stockwatch_BuyIndividualVolumePercentage': 'درصد حجم خرید حقیقی'},
            // {'stockwatch_SellFirmVolumePercentage': 'درصد حجم فروش حقوقی'},
            // {'stockwatch_SellIndividualVolumePercentage': 'درصد حجم فروش حقیقی'},
        ]
    },
];
var filter_ids = [];
var choosen_filters = {};
$(document).ready(function () {
    insertfilters(filters_data);
    read_filters();
    $( "select" ).change(function(){
        read_filters();
    });
});

function insertfilters(filters) {
    var filters_div = document.getElementById('filters place'),
        column_num = 5, tr, counter = 0;
    filters.forEach(function (filter) {
        filter['target'].forEach(function (target) {
            if (counter == 0)  tr = document.createElement('tr');
            var name = Object.keys(target)[0];
            tr = insertFilterName(tr, target[name]);
            var select = document.createElement('select'),
                options = filter['benchmark'];
            select.addE
            tr = insertFilterOptions(tr, name, select, options);
            select.setAttribute('id', name);
            filter_ids.push(name);
            if (counter == 4) filters_div.appendChild(tr);
            counter = (counter + 1) % column_num;
        });
        filters_div.appendChild(tr);
    });
}

function insertFilterName(tr, name) {
    var td = document.createElement('td');
    td.innerHTML = name + ': ';
    tr.appendChild(td);
    return tr
}

function insertFilterOptions(tr, name, select, options) {
    var td = document.createElement('td'),
        operators = {'<': 'کمتر از ', '>': 'بیشتر از '};
    var option = document.createElement('option');
    option.innerHTML = 'همه';
    option.setAttribute('value', '');
    select.appendChild(option);
    Object.keys(operators).forEach(function (operator) {
        options.forEach(function (opt) {
            var option = document.createElement('option');
            option.innerHTML = operators[operator] + opt;
            option.setAttribute('value', name + operator + opt);
            select.appendChild(option);
        });
        td.appendChild(select);
        tr.appendChild(td);
    });
    return tr
}
function read_filters() {
    filter_ids.forEach(function (filter) {
        var select = document.getElementById(filter);
        if (!select.value == '') {
            console.log(filter);
            choosen_filters[filter] = select.value;
        } else {
            if (choosen_filters[filter]) {
                delete choosen_filters[filter];
            }
        }
    });
    var filters_list = [];
    Object.keys(choosen_filters).forEach(function (filter) {
        filters_list.push(choosen_filters[filter]);
    });
    filter_market(filters_list);
}

function filter_market(filters) {
    $.ajax({
        type: 'GET',
        url: "/filtermarket",
        data: {
            filters: JSON.stringify(filters),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        error: function () {
            // alert('متاسفانه هنگام دخیره کردن استراتژی شما مشکلی پیش آمده است,\n لطفا بعدا تلاش کنید.');
        },
        success: function (result) {
            result = JSON.parse(result);
            show_filters_result(result);
        }
    });
}
