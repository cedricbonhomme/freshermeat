var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

function updateQueryStringParameter(uri, key, value) {
    var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
    var separator = uri.indexOf('?') !== -1 ? "&" : "?";
    if (uri.match(re)) {
        return uri.replace(re, '$1' + key + "=" + value + '$2');
    }
    else {
        return uri + separator + key + "=" + value;
    }
}

// random pastel colors
function pastelColorMaker() {
    var hue = Math.floor(Math.random() * 360);
    return 'hsl(' + hue + ', 100%, 87.5%)';
}
// some static pastel colors
var colors = ['rgba(230, 25, 75, 0.2)', 'rgba(60, 180, 75, 0.2)',
    'rgba(255, 225, 25, 0.2)', 'rgba(0, 130, 200, 0.2)', 'rgba(245, 130, 48, 0.2)',
    'rgba(145, 30, 180, 0.2)', 'rgba(70, 240, 240, 0.2)', 'rgba(240, 50, 230, 0.2)',
    'rgba(210, 245, 60, 0.2)', 'rgba(250, 190, 190, 0.2)', 'rgba(0, 128, 128, 0.2)',
    'rgba(230, 190, 255, 0.2)', 'rgba(170, 110, 40, 0.2)', 'rgba(255, 250, 200, 0.2)',
    'rgba(128, 0, 0, 0.2)', 'rgba(170, 255, 195, 0.2)', 'rgba(128, 128, 0, 0.2)',
    'rgba(255, 215, 180, 0.2)', 'rgba(0, 0, 128, 0.2)', 'rgba(128, 128, 128, 0.2)',
    'rgba(255, 255, 255, 0.2)','rgba(0, 0, 0, 0.2)'];
