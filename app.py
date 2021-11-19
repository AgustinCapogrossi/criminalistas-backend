from fastapi import FastAPI, WebSocket
from fastapi import Depends, HTTPException, status
from typing import List
from fastapi.responses import HTMLResponse
from database import *
from pydantic_models import *
from fastapi.middleware.cors import CORSMiddleware

MAX_LEN_NAME_GAME = 10
MIN_LEN_NAME_GAME = 3
MAX_LEN_NAME_NICK = 10
MIN_LEN_NAME_NICK = 3


origins = ["http://localhost:3000", "localhost:3000"]
tags_metadata = [
    {"name": "User Methods", "description": "Gets all User Methods"},
    {"name": "Game Methods", "description": "Gets all Game Methods"},
    {"name": "Player Methods", "description": "Gets all PLayer Methods"},
    {"name": "Cards Methods", "description": "Gets all Cards Methods"},
]

app = FastAPI(openapi_tags=tags_metadata)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------------------------- WEBSOCKET -----------------------------------------
class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_text(data)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    while True:
        data = await websocket.receive_text()
        await manager.broadcast(f"Client {client_id}: {data}")

# ----------------------------------------- USER -----------------------------------------
# Creates a Nickname

@app.post("/user/creationuser", tags=["User Methods"], status_code=200)
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


# Deletes User


@app.delete("/user/delete_user", tags=["User Methods"])
async def user_delete(user_name: str):
    """Deletes an user.
    Args: \n
        user_name (str): Name of the user to delete. \n
    Raises: \n
        HTTPException: The user does not exist. \n
    Returns: \n
        str: Verification text.
    """
    if not user_exist(user_name):
        raise HTTPException(status_code=404, detail="user doesn't exist")
    elif player_exist(user_name):
        player_delete(user_name)
        delete_user(user_name)
        return {"player and user successfully deleted"}
    else:
        delete_user(user_name)
        return {"user successfully deleted"}


# ----------------------------------------- GAME -----------------------------------------

# Creates a Game
@app.post("/game/creationgame", tags=["Game Methods"])
async def game_creation(game_name: str, game_creator: str):
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


# Joins a Game


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
    elif not user_exist(user_to_play):
        raise HTTPException(status_code=404, detail="user does not exist")
    else:
        new_player(user_to_play, game_to_play)
        insert_player(game_to_play, user_to_play)
        add_player(game_to_play)
        return {"joining game": game_to_play}


# Exits a Game


@app.delete("/game/exitgame", tags=["Game Methods"])
async def exitgame(player_to_exit: str):
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
        order = get_player_order(player_to_exit)
        my_list = get_all_players()
        my_new_list = []
        game_id = get_player_game(player_to_exit)

        for i in range(0, len(my_list), 1):
            if my_list[i][4] == game_id:
                my_new_list.append(my_list[i])
        for i in range(order, len(my_new_list), 1):
            set_player_order(my_new_list[i][1], my_new_list[i][5] - 1)

        if order == len(my_new_list) - 1:
            order == -1

        if player_is_host(player_to_exit):
            for i in range(0, len(my_new_list), 1):
                if my_new_list[i][5] == order + 1:
                    player_set_host(my_new_list[i][1])
        if player_is_in_turn(player_to_exit):
            for i in range(0, len(my_new_list), 1):
                if my_new_list[i][5] == order + 1:
                    enable_turn_to_player(my_new_list[i][1])
        player_delete(player_to_exit)
        if get_number_player(get_game_name(game_id)) == 0:
            delete_game(get_game_name(game_id))

        return {"exit game"}


# Starts a Game


@app.post("/game/start_game", tags=["Game Methods"])
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
    if not game_exist(game_to_start):
        raise HTTPException(status_code=404, detail="game doesn't exist")
    elif get_number_player(game_to_start) < 2:
        raise HTTPException(status_code=404, detail="not enough players to start game")
    elif is_started(game_to_start):
        raise HTTPException(status_code=404, detail="game is already started")
    else:
        start_game(game_to_start)
        host_name = get_game_host(game_to_start)
        enable_turn_to_player(host_name)
        generate_cards(game_to_start)
    return {"game started"}


# Shows Games


@app.get("/game/show_available_games", tags=["Game Methods"])
async def show_games():
    """Returns the inner values of each game.
    Returns: \n
        my_list: A list which contains the inner values of each game. \n
    """
    my_list = get_all_games()
    return my_list


# Delete Game
@app.delete("/game/delete_game", tags=["Game Methods"])
async def delete_a_game(game_name: str):
    """Deletes an empty game.
    Args: \n
        game_name (str): Name of the game to delete. \n
    Raises: \n
        HTTPException: The game does not exist. \n
        HTTPException: The game has at least one player in it. \n
    Returns: \n
        str: Verification text.
    """
    if not game_exist(game_name):
        raise HTTPException(status_code=404, detail="game doesn't exist")
    elif get_number_player(game_name) > 0:
        raise HTTPException(status_code=404, detail="game has players in it")
    else:
        delete_game(game_name)
        return {"game successfully deleted"}


# ----------------------------------------- PLAYER -----------------------------------------

# Ends Turn


@app.post("/player/end turn", tags=["Player Methods"])
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
    if not game_exist(game_name):
        raise HTTPException(status_code=404, detail="game doesn't exist")
    elif not player_exist(player_name):
        raise HTTPException(status_code=404, detail="player doesn't exist")
    elif not is_started(game_name):
        raise HTTPException(status_code=404, detail="game has not started yet")
    elif not player_is_in_turn(player_name):
        raise HTTPException(status_code=404, detail="player is already not in turn")
    else:
        disable_turn_to_player(player_name)
        order = get_player_order(player_name)
        my_list = get_all_players()
        my_new_list = []
        game_id = get_game_id(game_name)
        for i in range(0, len(my_list), 1):
            if my_list[i][4] == game_id:
                my_new_list.append(my_list[i])
        if order == len(my_new_list) - 1:
            order = -1
        for i in range(0, len(my_new_list), 1):
            if my_new_list[i][5] == order + 1:
                enable_turn_to_player(my_new_list[i][1])


# Gives a number to a player


@app.post("/player/dice_number", tags=["Player Methods"])
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
        dice = random_number_dice(player_name)
    else:
        raise HTTPException(status_code=404, detail="game doesn't exist")
    return dice


# Shows Player


@app.get("/player/show_players", tags=["Player Methods"])
async def show_players(game_name):
    """Returns the active players and their inner values.
    Returns: \n
        my_list: A list containing the active players and their inner values. \n
    """

    if not game_exist(game_name):
        raise HTTPException(status_code=404, detail="game doesn't exist")
    else:
        my_list = get_all_players()
        my_new_list = []
        game_id = get_game_id(game_name)
        for i in range(0, len(my_list), 1):
            if my_list[i][4] == game_id:
                my_new_list.append(my_list[i])
        return my_new_list
      
@app.post("/cards/suspicion", tags=["Cards Methods"])
async def suspicion(player_who_suspects, monster_card, victim_card, room_card):
    if not player_is_in_turn(player_who_suspects):
        raise HTTPException(status_code=404, detail="player is not in turn")
    if not card_monster_exist(monster_card):
        raise HTTPException(status_code=404, detail="monster card doesn't exist")
    elif not card_room_exist(room_card):
        raise HTTPException(status_code=404, detail="room card doesn't exist")
    elif not card_victims_exist(victim_card):
        raise HTTPException(status_code=404, detail="victim card doesn't exist")
    else:
        return suspect(player_who_suspects, monster_card, victim_card, room_card)


@app.post("/player/set_position_and_piece", tags=["Player Methods"])
async def set_piece_position(player_name):
    """Set piece and position of the player in the game.


    Args: \n
        player_name (str): Name of the player for whom we are generating the piece and position. \n

    Raises: \n
        HTTPException: The player does not exist. \n
        
    Returns: \n
        str: Verification text.
    """
    if player_exist(player_name):
        player_position_and_piece(player_name)
        return {"position and piece generated"}
    elif not player_exist(player_name):
        raise HTTPException(status_code=404, detail="player doesn't exist")


@app.post("/player/move", tags=["Player Methods"])
async def moving_player(player_name: str, direction: str):
    """Moves the player in the indicated position.

    Args: \n
        player_name (str): Name of the player we want to move. \n
        direction (str): Direction of the movement.\n

    Raises: \n
        HTTPException: The player does not exist. \n
        HTTPException: AWSD keys were not entered.\n
        HTTPException: The player doesn't have any moves left.\n
        
    Returns: \n
        str: Verification text.
    """
    if get_player_dice(player_name) >= 1:
        if player_exist(player_name) and (
            direction == "W"
            or direction == "w"
            or direction == "S"
            or direction == "s"
            or direction == "A"
            or direction == "a"
            or direction == "D"
            or direction == "d"
        ):
            move_player(player_name, direction)
        elif not player_exist(player_name):
            raise HTTPException(status_code=404, detail="player doesn't exist")
        elif not (
            direction == "W"
            or direction == "w"
            or direction == "S"
            or direction == "s"
            or direction == "A"
            or direction == "a"
            or direction == "D"
            or direction == "d"
        ):
            raise HTTPException(status_code=404, detail="error, use just AWSD keys")
    else:
        raise HTTPException(
            status_code=404, detail="player doesn't have any moves left"
        )


# ----------------------------------------- CARDS -----------------------------------------

# Generate Envelope


@app.post("/cards/envelope", tags=["Cards Methods"])
async def select_envelope(game_name):
    """Selects The Moster, Victim and Room that will go in the envelope
    Args: \n
        select_envelope (str): Name of the game to select the cards. \n
    Returns: \n
        str: Verification text.
    """

    if not game_exist(game_name):
        raise HTTPException(status_code=404, detail="game doesn't exist")
    else:
        envelope(game_name)
    return {"Monster, Victim and Room Successfully selected."}


# Distribute Cards


@app.post("/cards/distribute_cards", tags=["Cards Methods"])
async def distribute_cards(a_game: str):
    if not game_exist(a_game):
        raise HTTPException(status_code=404, detail="game doesn't exist")
    else:
        player_with_monsters(a_game)
        player_with_rooms(a_game)
        player_with_victims(a_game)
        
    return {"cards distributes"}

