var CLEAR_RESULT = false;
var CLEAR_TABLE = false;

function clearResult(){
    hideResult();
    resetCountry();
}

function hideResult(){
    $(document).ready(function(){
    $("#result").html("");
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

function hideSpinner(){
    $(document).ready(function(){
    $("#spinner").html("");
    });
} 

function cleanInput(){
    $(document).ready(function(){
    $('input[name="city"]').val('');
    });
}