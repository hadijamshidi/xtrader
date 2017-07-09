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
var eng_to_per = {
    'pc': 'قیمت پایانی',
    'po': 'قیمت آغازین',
    'ph': 'بیشترین قیمت',
    'eng_name': 'نام انگلیسی',
    'per_name': 'نام شرکت',
    'symbol_name': 'نام نماد',
    'vol': 'حجم معاملات',
};
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
