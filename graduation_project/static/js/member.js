

function get_collection() {
    $.get('/get_collection/', function (data) {
        let optionss = ""
        $.each(data, function () {
            optionss += `<div onclick="change(${this.id},'${this.name}'),locations_in_collection(${this.id})" 
class="col-xs-3 col-sm-3 col-mm-3 col-lg-3 change suggest-collection">
                                    <a href="#"><img src=${this.avatar} alt=""
                                         style="width: 100%"
                                         class="img-thumbnail img-fluid"></a>
                                    <div class="caption text-center">
                                        <div class="crop"> ${this.name}</div>
                                    </div>
                                </div>`
        });
        $("#cat").html(optionss);
    });
}

function deleteColl(collectionId) {
    $.get('/collection_delete/', {collectionId: collectionId}, function (data) {
        get_collection()
    });

}

function locations_in_collection(collectionId) {
    $.get('/locations_in_collection/', {collectionId: collectionId}, function (data) {
        let optionss = ""
        $.each(data, function () {
            optionss += `
            <div>
            <a href="/ha-noi/${this.url}"><img style="width:30px;height:30px;" src="${this.avatar}" alt=""></a>
            <a href="/ha-noi/${this.url}"><span>${this.name}</span></a>
            <i class="fa fa-trash" onclick="delete_location_in_collection(${this.id},${collectionId});" aria-hidden="true"></i>
            </div> 
            `
        });
        $("#location-list").html(optionss);
    });
}

function delete_location_in_collection(locationId, collectionId) {
    $.get('/delete_location_in_collection/', {collectionId: collectionId, locationId: locationId}, function (data) {
        locations_in_collection(collectionId);
    });
}

function location_to_collection(locationId, collectionId) {
    $.get('/location_to_collection/', {locationId: locationId, collectionId: collectionId}, function (data) {
        if (data == 'None') {
            alert('Địa điểm đã có trong bộ sưu tập')
            return false;
        }
        locations_in_collection(collectionId);
    });
    $(".close").click();
}

function suggest_location () {
    let name = $("#name-location").val();
    // alert(name)
    let collection_id = $(".addLocation").attr('value');
    $.get('/location_suggest/', {location_name: name}, function (data) {
        let optionss = ""
        $.each(data, function () {
            optionss += `
            <div class="suggest-collection" onclick="location_to_collection(${this.id},${collection_id})">
            <img style="width:30px;height:30px;" src="${this.avatar}" alt="">
            <span>${this.name}</span>
            </div>
            `
        });
        $("#location-suggest").html(optionss);
    });
}


function change(col_id, col_name) {
    let collec = '';
    if (col_name != 'Yêu thích') {
        let name_html = `<div class="col-xs-3 col-sm-3 col-mm-3 col-lg-3" > 
<button type="button" 
 class="btn btn-outline-warning crop">${col_name}</button></div>`
        collec += `
<div class="container"><div class="row">` + name_html + `
  <div class="col-xs-3 col-sm-3 col-mm-3 col-lg-3">
  <button type="button" data-toggle="modal" data-target="#addColl" 
  class="btn btn-outline-warning addLocation" value="${col_id}">Thêm địa điểm</button></div>
  <div class="col-xs-3 col-sm-3 col-mm-3 col-lg-3"><button type="button" id="delete-collection"
  onclick="deleteColl(${col_id},'${col_name}')"
  class="btn btn-outline-danger">Xóa bộ sưu tập</button></div>
  </div>
  <div class="row" style="margin-top: 20px;"><div id="location-list"></div></div>
</div>
`
        $("#cat").html(collec)
    } else {
        let name_html = `<div class="col-xs-3 col-sm-3 col-mm-3 col-lg-3" > <button type="button" class="btn btn-outline-warning">${col_name}</button></div>`
        collec += `
<div class="container"><div class="row">` + name_html + `
  <div class="col-xs-3 col-sm-3 col-mm-3 col-lg-3">
  <button type="button" data-toggle="modal" data-target="#addColl" 
  class="btn btn-outline-warning addLocation" value="${col_id}">Thêm địa điểm</button></div>
  <div class="col-xs-3 col-sm-3 col-mm-3 col-lg-3"></div>
  <div id="location-list" style="margin-top: 20px;"></div>
</div></div>
`
        $("#cat").html(collec)
    }
}


function create_collection() {
    if ($("#name-col").val() == '') {
        alert('Hãy nhập tên bộ sưu tập');
        return false;
    }
    alert($('form#collection-form').serialize());
    $.get('/collection_create/', $('form#collection-form').serialize(), function (data) {

        if (data == 'None') {
            alert('Bộ sưu tập đã tồn tại');
            // $("#validate-name").replaceWith('Bộ sưu tập đã tồn tại');
            return false;
        }
        // alert(data )
        get_collection();

        $('form#collection-form')[0].reset();
        $("#close").click();
    });

}

function create_collection1() {
    if ($("#col_name").val() == '') {
        alert('Hãy nhập tên bộ sưu tập');
        return false;
    }
    alert($('form#collection-form1').serialize());
    $.get('/collection_create/', $('form#collection-form1').serialize(), function (data) {

        if (data == 'None') {
            alert('Bộ sưu tập đã tồn tại');
            // $("#validate-name").replaceWith('Bộ sưu tập đã tồn tại');
            return false;
        }
        // alert(data )
        get_collection();

        $('form#collection-form1')[0].reset();
        $("#back").click();
        // $("#close").click();
    });

}