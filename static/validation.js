let PL = 'ĄĆĘŁŃÓŚŹŻ';
let pl = 'ąćęłńóśźż';
let firstname = document.getElementById('firstname');
let lastname = document.getElementById('lastname');
let password = document.getElementById('password');
let login = document.getElementById('login');
let passwordCheck = document.getElementById('passwordCheck');
let male = document.getElementById('male');
let female = document.getElementById('female');
let submit = document.getElementById('submit')
let form = document.getElementById('registerForm')
let dataToValid = [firstname, lastname, password, passwordCheck, login, male, female];


var firstnameRegExp = new RegExp('[A-Z{PL}][a-z{pl}]+');
var lastnameRegExp = new RegExp('[A-Z{PL}][a-z{pl}]+');
var passwordRegExp = new RegExp('[A-Za-z]{8,}');
var loginRegExp = new RegExp('[a-z]{3,12}');

function valid(fieldName, value) {
    if (fieldName === 'firstname') {
        return {
            isValid: firstnameRegExp.test(value),
            errorMessage: "Imię musi rozpoczynać się wielką literą",
        };
    } else if (fieldName === 'lastname') {
        return {
            isValid: lastnameRegExp.test(value),
            errorMessage: "Nazwisko musi rozpoczynać się wielką literą",
        };
    } else if (fieldName === 'password') {
        return {
            isValid: passwordRegExp.test(value),
            errorMessage: "Hasło musi posiadać powyżej 8 znaków angielskiego alfabetu",
        };
    } else if (fieldName === 'passwordCheck') {
        return {
            isValid: value === password.value,
            errorMessage: "Oba hasła muszą być identyczne",
        };

    } else if (fieldName === 'login') {
        return {
            isValid: loginRegExp.test(value),
            errorMessage: "Login musi zawierać od 3 do 12 małych znaków",
        };
    } else if (fieldName === 'male' || fieldName === 'female') {

        return {
            isValid: true,

        }
    }
}
login.addEventListener("change", function () {
    let error = login;
    error = error.nextElementSibling;
    error = error.nextElementSibling;
    checkIfLoginIsFree(login, error)
});

submit.onclick = function() {
    if(!validateMyForm()) {
        return false;
    }
    
}

//adding listener for every needed field
dataToValid.forEach(data => {
    data.addEventListener("input", function () {
        let validation = valid(data.id, data.value);
        let test =  validation.isValid;
        let error = data;
        error = error.nextElementSibling;
        if (!test) {
            data.className = "invalid";
            error.innerText = validation.errorMessage;
            error.className = "error active";
        } else {
            data.className = "valid";
            error.innerText = "";
            error.className = "error";
        }
    });
});

function validateMyForm() {
    error = document.getElementById("finalError");
    inputs = document.getElementsByTagName('input');

    for (var i = 0; i < inputs.length; ++i) {
        if (inputs[i].className !== "valid") {
            error.innerText = "Wszystkie pola muszą zostać poprawnie wypełnione";
            error.className = "error active";
            return false;
        }
    }
    return true;
}

function checkIfLoginIsFree(loginField, errorField) {
    return new Promise((resolve, reject) => {
        loginString = loginField.value;
        const url = `https://infinite-hamlet-29399.herokuapp.com/check/${loginString}`;
        var response = new XMLHttpRequest();
        response.open("GET", url);

        response.onload = function () {
            var serverResponse = JSON.parse(this.responseText);
            if (serverResponse[loginString] === "available") {

                login.className = "valid";
                errorField.innerHTML = "";
                errorField.className = "error";
                resolve(true);
            }
            else if (serverResponse[loginString] === "taken") {
                login.className = "invalid";
                errorField.innerHTML = "Podany login jest zajęty";
                errorField.className = "error active";
                resolve(false);
            }
        };

        response.send();
    });
}