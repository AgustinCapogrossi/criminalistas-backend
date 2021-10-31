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


tags_metadata = [
    {"name": "User Methods", "description": "Gets all User Methods"},
    {"name": "Game Methods", "description": "Gets all Game Methods"},
    {"name": "Turn Methods", "description": "Gets all Turn Methods"},
    {"name": "Player Methods", "description": "Gets all PLayer Methods"},
]

app = FastAPI(openapi_tags=tags_metadata)


# creating a nickname/user


@app.post("/user/creationuser", tags= ["User Methods"])

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


@app.post("/game/creationgame" , tags=["Game Methods"])
async def game_creation(
    game_name: str, num_players: str, is_started: bool, is_full: bool, game_creator: str
):
    """It creates a new game and allocates it within the database.\n

    Args: \n
        game_name (str): Name of the player. \n
        num_players (str): Number of players in the game. \n
        is_started (bool): Whether the game is started or not. \n
        is_full (bool): Whether the game is full or not. \n
        game_creator (str): Name of the creator of the game \n

    Raises: \n
        invalid_fields: Arbitrary value for the maximum length of the name. \n
        HTTPException: The game already exists. \n
        HTTPException: The user does not exist. \n
        HTTPException: The player is already in a game. \n

    Returns: \n
        str: Verification text.
    """

    invalid_fields = HTTPException(status_code=404, detail="field size is invalid")
    if len(game_name) > MAX_LEN_NAME_GAME or len(game_name) < MIN_LEN_NAME_GAME:
        raise invalid_fields
    elif game_exist(game_name):
        raise HTTPException(status_code=404, detail="game exist")
    elif not user_exist(game_creator):
        raise HTTPException(status_code=404, detail="user does not exist")
    elif player_exist(game_creator):
        raise HTTPException(status_code=404, detail="player in game")
    else:
        is_full = False
        is_started = False

        new_game(game_name, game_creator)
        new_player_host(game_creator, game_name)
        insert_player(game_name, game_creator)
        add_player(game_name)
        return {"game": game_name}


# joining a game


@app.post("/game/joingame", tags=["Game Methods"])

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
        HTTPException: The user does not exist. \n

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
        raise HTTPException(status_code=404, detail="user in game")
    elif not user_exist(user_to_play):
        raise HTTPException(status_code=404, detail="user does not exist")
    else:
        new_player(user_to_play, game_to_play)
        insert_player(game_to_play, user_to_play)
        add_player(game_to_play)
        return {"joining game": game_to_play}


# exit game



@app.delete("/player/exitgame" , tags=["Player Methods"])
async def exitgame(player_to_exit: str):
    """It allows a player to leave the game.

    Args: \n
        player_to_exit (str): Name of the player who is exiting the game. \n
        
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



@app.post("/game/start_game" , tags=["Game Methods"])

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


@app.get("/game/show_available_games", tags=["Game Methods"])
async def show_games():
    """Returns the inner values of each game.

    Returns: \n
        my_list: A list which contains the inner values of each game. \n
    """
    my_list = get_all_games()
    return my_list


# start turn


@app.post("/turn/start turn" , tags=["Turn Methods"])

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



@app.post("/turn/end turn" , tags=["Turn Methods"])
=======

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


@app.post("/player/dice_number", tags=["Player Methods"])
async def dice_number(player_name, game_name):
    """The function generates a random dice number for the player.

    Args: \n
        player_name (str): Name of the player for whom we are generating a random number. \n
        game_name (str): Name of the game in which the player is currently playing. \n

    Raises: \n
        HTTPException: The selected player does not exist. \n

        HTTPException: The selected game does not exist. \n
        HTTPException: The selected game is not started. \n
        HTTPException: The selected player isn't in turn. \n

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
    elif(not player_exist(player_name)):
        raise HTTPException(status_code=404, detail="player doesn't exist")
    elif(not game_exist(game_name)):
        raise HTTPException(status_code=404, detail="game doesn't exist")
    elif(not is_started(game_name)):
        raise HTTPException(status_code=404, detail="game is not started")
    elif(is_started(game_name) and not player_is_in_turn(game_name)):
        raise HTTPException(status_code=404, detail="player isn't in turn")


# show player


@app.get("/player/show_players", tags=["Player Methods"])
async def show_players():
    """Returns the active players and their inner values.

    Returns: \n
        my_list: A list containing the active players and their inner values. \n
    """
    my_list = get_all_players()
    my_new_list = []
    game_id = get_game_id(game_name)
    for i in range(0, len(my_list), 1):
        if my_list[i][4] == game_id:
            my_new_list.append(my_list[i])
    return my_new_list, game_id
  
  
# Delete Game


@app.delete("/game/delete_game", tags=["Game Methods"])
async def delete_a_game(game_name : str):
    """Deletes an empty game.
    
    Args: \n
        game_name (str): Name of the game to delete. \n

    Raises: \n
        HTTPException: The game does not exist. \n
        HTTPException: The game has at least one player in it. \n

    Returns: \n
        str: Verification text.
    """
    if (not game_exist(game_name)):
        raise HTTPException(status_code=404, detail="game doesn't exist")
    elif (get_number_player(game_name)>0):
        raise HTTPException(status_code=404, detail="game has players in it")
    else:
        game_delete(game_name)
        return{"game successfully deleted"}
    
# Delete User

@app.delete("/user/delete_user", tags=["User Methods"])
async def user_delete(user_name : str):
    """Deletes an user.
    
    Args: \n
        user_name (str): Name of the user to delete. \n

    Raises: \n
        HTTPException: The user does not exist. \n

    Returns: \n
        str: Verification text.
    """
    if(not user_exist(user_name)):
        raise HTTPException(status_code=404, detail="user doesn't exist")
    elif (player_exist(user_name)):
        player_delete(user_name)
        delete_user(user_name)
        return{"player and user successfully deleted"}
    else:
        delete_user(user_name)
        return{"user successfully deleted"}
    
#Generate Cards

@app.post("/game/generate_cards", tags= ["Game Methods"])
async def cards_generator(game):
    """Generate the game cards.
    
    Args: \n
        cards_generator (str): Name of the game to generate cards. \n

    Returns: \n
        str: Verification text.
    """
    generate_cards(game)
    return{"Cards Successfully generated for the game"}
