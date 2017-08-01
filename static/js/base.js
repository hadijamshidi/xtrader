function quick_check(str) {
    if (!isNaN(str)) {
        var sign = '';
        if (Number(str)<0) {
            str = -1*Number(str);
            sign = '-';
        }
        str = String(str);
        var str1 = '',
            str2 = '',
            l = str.length;
        for (var i = 0; i < l; i++) {
            if(str.substring(i,i+1) == '.'){
                str2 = str.substring(i+1,l);
                str2 = '.' + str2;
                break
            }else{
                str1 += str.substring(i, i+1);
            }
        }
        var l = str.length;
        if(l>6 & l<=9){
            return str.substring(0,l-6)+'.'+str.substring(l-6,l-5)+' M'
        }
        if(l>9){
            return quick_check(str.substring(0,l-9)) +'.'+str.substring(l-9,l-8)+' B'
        }
        return sign + numberSeparator(str1) + str2;
    } else {
        return str
    }
}
function numberSeparator(n) {
    n = String(n);
    var m = [],
        ll = n.length;
    for (var i = 0; i < ll; i++) {
        m.push(n.substring(i, i + 1));
    }
    m.reverse();
    var i = 0,
        n = '';
    m.forEach(function (digit) {
        i++;
        n = digit + n;
        if (i % 3 == 0 & i != ll) {
            n = ',' + n;
        }
    });
    return n
}
