var ready = $(document).ready(function () {

    $(".form-control").keydown(function (e) {
        if (e.keyCode == 13) {
            return false;
        }
    });


    $(".page-link").click(function () {
        pageURL = window.location.href;
        if ($(this).attr("value")) {
            if (pageURL.includes("&page")) {

                pageURL = pageURL.split("&page")[0];
            }
            pageURL += '&page=' + $(this).attr("value");
            window.location.replace(pageURL);
        }
    });


    function saveSearchForm() {
        let pageURL = window.location.href;
        let word = getQueryStringValue("word").replace('?','');
        let loc = getQueryStringValue("loc");
        let cat = getQueryStringValue("cat");
        let cui = getQueryStringValue("cui");
        let pageLink = getQueryStringValue("page");
        $("#word").val(word).change();
        $("#select-loc").val(loc).change();
        $("#select-cat").val(cat).change();
        $("#select-cui").val(cui).change();

        $("#page-link").find(`[value='${pageLink}']`).removeClass('page_link').addClass('page_link active');

    }

    saveSearchForm();
    var input1 = document.getElementById("word-search");
    input1.addEventListener("keyup", function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            submitSearch();
        }
    });
    var input2 = document.getElementById("cat-search");
    input2.addEventListener("keyup", function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            submitSearch();
        }
    });
    var input3 = document.getElementById("loc-search");
    input3.addEventListener("keyup", function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            submitSearch();
        }
    });
    var input4 = document.getElementById("cui-search");
    input4.addEventListener("keyup", function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            submitSearch();
        }
    });

    function submitSearch() {
        let pageURL = window.location.href;
        pageURL = pageURL.split('/')[0]

        if (pageURL.includes("search")) {
            pageURL = pageURL.split("search/?")[0];
        }
        pageURL += '/search/?';
        let word = $("#word").val();
        let loc = $("#select-loc").val();
        let cat = $("#select-cat").val();
        let cui = $("#select-cui").val();
        if (word) {
            pageURL += '&word=' + word;
        }
        if (loc) {
            pageURL += '&loc=' + loc;
        }
        if (cat) {
            pageURL += '&cat=' + cat;
        }
        if (cui) {
            pageURL += '&cui=' + cui;
        }
        window.location.href=pageURL;
        // document.getElementById("word").innerHTML = word;
        // document.getElementById("select-loc").innerHTML = loc;
        // document.getElementById("select-cat").innerHTML = cat;
        // document.getElementById("select-cui").innerHTML = cui;
    }


    function getQueryStringValue(key) {
        return decodeURIComponent(window.location.search.replace(new RegExp("^(?:.*[&\\?]" + encodeURIComponent(key).replace(/[\.\+\*]/g, "\\$&") + "(?:\\=([^&]*))?)?.*$", "i"), "$1"));
    }
});


