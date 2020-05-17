var CLEAR_RESULT = false;
var CLEAR_TABLE = false;

// I could use jQuery $(document).ready(function() { /* code here */ });
// window.onload = resetCountry;

function buttonClear(){
    clearResult();
    CLEAR_RESULT = false;
}

function inputFocus(){
    let input = document.querySelector('input');
    $('input').focus();
}

function clearResult(){
    hideResult();
    resetCountry();
}

function cleanInput(){
    $(document).ready(function(){
    $('input[name="city"]').val('');
    });
}

function resetCountry(){
    elem =  document.getElementById("countryId");
    elem.selectedIndex = 0;
}

function hideCities(){
    $(document).ready(function(){
    $("#search").html('');
    });
}

function hideResult(){
    $(document).ready(function(){
    $("#result").html("");
    });
} 

function hideSpinner(){
    $(document).ready(function(){
    $("#spinner").html("");
    });
} 

function evalForm(form){
    // clean table of cities
    hideCities();
    CLEAR_TABLE = false;
    $.get('spinner', function(data){
        //alert(data);
        document.getElementById('spinner').innerHTML = data;
    });
    var city = form['city'].value;
    var country = form['country'].value;
    var param = city;
    // country is an optional selection 
    if (country) param = param + '/' + country;
    $.get('form/' + param, function(data){
    hideSpinner();
    document.getElementById("result").innerHTML = data;
    });
    CLEAR_RESULT = true;
    cleanInput();
}

let input = document.querySelector('input');
input.onkeypress = function(){
    if (CLEAR_RESULT) {
        clearResult();
        CLEAR_RESULT = false;
    }
    if (CLEAR_TABLE)  {
    hideCities();
    CLEAR_TABLE = false;
    }
}
input.onkeyup = function(){
    // data is a table of elements that is returned from the "/search" route
    $.get('search/' + input.value, function(data){
    document.querySelector('#search').innerHTML = data; 
    });
    CLEAR_TABLE = true;
};