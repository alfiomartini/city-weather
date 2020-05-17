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
