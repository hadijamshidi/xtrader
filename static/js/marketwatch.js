/**
 * Created by hadi on 7/5/17.
 */
function filter_market(query) {
    query = document.getElementById('filters_script').value;
    $.ajax({
        type: 'GET',
        url: "/finance/market_watch",
        data: {
            'query': query,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        error: function () {
            alert('فیلترها اشتباه نگارشی دارند!\n لطفا مجددا اقدام کنید.');
        },
        success: function (result) {
            // console.log(result);
            var result = JSON.parse(result);
            show_filters_result(result);
            // console.log(result);
        }
    });
}
function show_filters_result(result) {
    var columns = [
        'InstrumentName', 'InstrumentTitle', 'TotalNumberOfTrades',
        'TotalNumberOfSharesTraded',
        'TotalTradeValue', 'PreviousDayPrice', 'FirstTradePrice',
        'LastTradePrice', 'ClosingPrice',
        'LowestTradePrice', 'HighestTradePrice', 'Eps', 'PricePerEarning'
    ];
    var place = document.getElementById("filters scan place");
    place.innerHTML = '';

    // new code
    // creating table tag and attrs:
    var table = document.createElement("TABLE");
    table.setAttribute("id", "table");
    table.setAttribute("style", "text-align:right");
    table.setAttribute("class", "ui selectable inverted celled  table");
    place.appendChild(table);

    //creating tr for th tags:
    var tr = document.createElement('TR');
    columns.forEach(function (col) {
        var th = document.createElement('TH');
        th.appendChild(document.createTextNode(result['keys'][col]));
        tr.appendChild(th);
    });
    table.appendChild(tr);

    // creating tr for td tags:
    // var div = document.createElement('table');
    // div.setAttribute('style', 'height: 400px; overflow: auto');
    var div = table;
    console.log(result);
    result['result'].forEach(function (stock) {
        var tr = document.createElement('TR');
        columns.forEach(function (key) {
            var td = document.createElement('TD');
            td.appendChild(document.createTextNode(quick_check(stock[key])));
            tr.appendChild(td);
        });
        div.appendChild(tr);
    });
    place.appendChild(div);
    place.appendChild(document.createElement('br'));
    place.style.display = 'block';
}
function quick_check(str) {
    // if (!isNaN(str)) {
    //     return numberSeparator(str);
    // } else {
    //     return str
    // }
    return str
}

var filters_data = {
    'PE': {'همه':'', 'کمتر از 5': 'PE__lt=5', 'بیشتر از 5': 'PE__gt=5'},
    'EPS': {'همه':'', 'کمتر از 5': 'PE__lt=5', 'بیشتر از 5': 'PE__gt=5'},
    'ROE': {'همه':'', 'کمتر از 5': 'PE__lt=5', 'بیشتر از 5': 'PE__gt=5'},
    'ROA': {'همه':'', 'کمتر از 5': 'PE__lt=5', 'بیشتر از 5': 'PE__gt=5'},
    'DPS': {'همه':'', 'کمتر از 5': 'PE__lt=5', 'بیشتر از 5': 'PE__gt=5'},
    'PE1': {'همه':'', 'کمتر از 5': 'PE__lt=5', 'بیشتر از 5': 'PE__gt=5'},
    'EPS1': {'همه':'', 'کمتر از 5': 'PE__lt=5', 'بیشتر از 5': 'PE__gt=5'},
    'ROE1': {'همه':'', 'کمتر از 5': 'PE__lt=5', 'بیشتر از 5': 'PE__gt=5'},
    'ROA1': {'همه':'', 'کمتر از 5': 'PE__lt=5', 'بیشتر از 5': 'PE__gt=5'},
    'DPS1': {'همه':'', 'کمتر از 5': 'PE__lt=5', 'بیشتر از 5': 'PE__gt=5'},
    'ROA2': {'همه':'', 'کمتر از 5': 'PE__lt=5', 'بیشتر از 5': 'PE__gt=5'},
    'DPS2': {'همه':'', 'کمتر از 5': 'PE__lt=5', 'بیشتر از 5': 'PE__gt=5'},
};
insertfilters(filters_data);

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
        operators = {'<': 'کوچکتر از ', '>': 'بزرگتر از '};
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
    Object.keys(choosen_filters).forEach(function(filter){
        filters_list.push(choosen_filters[filter]);
    });
    console.log(filters_list);
    filter_market(filters_list);
}

function filter_market(filters) {
    $.ajax({
        type: 'GET',
        url: "/finance/filtermarket",
        data: {
            filters: JSON.stringify(filters),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        error: function () {
            // alert('متاسفانه هنگام دخیره کردن استراتژی شما مشکلی پیش آمده است,\n لطفا بعدا تلاش کنید.');
        },
        success: function (result) {
            console.log(result);
        }
    });
}
