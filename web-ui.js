$(document).ready(function() {
    buildHTML();
    $(".flipswitch").on('change', function(){
        var currentValue = $(this).val();
        var pinNumber = $(this).attr("pin-number");

        if (currentValue === "On"){
            // setPinStatus(pinNumber, 1);
            console.log("setPinStatus(" + pinNumber + ", 1)");
        }
        else if (currentValue === "Off"){
            // setPinStatus(pinNumber, 0);
            console.log("setPinStatus(" + pinNumber + ", 0)");
        }
    });
});

function buildHTML(){
    // var pins = getPinStatus();
    var pins = getPinStatusTest();
    pins.forEach(function(pin) {
        var $listItem = $("<li></li>");
        var $label = $("<label for='flip-select-"+ pin.pin_number +"'>" + pin.pin_name + "</label>");
        var $select = $("<select id='flip-select-" + pin.pin_number + "' data-role='slider' pin-number='" + pin.pin_number + "' name='flip-select-" + pin.pin_number + "' class='flipswitch'></select>");
        var $optionOn = $("<option>On</option>");
        var $optionOff = $("<option>Off</option>");
        $select.append($optionOff, $optionOn);
        $listItem.append($label, $select);
        $("#switches").append($listItem);
    });
}

function getPinStatus(){
    var data;
    var apiEndpoint = "/api/v1/gpio/status/";

    $.ajax({
        url: apiEndpoint,
        type: "GET"
    }).done(function(responseData) {
        console.log("GET: " + apiEndpoint  + " - Successful!");
        data = responseData;
    }).fail(function() {
        console.log("GET: " + apiEndpoint  + " - Failed!");
    });

    return data.data;
}

function setPinStatus(pinNumber, value){
    var data;
    var apiEndpoint = "/api/v1/gpio/" + pinNumber + "/";
    var postData = {"value": value};

    $.ajax({
        url: apiEndpoint,
        type: "POST",
        data: postData
    }).done(function(responseData){
        console.log("POST: " + apiEndpoint + " - Successful!");
        data = responseData;
    }).fail(function(){
        console.log("POST: " + apiEndpoint + " - Failed!");
    });

    return data;
}

function getPinStatusTest(){
    var pinList = [];
    for (i=0; i<8; i++){
        var object = {
            "pin_number": i,
            "pin_name": "IN:" + i,
            "value": 0
        };
        pinList.push(object);
    }
    var data = {
        "data": pinList
    };

    return data.data;
}

// $("#flip-select-1").val('On').slider('refresh');