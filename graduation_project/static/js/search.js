$(".view-location").click(function () {
    var id = $(this).attr('value').split('|')
    var param;
    if (id[1] == 'None') {
        param = {locationId: id[0]};
    } else {
        param = {locationId: id[0], userId: id[1]};
    }

    $.get('/view_create/', param, function (data) {
        // $('#like-count').html(data);
    });
});
var current_url = window.location.href;
if (current_url.includes('distance')) {
    $("#distance").css('color', 'red');
}
if (current_url.includes('view')) {
    $("#view").css('color', 'red');
}
if (current_url.includes('evaluate')) {
    $("#evaluate").css('color', 'red');
}
if (current_url.includes('price')) {
    $("#price").css('color', 'red');
}


$(".bg-light").click(function () {
    var url = window.location.href;
    if (url.includes('sort')) {
        url = url.split('&sort')[0]
    }
    url = url + '&sort=' + $(this).attr('id');
    window.location.href = url;
});

function getQueryStringValue(key) {
    return decodeURIComponent(window.location.search.replace(new RegExp("^(?:.*[&\\?]" + encodeURIComponent(key).replace(/[\.\+\*]/g, "\\$&") + "(?:\\=([^&]*))?)?.*$", "i"), "$1"));
}