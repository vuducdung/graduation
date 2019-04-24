function get_collections(locationId) {
    $.get('/get_collections/', {locationId: locationId}, function (data) {
        let optionss = ""
        // alert(data.length)
        $.each(data, function () {
            if (this.check != '0') {
                optionss += `<div>
                                    <div class="row">
                                        <div class="col-xs-6 col-sm-6 col-mm-6 col-lg-6">
                                            <div class="caption text-center">
                                                <div class="crop suggest-collection" href="#" onclick="choice_collection(${this.id},${locationId});">${this.name}</div>
                                            </div>
                                        </div>
                                        <div class="col-xs-5 col-sm-5 col-mm-5 col-lg-5">
                                            <div>${this.count}</div>
                                        </div>
                                        <div class="col-xs-1 col-sm-1 col-mm-1 col-lg-1">
                                            <div><i class="fa fa-check"></i></div>
                                        </div>
                                    </div>
                                </div>`
            } else {
                optionss += `<div>
                                    <div class="row">
                                        <div class="col-xs-6 col-sm-6 col-mm-6 col-lg-6">
                                            <div class="caption text-center">
                                                <div class="crop suggest-collection" onclick="choice_collection(${this.id},${locationId});">` + this.name + `</div>
                                            </div>
                                        </div>
                                        <div class="col-xs-6 col-sm-6 col-mm-6 col-lg-6">
                                            <div>${this.count}</div>
                                        </div>
                                    </div>
                                </div>`
            }
        });
        $(".item-collection").html(optionss);
    });
}

function choice_collection(collectionId, locationId) {
    $.get('/choice_collection/', {collectionId: collectionId, locationId: locationId}, function (data) {
        get_collections(locationId);
    });
}

document.getElementById('shareBtn').onclick = function () {
    // alert(window.location.href)
    FB.ui({
        display: 'popup',
        method: 'share',
        href: String(window.location.hef),
    }, function (response) {
        let locationId = $('#shareBtn').attr('value').split('|')[0]
        let userId = $('#shareBtn').attr('value').split('|')[1]
        // alert($('#shareBtn').attr('value'))
        // alert(locationId != 'None' && userId != 'None')
        if (locationId != 'None' && userId != 'None') {
            $.get('/share_create/', {locationId: locationId, userId: userId}, function (data) {
                // $('#like-count').html(data);
            });
        }
    });
}
$("#create-like").click(function () {
    $("#like").toggleClass('fa fa-thumbs-up');
    $("#like").toggleClass('fa fa-check');
    var myClass = $("#like").attr("class");
    var id = this.value.split('|');
    if (myClass == 'fa fa-check') {
        if (id[0] != 'None') {
            $.get('/like_create/', {locationId: id[1], userId: id[0]}, function (data) {
                $('#like-count').html(data);
            });
        }
    } else {
        if (id[0] != 'None') {
            $.get('/like_decreate/', {locationId: id[1], userId: id[0]}, function (data) {
                $('#like-count').html(data);
            });
        }
    }
});
var slider1 = document.getElementById("myRange1");
if (!$.isEmptyObject(slider1)) {
    var slider1 = document.getElementById("myRange1");

    var slider2 = document.getElementById("myRange2");
    var slider3 = document.getElementById("myRange3");
    var slider4 = document.getElementById("myRange4");
    var slider5 = document.getElementById("myRange5");

    var output1 = document.getElementById("demo1");
    // alert(output1.innerHTML)
    var output2 = document.getElementById("demo2");
    var output3 = document.getElementById("demo3");
    var output4 = document.getElementById("demo4");
    var output5 = document.getElementById("demo5");
    output1.innerHTML = slider1.value;
    output2.innerHTML = slider2.value;
    output3.innerHTML = slider3.value;
    output4.innerHTML = slider4.value;
    output5.innerHTML = slider5.value;

    slider1.oninput = function () {
        // alert(this.value)
        output1.innerHTML = this.value;
    }

    slider2.oninput = function () {
        output2.innerHTML = this.value;
    }

    slider3.oninput = function () {
        output3.innerHTML = this.value;
    }

    slider4.oninput = function () {
        output4.innerHTML = this.value;
    }

    slider5.oninput = function () {
        output5.innerHTML = this.value;
    }
    $("#comment-form").on("submit", function () {
        //your code
        var formObj = {};
        var form = $(this).serializeArray()
        $.each(form, function (i, input) {
            formObj[input.name] = input.value;
        });
        if (formObj['locate'] == '0' || formObj['price'] == '0' || formObj['quality'] == '0' || formObj['serve'] == '0' || formObj['capacity'] == '0') {
            $("#validate-comment").text("Hãy nhập giá trị đánh giá lớn hơn 0");
            //
            return false;
        }
        //return false HAS TO BE LAST, or the rest of  the code is not executed.
    });

}

