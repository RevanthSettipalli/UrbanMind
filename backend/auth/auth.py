import json
import hashlib
from pathlib import Path


# ==========================
# PATH
# ==========================

ROOT = Path(__file__).parent

USERS = ROOT / "users.json"


# ==========================
# CREATE FILE
# ==========================

if not USERS.exists():

    USERS.write_text("[]")


# ==========================
# LOAD
# ==========================

def load_users():

    try:

        with open(
            USERS,
            "r"
        ) as f:

            return json.load(f)

    except Exception:

        return []


# ==========================
# SAVE
# ==========================

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


# ==========================
# HASH
# ==========================

def hash_password(password):

    return hashlib.sha256(

        password.encode()

    ).hexdigest()


# ==========================
# REGISTER
# ==========================

def register(

    username,

    email,

    password

):

    username = username.strip()

    email = email.strip().lower()

    password = password.strip()

    if (

        not username

        or

        not email

        or

        not password

    ):

        return False

    users = load_users()

    for user in users:

        if (

            user["email"]

            .lower()

            ==

            email

        ):

            return False


    new_user = {

        "username": username,

        "email": email,

        "password": hash_password(
            password
        )

    }

    users.append(
        new_user
    )

    save_users(
        users
    )

    return True


# ==========================
# LOGIN
# ==========================

def login(

    email,

    password

):

    email = email.strip().lower()

    hp = hash_password(
        password
    )

    users = load_users()

    for user in users:

        if (

            user["email"]

            .lower()

            ==

            email

            and

            user["password"]

            ==

            hp

        ):

            return {

                "username":

                user["username"],

                "email":

                user["email"]

            }

    return None


# ==========================
# GET USERS
# ==========================

def get_all_users():

    users = load_users()

    return [

        {

            "username":

            u["username"],

            "email":

            u["email"]

        }

        for u in users

    ]