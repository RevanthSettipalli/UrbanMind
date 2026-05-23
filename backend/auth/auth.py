import json
import hashlib
from pathlib import Path


ROOT = Path(__file__).parent

USERS = ROOT / "users.json"


def load_users():

    try:

        with open(
            USERS
        ) as f:

            return json.load(
                f
            )

    except:

        return []


def save_users(data):

    with open(

        USERS,

        "w"

    ) as f:

        json.dump(

            data,

            f,

            indent=4

        )


def hash_password(password):

    return hashlib.sha256(

        password.encode()

    ).hexdigest()


def register(

    username,

    email,

    password

):

    users = load_users()

    for u in users:

        if u["email"] == email:

            return False

    users.append({

        "username": username,

        "email": email,

        "password":

        hash_password(
            password
        )

    })

    save_users(
        users
    )

    return True


def login(

    email,

    password

):

    users = load_users()

    hp = hash_password(
        password
    )

    for u in users:

        if (

            u["email"] == email

            and

            u["password"] == hp

        ):

            return u

    return None