var info = {"SymbolId":"IRO7SASP0001","InstrumentName":"سجام","InstrumentTitle":"مجتمع سیمان غرب آسیا","InstrumentCode":"309","InstrumentStateCode":"A","InstrumentStateTitle":"مجاز","BaseQuantity":1.0,"BidAsk":[{"RowPlace":1,"AskNumber":1,"AskPrice":853.0,"AskQuantity":5800,"BidNumber":1,"BidPrice":879.0,"BidQuantity":1200},{"RowPlace":2,"AskNumber":2,"AskPrice":852.0,"AskQuantity":60000,"BidNumber":1,"BidPrice":880.0,"BidQuantity":5264},{"RowPlace":3,"AskNumber":1,"AskPrice":841.0,"AskQuantity":4000,"BidNumber":1,"BidPrice":931.0,"BidQuantity":144}],"BuyGroupCount":0,"BuyGroupVolume":0,"BuyGroupVolumePercentage":0.0,"BuyFirmCount":0,"BuyFirmVolume":0,"BuyFirmVolumePercentage":0.0,"BuyIndividualCount":10,"BuyIndividualVolume":57721,"BuyIndividualVolumePercentage":100.0,"SellFirmCount":0,"SellFirmVolume":0,"SellFirmVolumePercentage":0.0,"SellIndividualCount":7,"SellIndividualVolume":57721,"SellIndividualVolumePercentage":100.0,"ClosingPrice":854.0,"ClosingPriceVariation":-72.00,"ClosingPriceVariationPercent":-7.78,"CompanyName":"مجتمع سيمان غرب آسيا          ","ExchangeName":"پایه فرابورس","ExchangeCode":"366","FirstTradePrice":900.0,"LastTradePrice":853.0,"LastTradeDate":"2017-04-24T12:30:07","ReferencePrice":926.00,"ReferencePriceVariation":-73.00,"ReferencePriceVariationPercent":-7.88,"YearHighestTradePrice":1026.00,"YearLowestTradePrice":521.00,"MinimumOrderQuantity":1,"MaximumOrderQuantity":50000,"LowerPriceThreshold":834.00,"UpperPriceThreshold":1018.00,"LowestTradePrice":850.0,"HighestTradePrice":900.0,"PreviousDayPrice":926.00,"TotalNumberOfSharesTraded":57721,"TotalNumberOfTrades":15.0,"TotalTradeValue":49271653.0,"Eps":-2,"PricePerEarningGroup":0.0,"PricePerEarning":-427.0,"FreeFloatPercent":0.0,"MonthAverageVolume":410764,"InstrumentMarketValue":1317564010000.0,"NumberOfSharesOrBonds":1542815000};

function get_stock_info(){
	var persianlist = {
		"InstrumentTitle":'نام شرکت',
		"InstrumentName":"نماد",
		"InstrumentStateTitle":"وضعیت",
		'Eps':'EPS',
		'PricePerEarning':'P/E',
		'PricePerEarningGroup': 'P/E گروه',
		'InstrumentMarketValue': 'ارزش بازار',
		'TotalTradeValue':'ارزش معاملات',
		'ExchangeName':'بازار',
	}
	var place = document.getElementById('tsetmc');
    place.innerHTML = '';
    Object.keys(persianlist).forEach(function (detail_key) {
        var item = document.createElement('div');
        item.setAttribute('class', 'item');
        var content = document.createElement('div');
        content.setAttribute('class', 'content');
        var p = document.createElement('p');
        p.innerHTML = persianlist[detail_key]+' :';
        content.appendChild(p);

        var description = document.createElement('div');
        description.setAttribute('class', 'description');
        description.setAttribute('style', 'float: left;color: white');
        description.innerHTML = info[detail_key];

        content.appendChild(description);

        item.appendChild(content);
        place.appendChild(item);
    });

    var price_list = {
    	'LowerPriceThreshold': 'حداقل قیمت مجاز',
    	'UpperPriceThreshold':'حداکثر قیمت مجاز',
		'BuyFirmVolumePercentage':'درصد حجم خرید حقوقی',
		'BuyFirmVolume':'حجم خرید حقوقی',
		'BuyIndividualVolumePercentage':'درصد حجم خرید حقیقی',
		'BuyIndividualVolume':'حجم خرید حقیقی',

    };
	var place = document.getElementById('price');
    place.innerHTML = '';
    Object.keys(price_list).forEach(function (detail_key) {
        var item = document.createElement('div');
        item.setAttribute('class', 'item');
        var content = document.createElement('div');
        content.setAttribute('class', 'content');
        var p = document.createElement('p');
        p.innerHTML = price_list[detail_key]+' :';
        content.appendChild(p);

        var description = document.createElement('div');
        description.setAttribute('class', 'description');
        description.setAttribute('style', 'float: left;color: white');
        description.innerHTML = info[detail_key];

        content.appendChild(description);

        item.appendChild(content);
        place.appendChild(item);
    });

}
function filter_market(query){
    $.ajax({
        type: 'POST',
        url: "/filtse/",
        data: {
            'query': query,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        error: function(){
            alert('فیلترها اشتباه نگارشی دارند!\n لطفا مجددا اقدام کنید.');
        },
        success: function (result) {
            var result = JSON.parse(result);
            show_filters_result(result['result']);
            console.log(result['result']);
        }
    });

}
var eng_to_per = {
    'pc':'قیمت پایانی',
    'po':'قیمت آغازین',
    'ph':'بیشترین قیمت',
    'eng_name':'نام انگلیسی',
    'per_name':'نام شرکت',
    'symbol_name':'نام نماد',
    'vol':'حجم معاملات',
};
function show_filters_result(result){
    var columns = ['symbol_name','per_name','pc','po','ph','vol']; 
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
    columns.forEach(function(col){
        var th = document.createElement('TH');
        th.appendChild(document.createTextNode(eng_to_per[col]));
        tr.appendChild(th);
    });
    table.appendChild(tr);

    // creating tr for td tags:
    // var div = document.createElement('table');
    // div.setAttribute('style', 'height: 400px; overflow: auto');
    var div = table;
    result.forEach(function(stock){
    var tr = document.createElement('TR');
        columns.forEach(function(key){
            var td = document.createElement('TD');
            td.appendChild(document.createTextNode(quick_check(stock[key])));
            tr.appendChild(td);
        })
        div.appendChild(tr);
    })
    place.appendChild(div);
    place.appendChild(document.createElement('br'));
    place.style.display = 'block';
}
function quick_check(str){
    if (!isNaN(str)){
        return numberSeparator(str);
    }else{
        return str
    }
}