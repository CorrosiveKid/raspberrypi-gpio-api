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
        var $listItem = $("<li class='ui-grid-a'></li>");
        var $label = $("<label class='ui-block-a custom-label' for='flip-select-"+ pin.pin_number +"'>" + pin.pin_name + "</label>");
        var $select = $("<select id='flip-select-" + pin.pin_number + "' data-role='slider' pin-number='" + pin.pin_number + "' name='flip-select-" + pin.pin_number + "' class='flipswitch ui-block-b'></select>");
        var $optionOn = $("<option>On</option>");
        var $optionOff = $("<option>Off</option>");
        $select.append($optionOff, $optionOn);
        $listItem.append($label, $select);
        $("#switches").append($listItem);
    });
}

function getPinStatus(){
    var data;
    var apiEndpoint = "http://192.168.1.111/api/v1/gpio/status/";

    $.ajax({
        url: apiEndpoint,
        type: "GET",
        async: false
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
    var apiEndpoint = "http://192.168.1.111/api/v1/gpio/" + pinNumber + "/";
    var postData = {"value": value};

    $.ajax({
        url: apiEndpoint,
        type: "POST",
        async: false,
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

    var object1 = {
        "pin_number": 0,
        "pin_name": "Audio System",
        "value": 1
    };

    var object2 = {
        "pin_number": 1,
        "pin_name": "Xbox 360",
        "value": 0
    };

    var object3 = {
        "pin_number": 2,
        "pin_name": "Xbox 360 Slim",
        "value": 0
    };

    var object4 = {
        "pin_number": 3,
        "pin_name": "Fan",
        "value": 1
    };
    
    pinList.push(object1);
    pinList.push(object2);
    pinList.push(object3);
    pinList.push(object4);
    
    var data = {
        "data": pinList
    };

    return data.data;
}
// $("#flip-select-1").val('On').slider('refresh');