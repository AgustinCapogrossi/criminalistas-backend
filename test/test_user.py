from fastapi.testclient import TestClient
from database import *
from starlette.middleware.cors import CORSMiddleware
from app import app
import random
import string

def define_database_and_entities(**db_params):
    global db
define_database_and_entities(
    provider='sqlite', filename='test.sqlite', create_db=True)

client = TestClient(app)

def get_random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))

#Creation new user
def test_create_a_user():
    register = client.post(
        "user/creationuser?user_to_create=user",
    headers={'accept': 'application/json'}
    )
    assert register.status_code == 200

# Creation new user random
def test_create_user():
    rstr = get_random_string(8)
    register = client.post(
        "/user/creationuser?user_to_create={}".format(rstr),
        headers={'accept': 'application/json'}
        )
    assert register.status_code == 200

# Bad Creation user exist

def test_creation_user_exist():
    register = client.post(
        "user/creationuser?user_to_create=user",
        headers={'accept':'application/json'}
    )
    assert register.status_code == 404

# Bad Creaton user max len
def test_creation_user_maxlen():
    rstr = get_random_string(12)
    register = client.post(
        "/user/creationuser?user_to_create={}".format(rstr),
        headers={'accept':'application/json'}
    )
    assert register.status_code == 404

#Bad Creation user min len
def test_creation_user_minlen():
    rstr = get_random_string(1)
    register = client.post(
        "/user/creationuser?user_to_create={}".format(rstr),
        headers={'accept':'application/json'}
    )
    assert  register.status_code == 404

#Delete user successful
def test_delete_user():
    deleter = client.delete(
        "/user/delete_user?user_name=user",
        headers={'accept':'application/json'}
    )
    assert deleter.status_code == 200

#Delete user bad (user not exist)
def test_delete_userunexist():
    deleter = client.delete(
        "/user/delete_user?user_name=user",
        headers={'accept':'application/json'}
    )
    assert  deleter.status_code == 404
