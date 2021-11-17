from fastapi.testclient import TestClient
from database import *
from starlette.middleware.cors import CORSMiddleware
from app import app
import random
import string


def define_database_and_entities(**db_params):
    global db


define_database_and_entities(provider="sqlite", filename="test.sqlite", create_db=True)

client = TestClient(app)


def get_random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


#creation game succesful
def test_create_game():
    client.post(
        "user/creationuser?user_to_create=userg",
        headers={"accept": "application/json"},
    )
    response = client.post(
        "game/creationgame?game_name=game&game_creator=userg",
        headers={"accept": "application/json"},
    )
    assert response.status_code == 200


# creation game random successful


def test_create_a_game():
    client.post(
        "user/creationuser?user_to_create=usergame",
        headers={"accept": "application/json"},
    )
    rstr = get_random_string(8)
    response = client.post(
        "game/creationgame?game_name={}&game_creator=usergame".format(rstr),
        headers={"accept": "application/json"},
    )
    assert response.status_code == 200


# creation game bad (not exist user)

def test_create_gamebad_unexistuser():
    response = client.post(
        "game/creationgame?game_name=badgame&game_creator=unexist",
        headers={"accept": "application/json"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "user does not exist"}


# creation bad game (max len)

def test_create_gamebad_maxlen():
    client.post(
        "user/creationuser?user_to_create=usergame1",
        headers={"accept": "application/json"},
    )
    rstr = get_random_string(12)
    response = client.post(
        "game/creationgame?game_name={}&game_creator=usergame1".format(rstr),
        headers={"accept": "application/json"},
    )
    assert response.status_code == 404


# creation bad game (min len)

def test_create_gamebad_minlen():
    client.post(
        "user/creationuser?user_to_create=usergame2",
        headers={"accept": "application/json"},
    )
    rstr = get_random_string(1)
    response = client.post(
        "game/creationgame?game_name={}&game_creator=usergame2".format(rstr),
        headers={"accept": "application/json"},
    )
    assert response.status_code == 404


# creation bad game (user in game)

def test_create_gamebad_useringame():
    response = client.post(
        "game/creationgame?game_name=gamex&game_creator=userg",
        headers={"accept": "application/json"},
    )
    assert response.status_code == 404

# creation bad game (game exist)

def test_create_gamebad_gameexist():
    response = client.post(
        "game/creationgame?game_name=game&game_creator=userg",
        headers={'accept':'application/json'},
    )
    assert response.status_code == 404

