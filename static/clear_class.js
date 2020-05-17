class ClearResults{
    constructor(){
        this._CLEAR_RESULT = false;
        this._CLEAR_TABLE = false;
    }

    setClearResult(truthy){
        this._CLEAR_RESULT = truthy;
    }

    setClearTable(truthy){
        this._CLEAR_TABLE = truthy;
    }

    getClearResult(){
        return this._CLEAR_RESULT;
    }

    getClearTable(){
        return this._CLEAR_TABLE;
    }

    hideResult(){
        $(document).ready(function(){
        $("#result").html("");
        });
    }
    
    resetCountry(){
        let elem =  document.getElementById("countryId");
        elem.selectedIndex = 0;
    }
    
    clearResult(){
        this.hideResult();
        this.resetCountry();
    }
    
    hideCities(){
        $(document).ready(function(){
        $("#search").html('');
        });
    }
    
    hideSpinner(){
        $(document).ready(function(){
        $("#spinner").html("");
        });
    } 
    
    cleanInput(){
        $(document).ready(function(){
        $('input[name="city"]').val('');
        });
    }
}