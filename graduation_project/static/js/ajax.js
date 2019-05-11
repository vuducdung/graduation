var ready = $(document).ready(function () {

    function view_notification(id) {

    }

    $(".form-control").keydown(function (e) {
        if (e.keyCode == 13) {
            return false;
        }
    });

    $(".page-link").click(function () {
        let pageURL = window.location.href;
        if (!pageURL.includes("/?")) {
            pageURL += "?"
        }
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
        let word = getQueryStringValue("word").replace('?', '');
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
    let input1 = document.getElementById("word-search");
    input1.addEventListener("keyup", function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            submitSearch();
        }
    });
    let input2 = document.getElementById("cat-search");
    input2.addEventListener("keyup", function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            submitSearch();
        }
    });
    let input3 = document.getElementById("loc-search");
    input3.addEventListener("keyup", function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            submitSearch();
        }
    });

    $("#but-sub").click(function () {
        submitSearch();
    });

    let input4 = document.getElementById("cui-search");
    input4.addEventListener("keyup", function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            submitSearch();
        }
    });

    function submitSearch() {
        collection_name = $(".choice-location").text()

        let pageURL = window.location.href;
        pageURL = pageURL.split('/')[0]

        if (pageURL.includes("search")) {
            pageURL = pageURL.split("search/?")[0];
        }
        pageURL += '/search/?';
        let word = $("#word").val();
        if (collection_name != '') {
            word = collection_name.trim()
            alert(word)
        }
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
        window.location.href = pageURL;
    }


    function getQueryStringValue(key) {
        return decodeURIComponent(window.location.search.replace(new RegExp("^(?:.*[&\\?]" + encodeURIComponent(key).replace(/[\.\+\*]/g, "\\$&") + "(?:\\=([^&]*))?)?.*$", "i"), "$1"));
    }
});


