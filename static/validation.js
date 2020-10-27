let PL = 'ĄĆĘŁŃÓŚŹŻ';
let pl = 'ąćęłńóśźż';
let firstname = document.getElementById('firstname');
let lastname = document.getElementById('lastname');
let password = document.getElementById('password');
let login = document.getElementById('login');
let pesel = document.getElementById('pesel');
let male = document.getElementById('male');
let female = document.getElementById('female');
let dataToValid = [firstname, lastname, password, login, pesel, male, female];


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
    } else if (fieldName === 'login') {
        return {
            isValid: loginRegExp.test(value),
            errorMessage: "Login musi zawierać od 3 do 12 małych znaków",
        };
    } else if (fieldName === 'pesel') {
        if (value.length !== 11)
            return {
                isValid: false,
                errorMessage: "Numer PESEL składa się z 11 cyfr",
            };
        let wk = 0, w = [1, 3, 7, 9];
        for (i = 0; i < 10; i++) {
            wk = (wk + parseInt(value[i]) * w[i % 4]) % 10;
            var k = (10 - wk) % 10;
        }
        return {
            isValid: parseInt(value[10]) === k,
            errorMessage: "To nie jest poprawny numer PESEL",
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


//adding listener for every needed field
dataToValid.forEach(data => {
    data.addEventListener("input", function () {
        let validation = valid(data.id, data.value);
        let test = firstname.value.length === 0 || validation.isValid;
        let error = data;
        error = error.nextElementSibling;
        if (!test) {
            data.className = "invalid";
            error.innerHTML = validation.errorMessage;
            error.className = "error active";
        } else {
            data.className = "valid";
            error.innerHTML = "";
            error.className = "error";
        }
    });
});

function validateMyForm() {
    let error = document.getElementById("submit");
    error = error.nextElementSibling;
    inputs = document.getElementsByTagName('input');

    for (var i = 0; i < inputs.length; ++i) {

        if (inputs[i].className !== "valid") {
            error.innerHTML = "Wszystkie pola muszą zostać poprawnie wypełnione";
            error.className = "error active";
            return false;
        }
    }
    if (validatePeselWithSex() === false) {
        error.innerHTML = "Płeć niezgadza się z podanym loginem";
        error.className = "error active";
        return false;
    } else {
        error.innerHTML = "";
        error.className = "error";
        return true;
    }
}

function validatePeselWithSex() {
    let peselSexDigit = parseInt(pesel.value[9]);
    let sexValue = document.querySelector('input[name="sex"]:checked').value;
    if (peselSexDigit % 2 == 1) {
        peselSexDigit = "M"
    } else {
        peselSexDigit = "F"
    }
    return peselSexDigit === sexValue;
}

function checkIfLoginIsFree(loginField, errorField) {
    return new Promise((resolve, reject) => {
        loginString = loginField.value;
        const url = `https://pi.iem.pw.edu.pl/user/${loginString}`;
        var response = new XMLHttpRequest();
        response.open("GET", url);

        response.onload = function () {
            if (response.status === 404) {
                login.className = "valid";
                errorField.innerHTML = "";
                errorField.className = "error";
                resolve(true);
            }
            else if (response.status === 200) {
                login.className = "invalid";
                errorField.innerHTML = "Podany login jest zajęty";
                errorField.className = "error active";
                resolve(false);

            }
        };

        response.send();
    });
}