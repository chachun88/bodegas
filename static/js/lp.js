Number.prototype.formatMoney = function(c, d, t)
{
    var n = this, 
    c = isNaN(c = Math.abs(c)) ? 2 : c, 
    d = d === undefined ? "," : d, 
    t = t === undefined ? "." : t, 
    s = n < 0 ? "-" : "", 
    i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", 
    j = (j = i.length) > 3 ? j % 3 : 0;
    return "$" + s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
};

Number.prototype.truncate = function(n)
{
    var nn = Math.pow( 10, n );

    return (parseInt(this * nn) / nn);
};


String.prototype.unformatMoney = function()
{
    var n = this;
    return parseFloat( n.split("$").join("").split(".").join("").split(",").join("").split(" ").join("")  );
};

Object.size = function(obj) 
{
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

$.lp = function()
{};

$.lp.validateInt = function( n, def )
{
    if (def === undefined)
        def = 0;
    return parseInt( isNaN( parseInt( n ) ) ? def : n );
};

$.lp.validateFloat = function( n, def )
{
    if (def === undefined)
        def = 0.0;
    return parseFloat( isNaN( parseFloat( n ) ) ? def : n );
};

$.lp.getUrlParameter = function(sParam, default_value)
{
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) 
    {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) 
        {
            return sParameterName[1];
        }
    }

    if (default_value != undefined)
        return default_value;

    return false;
};