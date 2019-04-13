var ready = $(document).ready(function () {

    // let pageURL = window.location.href;
    // let word = getQueryStringValue("word")
    // alert(word)
    $(".form-control").keydown(function (e) {
        if (e.keyCode == 13) {
            return false;
        }
    });

    $("#update-button").click(function(){
        $("#show-button-update").show();
    });

    // go.addEventListener("click", submitSearch);

    $(".page-link").click(function () {
        pageURL = window.location.href;
        if ($(this).attr("value")) {
            if (pageURL.includes("?")) {

                pageURL = pageURL.split("?")[0];
                // alert(pageURL)
            }
            pageURL += '?page=' + $(this).attr("value");
            window.location.replace(pageURL);
            // alert(pageURL)
        }
    });

    $("#user-name").keydown(function (e) {
        pageURL = window.location.href;
        if (e.keyCode == 13) {
            if ($("#user-name").val()) {
                if (pageURL.includes("?")) {

                    pageURL = pageURL.split("?")[0];
                    // alert(pageURL)
                }
                pageURL += '?username=' + $("#user-name").val();
                window.location.replace(pageURL);
            }
            // alert($("#user-name").val())
        }
    });


    function saveSearchForm() {
        let pageURL = window.location.href;
        let word = getQueryStringValue("word");
        let loc = getQueryStringValue("loc");
        let cat = getQueryStringValue("cat");
        let cui = getQueryStringValue("cui");
        let page_link = getQueryStringValue("page");
        $("#word").val(word).change();
        $("#select-loc").val(loc).change();
        $("#select-cat").val(cat).change();
        $("#select-cui").val(cui).change();
        $("#page-link[value=${page_link}]").toggleClass('page-link active');
        ;
        // // alert(word+loc+ cat+ cui);

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

    const go = document.getElementById("but-sub");
    go.addEventListener("click", submitSearch);

    function submitSearch() {
        let pageURL = window.location.href;

        if (pageURL.includes("search")) {

            pageURL = pageURL.split("search/")[0];
            // alert(pageURL)
        }
        pageURL += 'search/?';
        let word = $("#word").val();
        let loc = $("#select-loc").val();
        let cat = $("#select-cat").val();
        let cui = $("#select-cui").val();
        if (word) {
            pageURL += 'word=' + word + '&';
        }
        if (loc) {
            pageURL += 'loc=' + loc + '&';
        }
        if (cat) {
            pageURL += 'cat=' + cat + '&';
        }
        if (cui) {
            pageURL += 'cui=' + cui;
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

    function sortTable(n) {
        var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
        table = document.getElementById("myTable");
        switching = true;
        //Set the sorting direction to ascending:
        dir = "asc";
        /*Make a loop that will continue until
        no switching has been done:*/
        while (switching) {
            //start by saying: no switching is done:
            switching = false;
            rows = table.rows;
            /*Loop through all table rows (except the
            first, which contains table headers):*/
            for (i = 1; i < (rows.length - 1); i++) {
                //start by saying there should be no switching:
                shouldSwitch = false;
                /*Get the two elements you want to compare,
                one from current row and one from the next:*/
                x = rows[i].getElementsByTagName("TD")[n];
                y = rows[i + 1].getElementsByTagName("TD")[n];
                /*check if the two rows should switch place,
                based on the direction, asc or desc:*/
                if (dir == "asc") {
                    if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                        //if so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                } else if (dir == "desc") {
                    if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                        //if so, mark as a switch and break the loop:
                        shouldSwitch = true;
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
                switchcount++;
            } else {
                /*If no switching has been done AND the direction is "asc",
                set the direction to "desc" and run the while loop again.*/
                if (switchcount == 0 && dir == "asc") {
                    dir = "desc";
                    switching = true;
                }
            }
        }
    }
});


