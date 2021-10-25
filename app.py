from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from database import *
from pydantic_models import *
from fastapi.middleware.cors import CORSMiddleware

MAX_LEN_NAME_GAME = 10
MIN_LEN_NAME_GAME = 3
MAX_LEN_NAME_NICK = 10
MIN_LEN_NAME_NICK = 3

app = FastAPI(title="mystery")

origins = ["http://localhost:5000" "localhost:5000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# creating a game


@app.post("/creationgame")
async def game_creation(gametocreate: GameTemp, game_creator:str):
    """It creates an empty game with no players"""
    invalid_fields = HTTPException(status_code=404, detail="field size is invalid")
    if (
        len(gametocreate.game_name) > MAX_LEN_NAME_GAME
        or len(gametocreate.game_name) < MIN_LEN_NAME_GAME
    ):
        raise invalid_fields
    elif game_exist(gametocreate.game_name):
        raise HTTPException(status_code=404, detail="game exist")
    elif not user_exist(game_creator):
        raise HTTPException(status_code=404, detail="user does not exist")
    else:
        gametocreate.is_full = False
        gametocreate.is_started = False
        new_game(gametocreate.game_name)
        new_player_host(game_creator, gametocreate.game_name)
        insert_player(gametocreate.game_name, game_creator)
        add_player(gametocreate.game_name)
        return {"game": gametocreate.game_name}


# joining a game


@app.post("/joingame")
async def join_game(game_to_play: str, player_to_play: str):
    """It allows the user to join a match, as long as the match is not full or already ongoing"""
    if not game_exist(game_to_play):
        raise HTTPException(status_code=404, detail="game does not exist")
    elif is_full(game_to_play):
        raise HTTPException(status_code=404, detail="game is full")
    elif is_started(game_to_play):
        raise HTTPException(status_code=404, detail="game is not available")
    elif player_exist(player_to_play):
        raise HTTPException(status_code=404, detail="player in game")
    else:
        new_player(player_to_play, game_to_play)
        insert_player(game_to_play, player_to_play)
        add_player(game_to_play)
        return {"joining game": game_to_play}


# creating a nickname/user


@app.post("/creationuser")
async def user_creation(user_to_create: str):
    """It allows the player to set a nickname which will be displayed in game"""
    invalid_fields = HTTPException(status_code=404, detail="field size is invalid")
    if (
        len(user_to_create) > MAX_LEN_NAME_NICK
        or len(user_to_create) < MIN_LEN_NAME_NICK
    ):
        raise invalid_fields
    elif user_exist(user_to_create):
        raise HTTPException(status_code=404, detail="user exist")
    else:
        new_user(user_to_create)
        return {"user": user_to_create}


@app.get("/testfunction")
async def test(game_to_test: str):
    return {"num": get_number_player(game_to_test)}


@app.delete("/exitgame")
async def exitgame(player_to_exit: str, game_to_exit: str):
    if not player_exist(player_to_exit):
        raise HTTPException(status_code=404, detail="player does not exist")
    else:
        if get_number_player(game_to_exit) == 0:
            raise HTTPException(status_code=404, detail="game is empty")
        else:
            player_delete(player_to_exit)
            return {"exit game"}


# starting a game
@app.post("/start_game")
async def start_the_game(game_to_start: str):
    """it starts the game"""
    invalid_fields = HTTPException(status_code=404, detail="field size is invalid")
    if is_started(game_to_start):
        raise HTTPException(status_code=404, detail="game is already started")
    elif get_number_player(game_to_start) < 2:
        raise HTTPException(status_code=404, detail="not enoght players to start game")
    elif not game_exist(game_to_start):
        raise HTTPException(status_code=404, detail="game doesn't exist")
    else:
        start_game(game_to_start)
    return {"game started"}


# show games


@app.get("/show_available_games")
async def show_games():
    """It shows all games"""
    my_list = get_all_games()
    return my_list


# show player


@app.get("/show_players")
async def show_players():
    """It shows all players"""
    my_list = get_all_players()
    return my_list
