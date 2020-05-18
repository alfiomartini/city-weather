function evalForm(){
    //clean table of cities
    console.log('form submitted');
    clear.hideCities();
    clear.setClearTable(false);
    $.get('spinner', function(data){
         //alert(data);
         document.getElementById('spinner').innerHTML = data;
    });
    let city = this['city'].value;
    console.log(city);
    let country = this['country'].value;
    console.log(country);
    let param = city;
    // country is an optional selection 
    if (country) param = param + '/' + country;
    $.get('form/' + param, function(data){
      clear.hideSpinner();
      document.getElementById("result").innerHTML = data;
    });
    clear.setClearResult(true);
    clear.cleanInput();
  }
