/**
 * Created by hadi on 7/25/17.
 */
var ids = {
    'pd1': "pd1", //خرید
    'LastTradePrice': "LastTradePrice", //معامله
    'po1': "po1", //فروش
    'FirstTradePrice': "FirstTradePrice",  //اولین
    'ClosingPrice': "ClosingPrice", //پایانی
    'PreviousDayPrice': "PreviousDayPrice", //دیروز
    'HighestTradePrice': "HighestTradePrice", //بازه روز اول
    'LowestTradePrice': "LowestTradePrice", // بازه روز دوم
    'UpperPriceThreshold': "UpperPriceThreshold", //قیمت مجاز اول
    'LowerPriceThreshold': "LowerPriceThreshold", //قیمت مجاز دوم
    'YearHighestTradePrice': "YearHighestTradePrice", //بازه سال اول
    'YearLowestTradePrice': "YearLowestTradePrice", // بازه سال دوم
    'TotalNumberOfTrades': "TotalNumberOfTrades", // تعداد  معاملات
    'TotalNumberOfSharesTraded': "TotalNumberOfSharesTraded", // حجم معاملات
    'TotalTradeValue': "TotalTradeValue", // ارزش معاملات
    'InstrumentMarketValue': "InstrumentMarketValue", // ارزش بازار
    'NumberOfSharesOrBonds': "NumberOfSharesOrBonds", // تعداد سهام
    'BaseQuantity': "BaseQuantity", // حجم مبنا
    'FreeFloatPercent': "FreeFloatPercent", // سهام شناور
    'MonthAverageVolume': "MonthAverageVolume", // میانگین حجم ماه
    'BuyIndividualVolumePercentage': "BuyIndividualVolumePercentage", // درصد خرید حقیقی
    'BuyIndividualVolume': "BuyIndividualVolume", // خرید حقیقی
    'SellIndividualVolumePercentage': "SellIndividualVolumePercentage", // درصد فروش حقیقی
    'SellIndividualVolume': "SellIndividualVolume", // فروش حقیقی
    'BuyFirmVolumePercentage': "BuyFirmVolumePercentage", // درصد خرید حقوقی
    'BuyFirmVolume': "BuyFirmVolume", // خرید حقوقی
    'SellFirmVolumePercentage': "SellFirmVolumePercentage", // درصد فروش حقوقی
    'SellFirmVolume': "SellFirmVolume", // فروش حقوقی
    'BuyIndividualCount': "BuyIndividualCount", // تعداد خرید حقیقی
    'SellIndividualCount': "SellIndividualCount", // تعداد فروش حقیقی
    'BuyFirmCount': "BuyFirmCount", // تعداد خرید حقوقی
    'SellFirmCount': "SellFirmCount", // تعداد فروش حقوقی
    'LastTradeDate': "LastTradeDate", // آخرین معامله
    'InstrumentStateTitle': "InstrumentStateTitle", // وضعیت
    'Eps': "Eps", //eps
    'PricePerEarning': "PricePerEarning", // p/e
    'PricePerEarningGroup': "PricePerEarningGroup", // p/e group
    'InstrumentName': "InstrumentName",
    'CompanyName': "CompanyName",

   /**************************************************************/
    'zd1': "zd1",
    'qd1': "qd1",
    'pd1': "pd1q",
    'po1': "po1q",
    'qo1': "qo1",
    'zo1': "zo1",
    'zd2': "zd2",
    'qd2': "qd2",
    'pd2': "pd2",
    'po2': "po2",
    'qo2': "qo2",
    'zo2': "zo2",
    'zd3': "zd3",
    'qd3': "qd3",
    'pd3': "pd3",
    'po3': "po3",
    'qo3': "qo3",
    'zo3': "zo3",
};

var price_data = {
    'zo1': 1,
//    'BuyFirmVolumePercentage': 0.0,
    'UpperPriceThreshold': 1247.0,
    'BuyIndividualVolumePercentage': 100.0,
    'pd2': 1161.0,
    'BuyGroupCount': 0,
    'BuyFirmVolume': 0,
    'BuyIndividualCount': 7,
    'qo2': 16400,
    'pd1': 1200.0,
    'TotalNumberOfSharesTraded': 105636,
    'ReferencePrice': 1188.0,
    'qd3': 1000,
    'InstrumentTitle': 'شرکت بیمه اتکایی امین',
    'qd1': 19,
    'InstrumentStateCode': 'A',
    'zd2': 1,
    'ClosingPriceVariationPercent': 1.35,
    'ClosingPriceVariation': 16.0,
    'SymbolId': 'IRO3TKMZ0001',
    'SellIndividualCount': 11,
    'LastTradePrice': 1201.0,
    'YearLowestTradePrice': 1111.0,
    'SellFirmVolume': 1000,
    'BuyGroupVolume': 0,
    'LowestTradePrice': 1192.0,
    'SellIndividualVolume': 104636,
    'BuyFirmCount': 0,
    'po2': 1214.0,
    'pd3': 1133.0,
    'zo3': 1,
    'FreeFloatPercent': 0.0,
    'FirstTradePrice': 1192.0,
    'MinimumOrderQuantity': 1,
    'qd2': 950,
    'po1': 1210.0,
    'ClosingPrice': 1204.0,
    'TotalNumberOfTrades': 22.0,
    'ExchangeCode': '364',
    'NumberOfSharesOrBonds': 2030000000,
    'Eps': 0,
    'MonthAverageVolume': 0,
    'HighestTradePrice': 1216.0,
    'TotalTradeValue': 127157571.0,
    'SellFirmCount': 1,
    'ExchangeName': 'فرابورس',
    'qo1': 14420,
    'MaximumOrderQuantity': 50000,
    'BuyGroupVolumePercentage': 0.0,
    'YearHighestTradePrice': 1724.0,
    'LowerPriceThreshold': 1129.0,
    'zd3': 1,
    'qo3': 3000,
    'po3': 1219.0,
    'InstrumentCode': '303',
    'PricePerEarningGroup': 7.99,
    'SellFirmVolumePercentage': 0.0,
    'ReferencePriceVariationPercent': 1.09,
    'BuyIndividualVolume': 105636,
    'PricePerEarning': 5.84236001968384,
    'CompanyName': 'شركت بيمه اتكايي امين',
    'SellIndividualVolumePercentage': 99.0,
    'LastTradeDate': '2017-07-23',
    'InstrumentMarketValue': 2444120000000.0,
    'ReferencePriceVariation': 13.0,
    'InstrumentStateTitle': 'مجاز',
    'InstrumentName': 'اتکام',
    'PreviousDayPrice': 1188.0,
    'zo2': 1,
    'zd1': 1,
    'BaseQuantity': 1.0
};
$(document).ready(function () {
    update_stockwatch();
    draw_chart();
});


function insert(data) {
    Object.keys(data).forEach(function (key) {
        if (ids[key]) {
            if (document.getElementById(ids[key])) {
                document.getElementById(ids[key]).innerHTML = data[key];
            }
        }
    });
}
var data;
function update_stockwatch(){
    $.ajax({
    type: 'GET',
    url: "/data/stockwatch/"+SymbolId,
    success: function (result) {
        result = JSON.parse(result);
        data = result;
        insert(result);
        },
    });

}

window.ODate = Date;
window.Date = JDate;


// $('input.prompt').attr('style', 'background-color: #333;color:white;text-align: center;font-family:IranSanc');
$('.ui.search').search({
    type: 'category',
    error: false,
    onSelect: function (result) {
            var value = result;
            symbol_id = value.symbol_id;
            window.location = '/stockwatch/' + symbol_id;
    },
    apiSettings: {
        onResponse: function (serverResponse) {
            var response = {
                results: {}
            };
            // translate GitHub API response to work with search
            $.each(serverResponse.items, function (index, item) {
                // console.log(item);
                var
                    category = item.category || 'Unknown',
                    maxResults = 8
                    ;
                if (index >= maxResults) {
                    return false;
                }
                // create new language category
                if (response.results[category] === undefined) {
                    response.results[category] = {
                        name: category,
                        results: []
                    };
                }
                // add result to category
                response.results[category].results.push({
                    title: item.symbol_name,
                    description: item.name,
                    price: item.kind,
                    eng_name: 'eng',
                    symbol_id: item.symbol_id,
                });
            });
            return response;
        },
        url: '/symbol-search/q={query}'
    }
});

$('.ui.search').dblclick(function () {
    $('.ui.search').transition('jiggle');
});


function draw_chart(){
//    $.getJSON('/get-data/'+SymbolId, function (data) {
    $.getJSON('https://www.highcharts.com/samples/data/jsonp.php?filename=aapl-c.json&callback=?', function (data) {
        var close = [];
        console.log(data);
    //    data = JSON.parse(data);
  //      name = data['per_name'];
//        data = JSON.parse(data['items']);
        var dataLength = data.length;
        for (var i = 0; i < dataLength; i++) {
            close.push([
                data[i][0], // date
                Math.ceil(data[i][4]), // close
            ]);
        }
        Highcharts.stockChart('chart', {
            rangeSelector: {
                enabled: false,
                inputEnabled: false,
                // selected: 1
            },
            credits:{
                enabled: false,
            },
            yAxis: [{
                gridLineWidth: 0,
                minorGridLineWidth: 0,
                opposite: false,
             }],
             scrollbar: {
                enabled: false
            },
            navigator: {
                enabled: false
            },
            series: [{
                color: {
                    linearGradient: { x1: 0, x2: 0, y1: 0, y2: 1 },
                    stops: [
                        [0, '#f3f774'],
                        [0.25, '#aae98e'],
                        [0.50, '#09cac8'],
                        [0.75, '#aae98e'],
                        [1, '#f3f774']
                    ]
                },
                name: name,
//                data: close,
                data: data
            }]
        });
    });

    Highcharts.setOptions({
        lang: {
            months: ['فروردين', 'ارديبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'],
            shortMonths: ['فروردين', 'ارديبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'],
            weekdays: ["یکشنبه", "دوشنبه", "سه شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه"]
        }
    });

    Highcharts.createElement('link', {
        href: 'https://fonts.googleapis.com/css?family=Unica+One',
        rel: 'stylesheet',
        type: 'text/css'
    }, null, document.getElementsByTagName('head')[0]);
    Highcharts.theme = {
        colors: ['#2b908f', '#90ee7e', '#f45b5b', '#7798BF', '#aaeeee', '#ff0066', '#eeaaee',
            '#55BF3B', '#DF5353', '#7798BF', '#aaeeee'],
        chart: {
            backgroundColor: {
            color :'#fff',
                /*linearGradient: {x1: 0, y1: 0, x2: 1, y2: 1},
                stops: [
                    [0, '#2a2a2b'],
                    [1, '#3e3e40']
                ]
            },
            style: {
                fontFamily: 'IRANSans'
            },
            plotBorderColor: '#606063',

            // zooming:
            // zoomType: 'x',
            // panning: true,
            // panKey: 'shift'
        },
        title: {
            style: {
                color: '#E0E0E3',
                // textTransform: 'uppercase',
                fontSize: '20px'
            }
        },
        subtitle: {
            style: {
                color: '#E0E0E3',
                // textTransform: 'uppercase'
            }
        },
        xAxis: {
            gridLineColor: '#707073',
            labels: {
                style: {
                    color: '#E0E0E3'
                }
            },
            lineColor: '#707073',
            minorGridLineColor: '#505053',
            tickColor: '#707073',
            title: {
                style: {
                    color: '#A0A0A3'

                }
            }
        },
        yAxis: {
            gridLineColor: '#707073',
            labels: {
                style: {
                    color: '#E0E0E3'
                }
            },
            lineColor: '#707073',
            minorGridLineColor: '#505053',
            tickColor: '#707073',
            tickWidth: 1,
            title: {
                style: {
                    color: '#A0A0A3'
                }
            }
        },
        tooltip: {

            // xDateFormat: '%Y-%m-%d',
            shared: true,
            useHTML: true,
            // headerFormat: '<small>{point.key}</small><br><table>',
            // pointFormat: '<tr><td style="color: {series.color}">{series.name}: </td>' +
            // '<td style="text-align: right"> <b>{point.y} </b></td></tr>',

            headerFormat: '',
            pointFormat: '<td style="text-align: right"> <b>{point.y}</b></td></tr>',
            footerFormat: '</table>',
            valueDecimals: 0,

            backgroundColor: 'rgba(0, 0, 0, 0.85)',
            style: {
                color: '#F0F0F0'
            }
        },
        plotOptions: {
            series: {
                animation: false,

                dataLabels: {
                    color: '#B0B0B3'
                },
                marker: {
                    lineColor: '#333'
                }
            },
            boxplot: {
                fillColor: '#505053'
            },
            candlestick: {
                lineColor: 'white'
            },
            errorbar: {
                color: 'white'
            }
        },
        legend: {
            itemStyle: {
                color: '#E0E0E3'
            },
            itemHoverStyle: {
                color: '#FFF'
            },
            itemHiddenStyle: {
                color: '#606063'
            }
        },
        credits: {
            style: {
                color: '#FFF'
                // '#666'
            },
            text: 'Xtrader.ir',
            href: 'http://www.xtrader.ir'
        },
        labels: {
            style: {
                color: '#707073'
            }
        },

        drilldown: {
            activeAxisLabelStyle: {
                color: '#F0F0F3'
            },
            activeDataLabelStyle: {
                color: '#F0F0F3'
            }
        },

        navigation: {
            buttonOptions: {
                symbolStroke: '#DDDDDD',
                theme: {
                    fill: '#505053'
                }
            }
        },

        // scroll charts
        rangeSelector: {
            buttonTheme: {
                fill: '#505053',
                stroke: '#000000',
                style: {
                    color: '#CCC'
                },
                states: {
                    hover: {
                        fill: '#707073',
                        stroke: '#000000',
                        style: {
                            color: 'white'
                        }
                    },
                    select: {
                        fill: '#000003',
                        stroke: '#000000',
                        style: {
                            color: 'white'
                        }
                    }
                }
            },
            inputBoxBorderColor: '#505053',
            inputStyle: {
                backgroundColor: '#333',
                color: 'silver'
            },
            labelStyle: {
                color: 'silver'
            }
        },

        navigator: {
            handles: {
                backgroundColor: '#666',
                borderColor: '#AAA'
            },
            outlineColor: '#CCC',
            maskFill: 'rgba(255,255,255,0.1)',
            series: {
                color: '#7798BF',
                lineColor: '#A6C7ED'
            },
            xAxis: {
                gridLineColor: '#505053'
            }
        },

        scrollbar: {
            barBackgroundColor: '#808083',
            barBorderColor: '#808083',
            buttonArrowColor: '#CCC',
            buttonBackgroundColor: '#606063',
            buttonBorderColor: '#606063',
            rifleColor: '#FFF',
            trackBackgroundColor: '#404043',
            trackBorderColor: '#404043'
        },

        // special colors for some of the
        legendBackgroundColor: 'rgba(0, 0, 0, 0.5)',
        background2: '#505053',
        dataLabelsColor: '#B0B0B3',
        textColor: '#C0C0C0',
        contrastTextColor: '#F0F0F3',
        maskColor: 'rgba(255,255,255,0.3)'
    };
    Highcharts.setOptions(Highcharts.theme);

}
