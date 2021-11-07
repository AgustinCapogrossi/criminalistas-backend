from pony.orm import *
import sqlite3
import random

db = pony.orm.Database()


db.bind(provider="sqlite", filename="db.mystery", create_db=True)

# Games table and Functions
class User(db.Entity):
    username = pony.orm.Required(str, unique=True)
    player = Optional("Player")


# Player Table
class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    host = Optional(bool)
    user = Required(User)
    game = Required("Game")
    order = Required(int)
    dice_number = Required(int)
    turn = Required(bool)
    cards_monsters = Set("Cards_Monsters")
    cards_rooms = Set("Cards_Rooms")
    cards_victims = Set("Cards_Victims")


# Game Table
class Game(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    host_name = Required(str)
    is_started = Required(bool)
    is_full = Required(bool)
    num_players = Required(int)
    Players = Set("Player", cascade_delete=True)
    cards_monsters = Set("Cards_Monsters", cascade_delete=True)
    cards_rooms = Set("Cards_Rooms", cascade_delete=True)
    cards_victims = Set("Cards_Victims", cascade_delete=True)


# Game Cards
class Cards_Monsters(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    is_in_use = Required(bool)
    is_in_envelope = Required(bool)
    game = Optional("Game")
    player = Optional(Player)

class Cards_Victims(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    is_in_use = Required(bool)
    is_in_envelope = Required(bool)
    game = Optional("Game")
    player = Optional(Player)

class Cards_Rooms(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    is_in_use = Required(bool)
    is_in_envelope = Required(bool)
    game = Optional("Game")
    player = Optional(Player)


db.generate_mapping(create_tables=True)

# ----------------------------------------- GAME -----------------------------------------
@db_session
def new_game(new_name, creator):
    Game(
        name=new_name, host_name=creator, is_started=False, is_full=False, num_players=0
    )


@db_session
def game_exist(un_name):
    if Game.get(name=un_name) is not None:
        return True


@db_session
def game_exist(game):
    if Game.get(name=game) is not None:
        return True


@db_session
def get_number_player(a_game: str):
    return Game.get(name=a_game).num_players


@db_session
def is_full(the_game):
    if get_number_player(the_game) == 6:
        return True


@db_session
def is_started(a_name):
    return Game.get(name=a_name).is_started


@db_session
def add_player(a_game):
    game = get_game(a_game)
    sum_players = get_number_player(a_game) + 1
    game.set(num_players=sum_players)


@db_session
def get_game(a_game):
    return Game.get(name=a_game)


@db_session
def get_game_id(a_game):
    return Game.get(name=a_game).id


@db_session
def get_game_name(game_id):
    return Game.get(id=game_id).name


@db_session
def get_game_host(a_game):
    return Game.get(name=a_game).host_name


@db_session
def get_all_games():
    try:
        conn = sqlite3.connect("db.mystery")
        cursor = conn.cursor()
        print("\n")
        select_games = """SELECT * from Game"""
        cursor.execute(select_games)
        records = cursor.fetchall()
        gamesList = []
        for row in records:
            print("id: ", row[0])
            print("name: ", row[1])
            print("name: ", row[2])
            print("is_started: ", row[3])
            print("is_full: ", row[4])
            print("num_players: ", row[5])
            print("\n")
            games = [row[0], row[1], row[2], row[3], row[4], row[5]]
            gamesList.append(games)
            cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()
    return gamesList


@db_session
def start_game(game):
    my_game = get_game(game)
    my_game.set(is_started=True)


@db_session
def delete_game(game_name):
    game = get_game(game_name)
    Game.delete(game)


# ----------------------------------------- USER -----------------------------------------


@db_session
def new_user(new_name):
    User(username=new_name)


@db_session
def user_exist(a_name):
    if User.get(username=a_name) is not None:
        return True


@db_session
def get_user(a_user):
    return User.get(username=a_user)


@db_session
def delete_user(user_name):
    user = get_user(user_name)
    User.delete(user)


# ----------------------------------------- PLAYER -----------------------------------------


@db_session
def new_player(name_player, name_game):
    Player(
        name=name_player,
        host=False,
        order=get_number_player(name_game),
        user=get_user(name_player),
        game=get_game(name_game),
        dice_number=0,
        turn=False,
    )


@db_session
def new_player_host(name_player, name_game):
    Player(
        name=name_player,
        host=True,
        order=0,
        user=get_user(name_player),
        game=get_game(name_game),
        dice_number=0,
        turn=False,
    )


@db_session
def player_delete(un_player):
    player = Player.get(name=un_player)
    curgame = player.game
    curgame.set(num_players=get_number_player(curgame.name) - 1)
    Player.delete(player)


@db_session
def player_exist(un_player):
    if Player.get(name=un_player) is not None:
        return True


@db_session
def get_all_players():
    try:
        conn = sqlite3.connect("db.mystery")
        cursor = conn.cursor()
        print("\n")
        select_player = """SELECT * from Player"""
        cursor.execute(select_player)
        records = cursor.fetchall()
        playerList = []
        for row in records:
            print("id: ", row[0])
            print("name: ", row[1])
            print("host: ", row[2])
            print("user: ", row[3])
            print("game: ", row[4])
            print("order: ", row[5])
            print("dice number: ", row[6])
            print("turn: ", row[7])
            print("\n")
            player = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]
            playerList.append(player)
            cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()
    return playerList


@db_session
def get_player_order(player):
    return Player.get(name=player).order


@db_session
def set_player_order(player, new_order):
    my_player = Player.get(name=player)
    my_player.set(order=new_order)


@db_session
def player_is_host(player):
    return Player.get(name=player).host


@db_session
def player_set_host(player):
    my_player = Player.get(name=player)
    my_player.set(host=True)
    my_player.game.set(host_name=player)


@db_session
def get_player_game(un_player):
    player = Player.get(name=un_player)
    return player.game.id


@db_session
def random_number_dice(player):
    myPlayer = Player.get(name=player)
    myPlayer.set(dice_number=random.randint(1, 6))


@db_session
def dice_to_zero(player):
    myPlayer = Player.get(name=player)
    myPlayer.set(dice_number=0)


@db_session
def enable_turn_to_player(player):
    myPlayer = Player.get(name=player)
    myPlayer.set(turn=True)


@db_session
def disable_turn_to_player(player):
    myPlayer = Player.get(name=player)
    myPlayer.set(turn=False)


@db_session
def player_is_in_turn(player):
    myPlayer = Player.get(name=player)
    return myPlayer.turn


@db_session
def insert_player(un_game, un_player):
    player = Player.get(name=un_player)
    game = get_game(un_game)
    game.Players.add(player)


# ----------------------------------------- CARDS -----------------------------------------

# Generate Cards


@db_session
def generate_cards(game_name):
    cards_monster = [
        "Dŕacula",
        "Frankenstein",
        "Hombre Lobo",
        "Fantasma",
        "Momia",
        "Dr Jekyll Mr. Hyde",
    ]
    cards_victims = [
        "Conde",
        "Condesa",
        "Ama de Llaves",
        "Mayordomo",
        "Doncella",
        "Jardinero",
    ]
    cards_rooms = [
        "Cochera",
        "Alcoba",
        "Biblioteca",
        "Panteón",
        "Vestíbulo",
        "Bodega",
        "Salón",
        "Laboratorio",
    ]

    p = 0
    for p in range(len(cards_monster)):
        card_name = cards_monster[p]
        Cards_Monsters(
            name=card_name,
            game=get_game(game_name),
            is_in_use=False,
            is_in_envelope=False,
            game=get_game(game_name)
        )

    p = 0
    for p in range(len(cards_victims)):
        card_name = cards_victims[p]
        Cards_Victims(
            name=card_name,
            game=get_game(game_name),
            is_in_use=False,
            is_in_envelope=False,
            game=get_game(game_name)
        )

    p = 0
    for p in range(len(cards_rooms)):
        card_name = cards_rooms[p]
        Cards_Rooms(
            name=card_name,
            game=get_game(game_name),
            is_in_use=False,
            is_in_envelope=False,
            game = get_game(game_name)
        )


@db_session
def envelope(game):
    mygameId = get_game(game).id
    try:
        conn = sqlite3.connect("db.mystery")
        cursor = conn.cursor()
        print("\n")
        select_cards = (
            """UPDATE Cards_Monsters SET is_in_envelope=true WHERE game = %d ORDER BY RANDOM() LIMIT 1"""
            % mygameId
        )
        cursor.execute(select_cards)
        select_cards = (
            """UPDATE Cards_Victims SET is_in_envelope=true WHERE game = %d ORDER BY RANDOM() LIMIT 1"""
            % mygameId
        )
        cursor.execute(select_cards)
        select_cards = (
            """UPDATE Cards_Rooms SET is_in_envelope=true WHERE game = %d ORDER BY RANDOM() LIMIT 1"""
            % mygameId
        )
        cursor.execute(select_cards)
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()


@db_session
def get_card_monster(id_card):
    return Cards_Monsters.get(id=id_card)


@db_session
def player_delete(un_player):
    player = Player.get(name=un_player)
    curgame = player.game
    curgame.set(num_players=get_number_player(curgame.name) - 1)
    Player.delete(player)


@db_session
def get_card_room(id_card):
    return Cards_Rooms.get(id=id_card)


@db_session
def get_card_victims(id_card):
    return Cards_Victims.get(id=id_card)


@db_session
def get_card_game(card):
    return Cards_Monsters.get(name=card).game

@db_session
def get_player_random(game):
    game_id = get_game_id(game)
    try:
        conn = sqlite3.connect("db.mystery")
        cursor = conn.cursor()
        player_random = ("SELECT id from Player WHERE `game` = %d ORDER BY RANDOM() LIMIT 1" % game_id)
        cursor.execute(player_random)
        records = cursor.fetchall()
        id_player = records[0]
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()
    return id_player

@db_session
def player_with_monsters(a_game):
    num_player = get_number_player(a_game)
    game_id = get_game_id(a_game)
    try:
        conn = sqlite3.connect("db.mystery")
        cursor = conn.cursor()
        print("\n")
        select_card = ("""SELECT * from Cards_Monsters WHERE `game` = %d""" % game_id)
        cursor.execute(select_card)
        records = cursor.fetchall()
        for row in records:
            id_card = row[0]
            game = row[4]
            value = row[3]
            if (get_game_id(a_game) == game) and (value == 0):
                player_random = get_player_random(a_game)
                card = get_card_monster(id_card)
                card.set(player=player_random)
                card.set(is_in_use=True)
                cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()


@db_session
def player_with_rooms(a_game):
    num_player = get_number_player(a_game)
    game_id = get_game_id(a_game)
    try:
        conn = sqlite3.connect("db.mystery")
        cursor = conn.cursor()
        print("\n")
        select_card = ("""SELECT * from Cards_Rooms WHERE `game` = %d """ % game_id)
        cursor.execute(select_card)
        records = cursor.fetchall()
        for row in records:
            id_card = row[0]
            game = row[4]
            value = row[3]
            if (get_game_id(a_game) == game) and (value == 0):
                player_random = get_player_random(a_game)
                card = get_card_room(id_card)
                card.set(player=player_random)
                card.set(is_in_use=True)
                cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()


@db_session
def player_with_victims(a_game):
    num_player = get_number_player(a_game)
    game_id = get_game_id(a_game)
    try:
        conn = sqlite3.connect("db.mystery")
        cursor = conn.cursor()
        print("\n")
        select_card = ("""SELECT * from Cards_Victims WHERE `game` = %d """ % game_id)
        cursor.execute(select_card)
        records = cursor.fetchall()
        for row in records:
            id_card = row[0]
            game = row[4]
            value = row[3]
            if (get_game_id(a_game) == game) and (value == 0):
                player_random = get_player_random(a_game)
                card = get_card_victims(id_card)
                card.set(player=player_random)
                card.set(is_in_use=True)
                cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()
