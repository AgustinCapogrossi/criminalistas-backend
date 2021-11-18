from fastapi.testclient import TestClient
from database import *
from starlette.middleware.cors import CORSMiddleware
from app import app
import random
import string

client = TestClient(app)

# function to create users and game for test players and turns
def test_creations():
    for i in range(3):
        client.post(
            "user/creationuser?user_to_create=usertest{}".format(i),
            headers={"accept": "application/json"},
        )
    client.post(
        "game/creationgame?game_name=gametest&game_creator=usertest0",
        headers={"accept": "application/json"},
    )
    for j in range(1, 3):
        client.post(
            "game/joingame?game_to_play=gametest&user_to_play=usertest{}".format(j),
            headers={"accept": "application/json"},
        )


# ------------------------------END TURN--------------------------------

# bad end turn game not exist


def test_end_turn_bad():
    response = client.post(
        "/player/end turn?player_name=badplayer&game_name=badgame",
        headers={"accept": "application/json"},
    )
    assert response.status_code == 404


# bad end turn (not started game)


def test_end_turn_bad_not_started():
    response = client.post(
        "/player/end turn?player_name=usertest0&game_name=gametest",
        headers={"accept": "application/json"},
    )
    assert response.status_code == 404


# function started game to successful end turn


def test_started_gametest():
    client.post(
        "/game/start_game?game_to_start=gametest",
        headers={"accept": "application/json"},
    )


# bad function not player is in turn


def test_end_turn_bad_not_player_turn():
    response = client.post(
        "/player/end turn?player_name=usertest2&game_name=gametest",
        headers={"accept": "application/json"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "player is already not in turn"}


# end turn successful


def test_end_turn():
    response = client.post(
        "/player/end turn?player_name=usertest0&game_name=gametest",
        headers={"accept": "application/json"},
    )
    assert response.status_code == 200


# --------------------------------------DICE NUMBER----------------------------------
# case successful (usertest1 in turn)


def test_dice_number():
    response = client.post(
        "/player/dice_number?player_name=usertest1&game_name=gametest",
        headers={"accept": "application/json"},
    )
    assert response.status_code == 200


# bad end turn (game not exist)


def test_bad_dice_number():
    response = client.post(
        "/player/dice_number?player_name=badplayer&game_name=badgame",
        headers={"accept": "application/json"},
    )
    assert response.status_code == 404


# bad end turn player not is turn
def test_bad_dice_number_not_player_turn():
    response = client.post(
        "/player/dice_number?player_name=usertest2&game_name=gametest",
        headers={"accept": "application/json"},
    )
    assert response.status_code == 404


# -------------------------------------SHOW_PLAYERS------------------------
def test_show_players():
    response = client.get(
        "/player/show_players?game_name=gametest",
        headers={"accept": "application/json"},
    )
    assert response.status_code == 200


# bad show players (game not exist)


def test_show_players_bad():
    response = client.get(
        "/player/show_players?game_name=gamebad",
        headers={"accept": "application/json"},
    )
    assert response.status_code == 404


# ??????????????????SUSPICION???????????????????????????

# -------------------------------SET PIECE POSITION-------------------
def test_set_piece_position():
    response = client.post(
        "/player/set_position_and_piece?player_name=usertest0",
        headers={"accept": "application/json"},
    )
    assert response.status_code == 200


# bad set piece position (player not exist)


def test_bad_set_piece_position():
    response = client.post(
        "/player/set_position_and_piece?player_name=baduser",
        headers={"accept": "application/json"},
    )
    assert response.status_code == 404


# ??????????????????????????????MOVING PLAYER???????????????????????

# ---------------------------ELIMINATION OF EXCESS DATA----------------------------


def test_delete_data_testplayer():
    for i in range(3):
        client.delete(
            "/game/exitgame?player_to_exit=usertest{}".format(i),
            headers={"accept": "application/json"},
        )
    for j in range(3):
        client.delete(
            "/user/delete_user?user_name=usertest{}".format(j),
            headers={'accept': 'application/json'}
        )