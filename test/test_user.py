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


