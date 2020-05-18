addEventListener('DOMContentLoaded', listeners);

// an attempt to make things as locally as possible.
// I could also pass the three variables below as
// arguments (using currying). I have to take a look
// at this.
function listeners(){
    let clearR = new ClearResults();
    let input = document.querySelector('input');
    let form = document.querySelector('form');
    let debounceTimeout = null;

    input.addEventListener('keypress', search_clean);
    input.addEventListener('paste', search_clean);
    input.addEventListener('keyup', search_get);
    input.addEventListener('change', search_get);
    form.addEventListener('submit', evalForm);

    function search_clean(){
        if (clearR.getClearResult()) {
            clearR.clearResult();
            clearR.setClearResult(false);
        }
    }

    function searchEvents(){
        let input = document.querySelector('input');
        let term = input.value;
        //remove spaces from both sides
        term = term.trim();
        if (term){
            $.ajax({
            url: 'search/' + term,
            method: 'get',
            async: true, // notice this line
            })
            .done(function(data, status, xhr){
                document.querySelector('#search').innerHTML = data;
            })
            .fail(function(xhr, status, error){
                    console.log(error);
            });
        }
        else{
           document.querySelector('#search').innerHTML = ''; 
        }
    }
    
    function search_get(event){
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(searchEvents, 200);
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