from bcrypt import hashpw, gensalt
import uuid

from redis import Redis
db = Redis(host='localhost', port=6379, db=0)

users = [{
        "firstname": "Michał",
        "lastname": "michał",
        "password": "admin",
        "login": "admin",
        "email": "mail@mail",
        "address": "Lublin"
    }, {
        "firstname": "Jack",
        "lastname": "Sparrow",
        "password": "savvy",
        "login": "WhyIsTheRumGone",
        "email": "jack@mail.ht",
        "address": "Ask for me on Tortuga"
    }
]

packages = [{
	    "receiver_name": "Adresat 1",
	    "box_id": "Warszawa, pulawska_1",
	    "size": "l"
    }, {
        "receiver_name": "Adresat 2",
	    "box_id": "Lublin, kunickiego_11",
	    "size": "m"
    }, {
        "receiver_name": "Adresat 3",
	    "box_id": "Nowy paczkomat",
	    "size": "s"
    }]


def save_user(user):
    salt = gensalt(5)
    password = user['password'].encode()
    hashed = hashpw(password, salt)
    user['password'] = hashed
    login = user['login']

    db.hmset(f"user:{login}", user)

    return True


def save_package(package, login):
    package_id = str(uuid.uuid4())
    db.hmset(f"package:{login}:{package_id}", package)

for user in users:
    save_user(user)

for package in packages:
    save_package(package, users[0]["login"])


