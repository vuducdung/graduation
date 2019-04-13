const go = document.getElementById("but-sub");
go.addEventListener("click", submitSearch);

function submitSearch() {
    let pageURL = window.location.href;
    pageURL = pageURL.split('/')[0]

    if (pageURL.includes("search")) {

        pageURL = pageURL.split("search/")[0];
        // alert(pageURL)
    }
    pageURL += '/search/?';
    let word = $("#word").val();
    let loc = $("#select-loc").val();
    let cat = $("#select-cat").val();
    let cui = $("#select-cui").val();
    if (word) {
        pageURL += 'word=' + word;
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
    window.location.replace(pageURL);
    // document.getElementById("word").innerHTML = word;
    // document.getElementById("select-loc").innerHTML = loc;
    // document.getElementById("select-cat").innerHTML = cat;
    // document.getElementById("select-cui").innerHTML = cui;
}


function getQueryStringValue(key) {
    return decodeURIComponent(window.location.search.replace(new RegExp("^(?:.*[&\\?]" + encodeURIComponent(key).replace(/[\.\+\*]/g, "\\$&") + "(?:\\=([^&]*))?)?.*$", "i"), "$1"));
}