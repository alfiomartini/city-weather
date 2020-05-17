let clear = new ClearResults();
let input = document.querySelector('input');
input.onkeypress = function(){
    if (clear.getClearResult()) {
        clear.clearResult();
        clear.setClearResult(false);
    }
    if (clear.getClearTable()){
        clear.hideCities();
        clear.setClearTable(false);
    }
}
input.onkeyup = function(){
    // data is a table of elements that is returned from the "/search" route
    $.get('search/' + input.value, function(data){
    document.querySelector('#search').innerHTML = data; 
    });
    clear.setClearTable(true);
};