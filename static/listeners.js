addEventListener('DOMContentLoaded', listeners);

function listeners(){
    let input = document.querySelector('#form-weather input');
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
                clean();
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
           clean();
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
            clean();
            result.innerHTML = html;
            input.value = '';
        })
        .catch(error => {
            console.log(error);
        });
    }

    function clean(){
        let result = document.getElementById('result');
        let search = document.getElementById('search');

        result.innerHTML = '';    
        search.innerHTML = '';
    }
}