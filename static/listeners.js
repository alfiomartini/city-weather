addEventListener('DOMContentLoaded', listeners);

// an attempt to make things as locally as possible.
// I coild also pass the three variables below as
// arguments (using currying). I have to take a look
// at this.
function listeners(){
    let clearR = new ClearResults();
    let input = document.querySelector('input');
    let form = document.querySelector('form');

    input.addEventListener('keypress', search_clean);
    input.addEventListener('keyup', search_get);
    form.addEventListener('submit', evalForm);

    function search_clean(){
        if (clearR.getClearResult()) {
            clearR.clearResult();
            clearR.setClearResult(false);
        }
        //if (clearR.getClearTable()){
        //    clearR.hideCities();
        //    clearR.setClearTable(false);
        //}
    }
    
    function search_get(){
        // data is a table of elements that is returned from the "/search" route
        $.get('search/' + this.value, function(data){
        document.querySelector('#search').innerHTML = data; 
        });
        //clearR.setClearTable(true);
    }

    function evalForm(event){
        event.preventDefault();
        //clean table of cities
        clearR.hideCities();
        clearR.setClearTable(false);
        $.get('spinner', function(data){
             document.getElementById('spinner').innerHTML = data;
        });
        let city = this['city'].value;
        let country = this['country'].value;
        let param = city;
        // country is an optional selection 
        if (country) param = param + '/' + country;
        $.get('form/' + param, function(data){
          clearR.hideSpinner();
          document.getElementById("result").innerHTML = data;
        });
        clearR.setClearResult(true);
        clearR.cleanInput();
      }
}