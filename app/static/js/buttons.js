var metrics = [];

function add_metrics(id) {
    metrics.push(document.getElementById(id).textContent);
}

function remove_metrics(id) {
    metrics.filter(function(ele){
        return ele != value;
    });
}

function parse_metrics(id) {
    
}
