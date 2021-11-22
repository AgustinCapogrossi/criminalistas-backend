from fastapi.testclient import TestClient
from database import *
from starlette.middleware.cors import CORSMiddleware
from app import app

client = TestClient(app)

# function to create users and game for test cards
def test_creations():
    for i in range(3):
        client.post(
            "/user/creationuser?user_to_create=testuser{}".format(i),
            headers={"accept": "application/json"},
        )
    client.post(
        "/game/creationgame?game_name=testgame&game_creator=testuser0",
        headers={"accept": "application/json"},
    )
    for j in range(1, 3):
        client.post(
            "/game/joingame?game_to_play=testgame&user_to_play=testuser{}".format(j),
            headers={"accept": "application/json"},
        )
    client.post(
        "/game/start_game?game_to_start=testgame",
        headers={"accept": "application/json"},
    )


# ----------------------------SELECT_ENVELOPE-------------------

# select envelope successful
def test_select_envelope():
    response = client.post(
        "/cards/envelope?game_name=testgame",
        headers={"accept": "application/json"},
    )
    assert response.status_code == 200


# bad select envelope (game not exist)
def test_bad_select_envelope():
    response = client.post(
        "/cards/envelope?game_name=badgame",
        headers={"accept": "application/json"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "game doesn't exist"}


# -------------------------------DISTRIBUTIVE CARDS--------------------------------------


def test_distribute_cards():
    response = client.post(
        "/cards/distribute_cards?a_game=testgame",
        headers={"accept": "application/json"},
    )
    assert response.status_code == 200


# bad distribute cards (game not exist)
def test_bad_distribute_cards():
    response = client.post(
        "/cards/distribute_cards?a_game=badgame",
        headers={"accept": "application/json"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "game doesn't exist"}


#------------------SUSPICION------------------------------

def test_suspicion():
    response = client.post(
        "/cards/suspicion?player_who_suspects=testuser0&monster_card=Frankenstein&victim_card=Conde&room_card=Cochera"
    )
    assert response.status_code == 200

#---------------------ACCUSATION-----------------------
def test_accusation():
    response = client.post(
        "/cards/accusation?player_who_accuse=testuser0&monster_card=Frankenstein&victim_card=Conde&room_card=Cochera"
    )
    assert response.status_code == 200
# ---------------------------ELIMINATION OF EXCESS DATA----------------------------


def test_delete_data_testplayer():
    for i in range(3):
        client.delete(
            "/game/exitgame?player_to_exit=testuser{}".format(i),
            headers={"accept": "application/json"},
        )
    for j in range(3):
        client.delete(
            "/user/delete_user?user_name=testuser{}".format(j),
            headers={"accept": "application/json"},
        )
