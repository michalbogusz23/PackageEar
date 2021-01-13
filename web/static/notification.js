function check_notifications() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if(xhr.readyState == 4) {
            console.info(xhr.responseText);
        }
    };
    xhr.open("GET", "/notifications", true);
    xhr.timeout = 4000
    xhr.ontimeout = function() { 
        console.error("Timeout");
        setTimeout(check_notifications, 1000);
    }
    xhr.send();
}