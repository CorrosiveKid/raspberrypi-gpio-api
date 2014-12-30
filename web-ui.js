$(document).ready(function() {

});

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

    return data;
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

// List item HTML Example
// <li>
// <label for="flip-select-1">IN1:</label>
// <select id="flip-select-1" name="flip-select-1" data-role="slider">
//   <option>Off</option>
//   <option>On</option>
// </select>
// </li>

// $("#flip-select-1").val('On').slider('refresh');