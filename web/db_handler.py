from app import session, db, app
from bcrypt import hashpw, gensalt, checkpw
import uuid


def save_user(user):
    salt = gensalt(5)
    password = user['password'].encode()
    hashed = hashpw(password, salt)
    user['password'] = hashed

    login = user['login']
    del user['login']

    db.hmset(f"user:{login}", user)

    return True

def verify_user(login, password):
    password = password.encode()
    hashed = db.hget(f'user:{login}', "password")
    if not hashed:
        print(f"ERROR: No password for {login}", file=sys.stderr)
        return False

    return checkpw(password, hashed)

def is_user(login):
    return db.hexists(f"user:{login}", "password")

def save_package(package):
    package_id = str(uuid.uuid4())

    login = session["user"]

    db.hmset(f"package:{login}:{package_id}", package)

    return True
    
def get_packages():
    packages = []

    login = session["user"]
    keys = db.keys(pattern=f"package:{login}*")
     
    for key in keys:
        package = db.hgetall(key)
        package = decode_redis(package)
        package["id"] = key.decode().split(":")[2]
        packages.append(package)

    return packages

def delete_package_from_db(id):
    login = session["user"]
    key = f"package:{login}:{id}"

    db.delete(key)

    return True

def decode_redis(src):
    if isinstance(src, list):
        rv = list()
        for key in src:
            rv.append(decode_redis(key))
        return rv
    elif isinstance(src, dict):
        rv = dict()
        for key in src:
            rv[key.decode()] = decode_redis(src[key])
        return rv
    elif isinstance(src, bytes):
        return src.decode()
    else:
        raise Exception("type not handled: " +type(src))