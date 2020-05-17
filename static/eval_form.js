function evalForm(form){
    // clean table of cities
    clear.hideCities();
    clear.setClearTable(false);
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
      clear.hideSpinner();
      document.getElementById("result").innerHTML = data;
    });
    clear.setClearResult(true);
    clear.cleanInput();
  }
