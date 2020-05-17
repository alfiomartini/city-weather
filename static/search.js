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