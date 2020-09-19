function getProductInfo(product, type){
    /* Type is = ingredients or co2 */
    url = "http://localhost:5000/"+ type +"/"+ product

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        response = JSON.parse(this.responseText)
        }
    };
    xhttp.open("GET", url , true);
    xhttp.send();
    return response.recipe.rating
}

