addEventListener('DOMContentLoaded', listeners);

// an attempt to make things as locally as possible.
// I could also pass the three variables below as
// arguments (using currying). I have to take a look
// at this.
function listeners(){
    let input = document.querySelector('#form-weather input');
    let result = document.getElementById('result');
    let debounceTimeout = null;
    
    input.addEventListener('keyup', search_get);  
   
    function searchEvents(){
        let term = input.value;
        //remove spaces from both sides
        term = term.trim();
        if (term){
            $.ajax({
            url: '/search/' + term,
            method: 'get',
            async: true, // notice this line
            })
            .done(function(search_list, status, xhr){
                // console.log(data);
                document.getElementById("result").innerHTML = '';
                document.querySelector('#search').innerHTML = search_list;
                let search_links = document.querySelectorAll('.search-container li');
                search_links.forEach(link => {
                    link.addEventListener('click', api_route)
                })
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
        debounceTimeout = setTimeout(searchEvents, 400);
    }

    function api_route(){
        route = this.dataset.city; //this = link (list item) that triggered the event
        // console.log(route);
        fetch(route)
        .then(response => response.text())
        .then(html  => {
            document.getElementById("search").innerHTML = '';
            result.innerHTML = html;
            input.value = '';
        })
        .catch(error => {
            console.log(error);
        });
    }

}