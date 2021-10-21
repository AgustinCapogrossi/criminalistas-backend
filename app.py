from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from database import *
from pydantic_models import *

MAX_LEN_NAME_GAME = 10
MIN_LEN_NAME_GAME = 3
MAX_LEN_NAME_NICK = 6
MIN_LEN_NAME_NICK = 3

app = FastAPI(title="mystery")

origins = ["http://localhost:3000" "localhost:3000"]

# creating a game


@app.post("/creationgame")
async def game_creation(gametocreate: GameTemp):
    """It creates an empty game with no players"""
    invalid_fields = HTTPException(status_code=404, detail="field size is invalid")
    if (
        len(gametocreate.game_name) > MAX_LEN_NAME_GAME
        or len(gametocreate.game_name) < MIN_LEN_NAME_GAME
    ):
        raise invalid_fields
    elif game_exist(gametocreate.game_name):
        raise HTTPException(status_code=404, detail="game exist")
    else:
        gametocreate.is_full = False
        gametocreate.is_started = False
        new_game(gametocreate.game_name)
        return {"game": gametocreate.game_name}


# joining a game


@app.post("/joingame")
async def join_game(gametojoin: GameTemp, player_to_play: str):
    """It allows the user to join a match, as long as the match is not full or already ongoing"""
    if is_full(gametojoin):
        raise HTTPException(status_code=404, detail="game is full")
    if not game_exist(gametojoin):
        raise HTTPException(status_code=404, detail="game does not exist")
    elif is_started(gametojoin):
        raise HTTPException(status_code=404, detail="game is not available")
    else:
        join_game(gametojoin.game_name)
        add_player(gametojoin.num_players)
        insert_player(gametojoin.game_name, player_to_play)
        return {"joining game": gametojoin.game_name}


# creating a nickname/user


@app.post("/creationuser")
async def user_creation(user_to_create: str):
    """It allows the player to set a nickname which will be displayed in game"""
    invalid_fields = HTTPException(status_code=404, detail="field size is invalid")
    if (
        len(user_to_create) > MAX_LEN_NAME_GAME
        or len(user_to_create) < MIN_LEN_NAME_GAME
    ):
        raise invalid_fields
    elif user_exist(user_to_create):
        raise HTTPException(status_code=404, detail="user exist")
    else:
        new_user(user_to_create)
        return {"user": user_to_create}
