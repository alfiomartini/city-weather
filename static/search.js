function search_clean(){
    if (clear.getClearResult()) {
        clear.clearResult();
        clear.setClearResult(false);
    }
    if (clear.getClearTable()){
        clear.hideCities();
        clear.setClearTable(false);
    }
}

function search_get(){
    // data is a table of elements that is returned from the "/search" route
    $.get('search/' + this.value, function(data){
    document.querySelector('#search').innerHTML = data; 
    });
    clear.setClearTable(true);
}