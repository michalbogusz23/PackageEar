function check_notifications() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if(xhr.readyState == 4 && xhr.status == 200) {
            console.info(xhr.responseText);
            setTimeout(check_notifications, 1000);
        }
    };
    xhr.open("GET", "/notifications", true);
    xhr.timeout = 30000
    xhr.ontimeout = function() { 
        console.error("Timeout");
        setTimeout(check_notifications, 1000);
    }
    xhr.send();
}
check_notifications();