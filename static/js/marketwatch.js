/**
 * Created by hadi on 7/5/17.
 */
    var columns = {
        // 'num': 'ردیف',
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
//        'ratio_roa': 'roa',
//        'ratio_roe': 'roe',
    };
function show_filters_result(result) {
    var columns = {
        // 'num': 'ردیف',
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
//        'ratio_roa': 'roa',
//        'ratio_roe': 'roe',
    };
    var place = document.getElementById("filters_scan_place");
    place.innerHTML = '';
    // creating table tag and attrs:
    var table = document.createElement("div");
    table.setAttribute("id", "table");
    // table.setAttribute("style", "text-align:right");
    // table.setAttribute("class", "ui selectable inverted celled  table");
    place.appendChild(table);

    //creating tr for th tags:
    var tr = document.createElement('div');
        tr.setAttribute('class', 'divTableRow main-nav');
    Object.keys(columns).forEach(function (column) {
        var th = document.createElement('div');
        th.setAttribute('class', 'divTableCell');
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
        tr.setAttribute('class', 'divTableRow');
        if (num2 % 2 == 1) tr.setAttribute('style', 'background:#4d5068');
        num2 += 1;
        var num = 0;
        Object.keys(columns).forEach(function (column) {
            var td = document.createElement('div');
            td.setAttribute('class', 'divTableCell');
            if (num == 0) {
                var a = document.createElement('a');
                a.appendChild(document.createTextNode(quick_check(stock[column])));
                a.setAttribute('href', '/stockwatch/' + stock['stockwatch_SymbolId']);
                td.appendChild(a);
                tr.appendChild(td);

            } else {
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
    /****************************************************1*************************************************************/
        'benchmark': [25, 50, 75],
        'target': [

            {'stockWatch__BuyIndividualVolumePercentage': 'درصد حجم خرید حقیقی'}

        ]
    },
    /****************************************************2*************************************************************/
    {
        'benchmark': [0.1, 0, 25, 0.5, 0, 75, 0.9],
        'target': [
            {'ratio__cash_ratio': 'نسبت نقد'}
        ]
    },
    /****************************************************3*************************************************************/
    {
        "benchmark": [0, 18, 25, 50, 75, 100, 200, 300],
        "target": [
            {'ratio__roe': 'ROE'}
        ]
    },
    /****************************************************4*************************************************************/
    {
        "benchmark": [20, 40, 50, 60, 80],
        'target': [
            {'ratio__da': 'D/A'}
        ]
    },

    /****************************************************5*************************************************************/
                {
        'benchmark': [25, 50, 75],
        'target': [

            {'stockWatch__SellIndividualVolumePercentage': 'درصد حجم فروش حقیقی'}
        ]
    },
    /****************************************************6*************************************************************/
     {
        'benchmark': [0.1, 0, 5, 1, 1.25, 1.5, 1, 2],
        'target': [
            {'ratio__quick_ratio': 'نسبت آني'}
        ]
    },

    /****************************************************7*************************************************************/
        {
        "benchmark": [0, 18, 25, 50, 75, 100, 200, 300],
        "target": [
            {'ratio__roa': 'ROA'}
        ]
    },

    /****************************************************8*************************************************************/

         {
        'benchmark': [0.25, 0.5, 1, 2, 4,],
        'target': [
            {'ratio__de': 'D/E'}
        ]
    },
    /****************************************************9*************************************************************/
    {
        'benchmark': [25, 50, 75],
        'target': [
            {'stockWatch__BuyFirmVolumePercentage': 'درصد حجم خرید حقوقی'}
        ]
    },
    /****************************************************10*************************************************************/
    {
        'benchmark': [0.1, 0, 5, 1, 1.25, 1.5, 1, 2],
        'target': [
            {'ratio__current_ratio': 'نسبت جاري'}
        ]
    },
    /****************************************************11*************************************************************/
        {
        "benchmark": [0, 18, 25, 50, 75, 100, 200, 300],
        "target": [
            {'ratio__profit_margin': 'حاشيه سود خالص'}
        ]
    },
    /****************************************************12*************************************************************/
    {
        'benchmark': [-2000, -1000, 0, 200, 500, 1000, 2000],
        'target': [
            {'stockWatch__Eps': 'EPS'}
        ]
    },

    /****************************************************13*************************************************************/
    {
        'benchmark': [25, 50, 75],
        'target': [
            {'stockWatch__SellFirmVolumePercentage': 'درصد حجم فروش حقوقی'}
        ]
    },
    /****************************************************14*************************************************************/
    {
        'benchmark': [1000000,5000000,10000000],
        'target': [
            {'stockWatch__TotalNumberOfSharesTraded': 'حجم معاملات'}
        ]
    },
    /****************************************************15*************************************************************/
    {
        "benchmark": [0, 18, 25, 50, 75, 100, 200, 300],
        "target": [
            {'ratio__gross_profit_margin': 'حاشيه سود ناخالص'}
        ]
    },
    /****************************************************16*************************************************************/
    {
        'benchmark': [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 20, 40, 80, 100],
        'target': [
            {'stockWatch__PricePerEarning': 'P/E'}
        ]
    },

    /****************************************************17*************************************************************/
    {
        'benchmark': [-4, -3, -2, -1, 0, 1, 2, 3, 4],
        'target': [
            {'stockWatch__ClosingPriceVariationPercent': 'درصد تغییر قیمت پایانی'}
        ]
    },

    /****************************************************18*************************************************************/

        {
        'benchmark': [10, 100000, 500000, 1000000, 5000000],
        'target': [
            {'stockWatch__BaseQuantity': 'حجم مبنا'},
        ]
    },
    /****************************************************19*************************************************************/
        {
        'benchmark': [-4, -3, -2, -1, 0, 1, 2, 3, 4],
        'target': [
            {'stockWatch__ReferencePriceVariationPercent': 'درصد تغییر آخرین معامله'}
        ]
    },
    /****************************************************20*************************************************************/
         {
        'benchmark': [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 20, 40, 80, 100],
        'target': [
            {'stockWatch__PricePerEarningGroup': 'P/E گروه'}
        ]
    },

];
var filter_ids = [];
var choosen_filters = {};
$(document).ready(function () {
    insertfilters(filters_data);
    read_filters();
    $("select").change(function () {
        read_filters();
    });
});

function insertfilters(filters) {
    var filters_div = document.getElementById('filters-place'),
        column_num = 4, tr, counter = 0;
    filters.forEach(function (filter) {
        filter['target'].forEach(function (target) {
            if (counter == 0)  tr = document.createElement('tr');
            var name = Object.keys(target)[0];
            tr = insertFilterName(tr, target[name]);
            var select = document.createElement('select'),
                options = filter['benchmark'];
            select.setAttribute('class','selectpicker');
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
    td.setAttribute('class','filter-name');
    td.innerHTML = name;
    tr.appendChild(td);
    return tr
}

function insertFilterOptions(tr, name, select, options) {
    var td = document.createElement('td'),
        operators = {'__lt': 'کمتر از ', '__gt': 'بیشتر از '};
    var option = document.createElement('option');
    option.innerHTML = 'همه';
    option.setAttribute('value', '');
    select.appendChild(option);
    Object.keys(operators).forEach(function (operator) {
        options.forEach(function (opt) {
            var option = document.createElement('option');
            option.innerHTML = operators[operator] + quick_check(opt);
            var d = {};
            d[name+operator] = opt;
            option.setAttribute('value', JSON.stringify(d));
            select.appendChild(option);
        });
        td.appendChild(select);
        tr.appendChild(td);
    });
    return tr
}
function read_filters(page) {
    filter_ids.forEach(function (filter) {
        var select = document.getElementById(filter);
        if (!select.value == '') {
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
    filter_market(filters_list, page);
}

function filter_market(filters, page) {
    waiting('wait');
    $.ajax({
        type: 'GET',
        url: "/filtermarket?page="+page,
        data: {
            filters: JSON.stringify(filters),
            sort_by: JSON.stringify(sort_by),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        error: function () {
            // alert('متاسفانه هنگام دخیره کردن استراتژی شما مشکلی پیش آمده است,\n لطفا بعدا تلاش کنید.');
            waiting('default');
        },
        success: function (result) {
            $('#filters_scan_place').html(result);
            waiting('default');
        }
    });
}

///////////////////////////////////////////////////////////////////////////////////////////////
var  mn = $(".main-nav");
    mns = "main-nav-scrolled";
    hdr = $('header').height();

$(window).scroll(function() {
  if( $(this).scrollTop() > hdr ) {
    mn.addClass(mns);
  } else {
    mn.removeClass(mns);
  }
});

function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("table");
  switching = true;
  //Set the sorting direction to ascending:
  dir = "asc";
  /*Make a loop that will continue until
  no switching has been done:*/
  while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.getElementsByClassName('divTableRow');
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < (rows.length - 1); i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      /*Get the two elements you want to compare,
      one from current row and one from the next:*/
      x = rows[i].getElementsByTagName("DIV")[n];
      y = rows[i + 1].getElementsByTagName("DIV")[n];
      /*check if the two rows should switch place,
      based on the direction, asc or desc:*/
      // console.log(Number(x.innerHTML.toLowerCase()) + 22);
      if (dir == "asc") {
        if (Number(x.innerHTML.toLowerCase()) > Number(y.innerHTML.toLowerCase())) {
          //if so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }
      } else if (dir == "desc") {
        if (Number(x.innerHTML.toLowerCase()) < Number(y.innerHTML.toLowerCase())) {
          //if so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /*If a switch has been marked, make the switch
      and mark that a switch has been done:*/
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      //Each time a switch is done, increase this count by 1:
      switchcount ++; 
    } else {
      /*If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again.*/
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
  recoloring(dir, n);
}
var sort_by;
function recoloring(dir, n){
    var table = document.getElementById("table"),
        sort_dict = {'asc':'','desc':'-'},
        rows = table.getElementsByClassName('divTableRow');
    for (i = 1; i < rows.length; i++) {
        if(i%2==1){
            rows[i].style.background = '#4d5068';
        }else{
            rows[i].style.background = '#1c1f32';
        }
    }
    sort_by = sort_dict[dir]+Object.keys(columns)[n];
}
function reset_filters(){
    filters_data.forEach(function (filter) {
        filter['target'].forEach(function(target){
            Object.keys(target).forEach(function (filter_id) {
                document.getElementById(filter_id).value = '';
            });
        });
    });
    read_filters();
}