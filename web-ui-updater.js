updateSwitches();

setInterval(function(){
    updateSwitches();
}, 30000);

function updateSwitches(){
    // var pins = getPinStatus();
    var pins = getPinStatusTest();
    console.log("Updating Switches")
    pins.forEach(function(pin) {
        var id = "#flip-select-" + pin.pin_number;

        if (pin.value == 0){
            $(id).val('Off').slider('refresh');
        }
        else{
            $(id).val('On').slider('refresh');
        }
    });
}