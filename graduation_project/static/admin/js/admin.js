function get_required_message() {
    $.get('/admin/get_required_message/', function (data) {
        let messages = `<li>
                            <div class="notification_header">
                                <h3 class="count-message">You have ${data[0].count} new messages</h3>
                            </div>
                        </li>`
        $.each(data, function () {
            $(".badge").html(this.count)
            $(".notification_desc").html(` ${this.require_name} `)
            messages += `<li>
                            <a href="/admin/location/?id=${this.loc_id}">
                                <div class="user_img"><img id="user-avatar" src="${this.user_avatar}" alt=""></div>
                                <div class="notification_desc">
                                    <p>${this.require_name}</p>
                                    <!--<p><span>1 hour ago</span></p>-->
                                </div>
                                <div class="clearfix"></div>
                            </a>
                        </li>`

        });
        $("#messages").html(messages)
    });
}

get_required_message();

var ready = $(document).ready(function () {

    $(".form-control").keydown(function (e) {
        if (e.keyCode == 13) {
            return false;
        }
    });
    $("#update-button").click(function () {
        $("#show-button-update").show();
    });

    $(".page-link").click(function () {
        pageURL = window.location.href;
        if ($(this).attr("value")) {
            if (pageURL.includes("?")) {
                pageURL = pageURL.split("?")[0];
            }
            pageURL += '?page=' + $(this).attr("value");
            window.location.replace(pageURL);
        }
    });

    // $("#location-name").keydown(function (e) {
    //     pageURL = window.location.href;
    //     if (e.keyCode == 13) {
    //         if ($("#location-name").val()) {
    //             if (pageURL.includes("?")) {
    //                 pageURL = pageURL.split("?")[0];
    //             }
    //             pageURL += '?locationName=' + $("#location-name").val();
    //             window.location.replace(pageURL);
    //         }
    //     }
    // });


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

    }

    // saveSearchForm();
    // var input1 = document.getElementById("word-search");
    // input1.addEventListener("keyup", function (event) {
    //     if (event.keyCode === 13) {
    //         event.preventDefault();
    //         submitSearch();
    //     }
    // });
    // var input2 = document.getElementById("cat-search");
    // input2.addEventListener("keyup", function (event) {
    //     if (event.keyCode === 13) {
    //         event.preventDefault();
    //         submitSearch();
    //     }
    // });
    // var input3 = document.getElementById("loc-search");
    // input3.addEventListener("keyup", function (event) {
    //     if (event.keyCode === 13) {
    //         event.preventDefault();
    //         submitSearch();
    //     }
    // });
    // var input4 = document.getElementById("cui-search");
    // input4.addEventListener("keyup", function (event) {
    //     if (event.keyCode === 13) {
    //         event.preventDefault();
    //         submitSearch();
    //     }
    // });

    // const go = document.getElementById("but-sub");
    // go.addEventListener("click", submitSearch);

    // function submitSearch() {
    //     let pageURL = window.location.href;
    //     if (pageURL.includes("search")) {
    //         pageURL = pageURL.split("search/")[0];
    //     }
    //     pageURL += 'search/?';
    //     let word = $("#word").val();
    //     let loc = $("#select-loc").val();
    //     let cat = $("#select-cat").val();
    //     let cui = $("#select-cui").val();
    //     if (word) {
    //         pageURL += 'word=' + word + '&';
    //     }
    //     if (loc) {
    //         pageURL += 'loc=' + loc + '&';
    //     }
    //     if (cat) {
    //         pageURL += 'cat=' + cat + '&';
    //     }
    //     if (cui) {
    //         pageURL += 'cui=' + cui;
    //     }
    //     window.location.replace(pageURL);
    // }

    function getQueryStringValue(key) {
        return decodeURIComponent(window.location.search.replace(new RegExp("^(?:.*[&\\?]" + encodeURIComponent(key).replace(/[\.\+\*]/g, "\\$&") + "(?:\\=([^&]*))?)?.*$", "i"), "$1"));
    }

});


