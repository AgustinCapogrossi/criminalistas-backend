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

origins = ["http://localhost:3000", "localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# creating a nickname/user


@app.post("/creationuser")
async def user_creation(user_to_create: str):
    """It creates a new user and allocates it in the database.

    Args: \n
        user_to_create (str): Name of the user we want to allocate in the database. \n

    Raises: \n
        invalid_fields: Arbitrary value for the maximum length of the name. \n
        HTTPException: The user already exists. \n

    Returns: \n
        str: Verification text.
    """
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


# creating a game


@app.post("/creationgame")
async def game_creation(gametocreate: GameTemp, game_creator: str):
    """It creates a new game and allocates it within the database.

    Args: \n
        gametocreate (GameTemp): Contains the necessary elements to create a game. \n
                                game_name: str \n
                                num_players: int \n
                                is_started: bool \n
                                is_full: bool \n
        game_creator (str): Name of the player who is creating the game.

    Raises: \n
        invalid_fields: Arbitrary value for the maximum length of the name. \n
        HTTPException: The game already exists. \n
        HTTPException: The user does not exist. \n
        HTTPException: The player is already in a game. \n

    Returns: \n
        str: Verification text.
    """
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
    elif player_exist(game_creator):
        raise HTTPException(status_code=404, detail="player in game")
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
async def join_game(game_to_play: str, user_to_play: str):
    """It turns an user into a player and allocates them within a game.

    Args: \n
        game_to_play (str): Name of the game we want the user to join. \n
        user_to_play (str): Name of the user to allocate into the game \n

    Raises: \n
        HTTPException: The game does not exist. \n
        HTTPException: The game is full. \n
        HTTPException: The game is not available. \n
        HTTPException: The user is already in the game. \n

    Returns: \n
        str: Verification text.
    """
    if not game_exist(game_to_play):
        raise HTTPException(status_code=404, detail="game does not exist")
    elif is_full(game_to_play):
        raise HTTPException(status_code=404, detail="game is full")
    elif is_started(game_to_play):
        raise HTTPException(status_code=404, detail="game is not available")
    elif player_exist(user_to_play):
        raise HTTPException(status_code=404, detail="player in game")
    else:
        new_player(user_to_play, game_to_play)
        insert_player(game_to_play, user_to_play)
        add_player(game_to_play)
        return {"joining game": game_to_play}


# exit game


@app.delete("/exitgame")
async def exitgame(player_to_exit: str, game_to_exit: str):
    """It allows a player to leave the game.

    Args: \n
        player_to_exit (str): Name of the player who is exiting the game. \n
        game_to_exit (str): Name of the game from which the player is exiting. \n

    Raises: \n
        HTTPException: The player does not exist. \n

    Returns: \n
        str: Verification text.
    """
    if not player_exist(player_to_exit):
        raise HTTPException(status_code=404, detail="player does not exist")
    else:
        player_delete(player_to_exit)
        return {"exit game"}


# starting a game


@app.post("/start_game")
async def start_the_game(game_to_start: str):
    """It switches the state of the selected game to started.

    Args: \n
        game_to_start (str): Name of the game of which we're switching it's state. \n

    Raises: \n
        HTTPException: The game is already started. \n
        HTTPException: There are not enough players to start the game. \n
        HTTPException: The game does not exist. \n

    Returns: \n
        str: Verification text.
    """
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
    """Returns the inner values of each game.

    Returns: \n
        my_list: A list which contains the inner values of each game. \n
    """
    my_list = get_all_games()
    return {my_list}


# start turn


@app.post("/start turn")
async def start_turn(player_name, game_name):
    """A function which starts the turn of the selected player in the selected game.

    Args: \n
        player_name (str): Name of the player whose turn we want to start. \n
        game_name (str): Name of the game in which the player is currently playing. \n

    Raises: \n
        HTTPException: The specified game is not started. \n
        HTTPException: The selected player's turn is ongoing. \n
        HTTPException: The selected player does not exist. \n
        HTTPException: The selected game does not exist. \n
    """
    if (
        player_exist(player_name)
        and game_exist(game_name)
        and not player_is_in_turn(player_name)
        and is_started(game_name)
    ):
        enable_turn_to_player(player_name)
    elif not is_started(game_name):
        raise HTTPException(status_code=404, detail="game has not started yet")
    elif player_is_in_turn(player_name):
        raise HTTPException(status_code=404, detail="player is already in turn")
    elif not player_exist(player_name):
        raise HTTPException(status_code=404, detail="player doesn't exist")
    elif not game_exist(game_name):
        raise HTTPException(status_code=404, detail="game doesn't exist")
    return {"Turn started"}


# end turn


@app.post("/end turn")
async def end_turn(player_name, game_name):
    """A function which ends the turn of the selected player in the selected game.

    Args: \n
        player_name (str): Name of the player whose turn we want to end. \n
        game_name (str): Name of the game in which the player is currently playing. \n

    Raises: \n
        HTTPException: The specified game is not started. \n
        HTTPException: The selected player's turn is not ongoing. \n
        HTTPException: The selected player does not exist. \n
        HTTPException: The selected game does not exist. \n

    Returns: \n
        str: Verification text.
    """
    if (
        player_exist(player_name)
        and game_exist(game_name)
        and player_is_in_turn(player_name)
        and is_started(game_name)
    ):
        disable_turn_to_player(player_name)
    elif not is_started(game_name):
        raise HTTPException(status_code=404, detail="game has not started yet")
    elif not player_is_in_turn(player_name):
        raise HTTPException(status_code=404, detail="player is already not in turn")
    elif not player_exist(player_name):
        raise HTTPException(status_code=404, detail="player doesn't exist")
    elif not game_exist(game_name):
        raise HTTPException(status_code=404, detail="game doesn't exist")


# gives a number to a player


@app.post("/dice_number")
async def dice_number(player_name, game_name):
    """The function generates a random dice number for the player.

    Args: \n
        player_name (str): Name of the player for whom we are generating a random number. \n
        game_name (str): Name of the game in which the player is currently playing. \n

    Raises: \n
        HTTPException: The selected player does not exist. \n

    Returns: \n
        str: Verification text.
    """
    if (
        player_exist(player_name)
        and game_exist(game_name)
        and is_started(game_name)
        and player_is_in_turn(player_name)
    ):
        random_number_dice(player_name)
        return {"number succesfully generated to player"}
    else:
        raise HTTPException(status_code=404, detail="player doesn't exist")


# show player


@app.get("/show_players")
async def show_players():
    """Returns the active players and their inner values.

    Returns: \n
        my_list: A list containing the active players and their inner values. \n
    """
    my_list = get_all_players()
    return my_list
