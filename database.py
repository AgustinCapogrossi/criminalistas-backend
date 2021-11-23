from sys import platform
from pony.orm import *
import sqlite3
import random

from pony.thirdparty.compiler.ast import For

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
    piece = Optional(str)
    player_x = Optional(int)
    player_y = Optional(int)
    is_winner = Optional(bool)
    is_loser = Optional(bool)


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
        is_winner=False,
        is_loser=False,
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
        is_winner=False,
        is_loser=False,
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
def player_in_game(game, player):
    if get_game_id(game) == get_player_game(player):
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
def get_all_players_from_game(game):
    game_id = get_game_id(game)
    try:
        conn = sqlite3.connect("db.mystery")
        cursor = conn.cursor()
        players_game = "SELECT * from Player WHERE `game` = %d" % game_id
        cursor.execute(players_game)
        records = cursor.fetchall()
        playerList = []
        for row in records:
            player = [
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8],
                row[9],
                row[10],
                row[11],
                row[12],
            ]
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
def get_player(player):
    return Player.get(name=player).name


@db_session
def get_my_player(player):
    return Player.get(name=player)


@db_session
def player_is_host(player):
    return Player.get(name=player).host


@db_session
def player_set_host(player):
    my_player = Player.get(name=player)
    my_player.set(host=True)
    my_player.game.set(host_name=player)


@db_session
def get_player_id(player):
    return Player.get(name=player).id


@db_session
def get_player_thegame(player):
    return Player.get(name=player).game


@db_session
def get_player_game(un_player):
    player = Player.get(name=un_player)
    return player.game.id


@db_session
def get_player_game_name(un_player):
    player = Player.get(name=un_player)
    return player.game.name


@db_session
def random_number_dice(player):
    myPlayer = Player.get(name=player)
    myPlayer.set(dice_number=random.randint(1, 6))
    return myPlayer.dice_number


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


@db_session
def get_player_dice(player):
    return Player.get(name=player).dice_number


@db_session
def get_next_player_order(un_player):
    order = get_player_order(un_player)
    my_list = get_all_players()
    my_new_list = []
    game_id = get_player_game(un_player)
    for i in range(0, len(my_list), 1):
        if my_list[i][4] == game_id:
            my_new_list.append(my_list[i])
    if order == len(my_new_list) - 1:
        order == -1
    for i in range(0, len(my_new_list), 1):
        if my_new_list[i][5] == order + 1:
            next_order = get_player_order(my_new_list[i][1])
    return next_order


@db_session
def get_next_player_id(un_player):
    order = get_player_order(un_player)
    my_list = get_all_players()
    my_new_list = []
    game_id = get_player_game(un_player)
    for i in range(0, len(my_list), 1):
        if my_list[i][4] == game_id:
            my_new_list.append(my_list[i])
    if order == len(my_new_list) - 1:
        order == -1
    for i in range(0, len(my_new_list), 1):
        if my_new_list[i][5] == order + 1:
            next_id = get_player_id(my_new_list[i][1])
    return next_id


@db_session
def get_next_player_name(un_player):
    order = get_player_order(un_player)
    my_list = get_all_players()
    my_new_list = []
    game_id = get_player_game(un_player)
    for i in range(0, len(my_list), 1):
        if my_list[i][4] == game_id:
            my_new_list.append(my_list[i])
    if order == len(my_new_list) - 1:
        order == -1
    for i in range(0, len(my_new_list), 1):
        if my_new_list[i][5] == order + 1:
            next_name = get_player(my_new_list[i][1])
    return next_name


@db_session
def player_is_winner(player_name):
    return Player.get(name=player_name).is_winner


# ----------------------------------------- CARDS -----------------------------------------

# Generate Cards


@db_session
def generate_cards(game_name):
    cards_monster = [
        "Drácula",
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
        )

    p = 0
    for p in range(len(cards_victims)):
        card_name = cards_victims[p]
        Cards_Victims(
            name=card_name,
            game=get_game(game_name),
            is_in_use=False,
            is_in_envelope=False,
        )

    p = 0
    for p in range(len(cards_rooms)):
        card_name = cards_rooms[p]
        Cards_Rooms(
            name=card_name,
            game=get_game(game_name),
            is_in_use=False,
            is_in_envelope=False,
        )


# Generate envelope


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


# -------------------------Returns card ID------------------------#

# me obtiene todas las cartas monster de un juego especifico
@db_session
def get_monster_id(card, gameId):
    card_list = get_monster_card()
    new_card_list = []
    for i in range(0, len(card_list), 1):
        if card_list[i][4] == gameId:
            new_card_list.append(card_list[i])
    for i in range(0, len(new_card_list), 1):
        if new_card_list[i][1] == str(card):
            return new_card_list[i][0]


@db_session
def get_victim_id(card, gameId):
    card_list = get_victim_card()
    new_card_list = []
    for i in range(0, len(card_list), 1):
        if card_list[i][4] == gameId:
            new_card_list.append(card_list[i])
    for i in range(0, len(new_card_list), 1):
        if new_card_list[i][1] == str(card):
            return new_card_list[i][0]


@db_session
def get_room_id(card, gameId):
    card_list = get_room_card()
    new_card_list = []
    for i in range(0, len(card_list), 1):
        if card_list[i][4] == gameId:
            new_card_list.append(card_list[i])
    for i in range(0, len(new_card_list), 1):
        if new_card_list[i][1] == str(card):
            return new_card_list[i][0]


# ----------------------------------------------------------------#


@db_session
def get_card_monster(id_card):
    return Cards_Monsters.get(id=id_card)


@db_session
def get_card_room(id_card):
    return Cards_Rooms.get(id=id_card)


@db_session
def get_card_victims(id_card):
    return Cards_Victims.get(id=id_card)


# ----------------------------------------------------------------#
# ---------------------------Card exists--------------------------#


@db_session
def card_monster_exist(card):
    if (
        str(card) == "Drácula"
        or str(card) == "Frankenstein"
        or str(card) == "Hombre Lobo"
        or str(card) == "Fantasma"
        or str(card) == "Momia"
        or str(card) == "Dr Jekyll Mr. Hyde"
    ):
        return True


@db_session
def card_victims_exist(card):
    if (
        str(card) == "Conde"
        or str(card) == "Condesa"
        or str(card) == "Ama de Llaves"
        or str(card) == "Mayordomo"
        or str(card) == "Doncella"
        or str(card) == "Jardinero"
    ):
        return True


@db_session
def card_room_exist(card):
    if (
        str(card) == "Cochera"
        or str(card) == "Alcoba"
        or str(card) == "Biblioteca"
        or str(card) == "Panteón"
        or str(card) == "Vestíbulo"
        or str(card) == "Bodega"
        or str(card) == "Salón"
        or str(card) == "Laboratorio"
    ):
        return True


# ----------------------------------------------------------------#
# ---------------------------Card game----------------------------#


@db_session
def get_monster_game(card):
    return Cards_Monsters.get(name=card).game


@db_session
def get_victim_game(card):
    return Cards_Victims.get(name=card).game


@db_session
def get_room_game(card):
    return Cards_Rooms.get(name=card).game


# ----------------------------------------------------------------#
# -------------------------Card Player----------------------------#


@db_session
def get_monster_player_id(card):
    return Cards_Monsters.get(name=card).player.id


@db_session
def get_victim_player_id(card):
    return Cards_Victims.get(name=card).player.id


@db_session
def get_room_player_id(card):
    return Cards_Rooms.get(name=card).player.id


# ----------------------------------------------------------------#


@db_session
def get_players(game):
    game_id = get_game_id(game)
    try:
        conn = sqlite3.connect("db.mystery")
        cursor = conn.cursor()
        player_random = "SELECT id from Player WHERE `game` = %d" % game_id
        cursor.execute(player_random)
        records = cursor.fetchall()
        playerList = []
        for row in records:
            player = row[0]
            playerList.append(player)
            cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()
    return playerList


# ----------------------------------------------------------------#
# -------------------------Player Card----------------------------#


@db_session
def player_with_monsters(a_game):
    game_id = get_game_id(a_game)
    players = get_players(a_game)
    try:
        conn = sqlite3.connect("db.mystery")
        cursor = conn.cursor()
        print("\n")
        select_card = """SELECT * from Cards_Monsters WHERE `game` = %d""" % game_id
        cursor.execute(select_card)
        records = cursor.fetchall()
        pl = 0
        for row in records:
            id_card = row[0]
            game = row[4]
            value = row[3]
            while True:
                a_player = players[pl]
                if (get_game_id(a_game) == game) and (value == 0):
                    card = get_card_monster(id_card)
                    card.set(player=a_player)
                    card.set(is_in_use=True)
                    cursor.close()
                pl = pl + 1
                if pl == len(players):
                    pl = 0
                    break
                break
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()


@db_session
def player_with_rooms(a_game):
    game_id = get_game_id(a_game)
    players = get_players(a_game)
    try:
        conn = sqlite3.connect("db.mystery")
        cursor = conn.cursor()
        print("\n")
        select_card = """SELECT * from Cards_Rooms WHERE `game` = %d """ % game_id
        cursor.execute(select_card)
        records = cursor.fetchall()
        pl = 0
        for row in records:
            id_card = row[0]
            game = row[4]
            value = row[3]
            while True:
                a_player = players[pl]
                print(a_player)
                if (get_game_id(a_game) == game) and (value == 0):
                    card = get_card_room(id_card)
                    card.set(player=a_player)
                    card.set(is_in_use=True)
                    cursor.close()
                pl = pl + 1
                if pl == len(players):
                    pl = 0
                    break
                break
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()


@db_session
def player_with_victims(a_game):
    game_id = get_game_id(a_game)
    players = get_players(a_game)
    try:
        conn = sqlite3.connect("db.mystery")
        cursor = conn.cursor()
        print("\n")
        select_card = """SELECT * from Cards_Victims WHERE `game` = %d """ % game_id
        cursor.execute(select_card)
        records = cursor.fetchall()
        pl = 0
        for row in records:
            id_card = row[0]
            game = row[4]
            value = row[3]
            while True:
                a_player = players[pl]
                if (get_game_id(a_game) == game) and (value == 0):
                    card = get_card_victims(id_card)
                    card.set(player=a_player)
                    card.set(is_in_use=True)
                    cursor.close()
                pl = pl + 1
                if pl == len(players):
                    pl = 0
                    break
                break
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()


# ----------------------------------------------------------------#
# -------------------------Show Cards-----------------------------#


@db_session
def get_monster_card():
    try:
        conn = sqlite3.connect("db.mystery")
        cursor = conn.cursor()
        print("\n")
        select_card = """SELECT * from Cards_Monsters"""
        cursor.execute(select_card)
        records = cursor.fetchall()
        cardList = []
        for row in records:
            print("id: ", row[0])
            print("name: ", row[1])
            print("is_in_use: ", row[2])
            print("is_in_envelope: ", row[3])
            print("game: ", row[4])
            print("player: ", row[5])
            print("\n")
            card = [row[0], row[1], row[2], row[3], row[4], row[5]]
            cardList.append(card)
            cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()
    return cardList


@db_session
def get_victim_card():
    try:
        conn = sqlite3.connect("db.mystery")
        cursor = conn.cursor()
        print("\n")
        select_card = """SELECT * from Cards_Victims"""
        cursor.execute(select_card)
        records = cursor.fetchall()
        cardList = []
        for row in records:
            print("id: ", row[0])
            print("name: ", row[1])
            print("is_in_use: ", row[2])
            print("is_in_envelope: ", row[3])
            print("game: ", row[4])
            print("player: ", row[5])
            print("\n")
            card = [row[0], row[1], row[2], row[3], row[4], row[5]]
            cardList.append(card)
            cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()
    return cardList


@db_session
def get_room_card():
    try:
        conn = sqlite3.connect("db.mystery")
        cursor = conn.cursor()
        print("\n")
        select_card = """SELECT * from Cards_Rooms"""
        cursor.execute(select_card)
        records = cursor.fetchall()
        cardList = []
        for row in records:
            print("id: ", row[0])
            print("name: ", row[1])
            print("is_in_use: ", row[2])
            print("is_in_envelope: ", row[3])
            print("game: ", row[4])
            print("player: ", row[5])
            print("\n")
            card = [row[0], row[1], row[2], row[3], row[4], row[5]]
            cardList.append(card)
            cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()
    return cardList


# ----------------------------------------------------------------#
# ---------------------Card in envelope---------------------------#


@db_session
def get_monster_card_envelope(gameId):
    card_list = get_monster_card()
    new_card_list = []
    # Returns cards from game#
    for i in range(0, len(card_list), 1):
        if card_list[i][4] == gameId:
            new_card_list.append(card_list[i])
    # Returns card in envelope#
    for i in range(0, len(new_card_list), 1):
        if new_card_list[i][3] == 1:
            return new_card_list[i]


@db_session
def get_victim_card_envelope(gameId):
    card_list = get_victim_card()
    new_card_list = []
    # Returns cards from game#
    for i in range(0, len(card_list), 1):
        if card_list[i][4] == gameId:
            new_card_list.append(card_list[i])
    # Returns card in envelope#
    for i in range(0, len(new_card_list), 1):
        if new_card_list[i][3] == 1:
            return new_card_list[i]


@db_session
def get_room_card_envelope(gameId):
    card_list = get_room_card()
    new_card_list = []
    # Returns cards from game#
    for i in range(0, len(card_list), 1):
        if card_list[i][4] == gameId:
            new_card_list.append(card_list[i])
    # Returns card in envelope#
    for i in range(0, len(new_card_list), 1):
        if new_card_list[i][3] == 1:
            return new_card_list[i]


# ----------------------------------------------------------------#


# Suspects
@db_session
def suspect(player_who_suspects, monster_card, victim_card, room_card):
    # Comparar los id, contar similitudes, cambiar los valores de booleans

    # Conseguir el id de las cartas dadas por el jugador
    # *********************************************#
    game = get_player_game_name(player_who_suspects)
    game_id = get_player_game(player_who_suspects)
    monster_id = get_monster_id(monster_card, game_id)
    victim_id = get_victim_id(victim_card, game_id)
    room_id = get_room_id(room_card, game_id)
    # *********************************************#

    # Conseguir todas las cartas en juego de la partida
    # *********************************************#
    list_monster_cards = get_monster_card()
    list_victim_cards = get_victim_card()
    list_room_cards = get_room_card()

    new_list_monster_cards = []
    new_list_victim_cards = []
    new_list_room_cards = []

    for i in range(0, len(list_monster_cards), 1):
        if list_monster_cards[i][4] == game_id:
            new_list_monster_cards.append(list_monster_cards[i])
    for i in range(0, len(list_victim_cards), 1):
        if list_victim_cards[i][4] == game_id:
            new_list_victim_cards.append(list_victim_cards[i])
    for i in range(0, len(list_room_cards), 1):
        if list_room_cards[i][4] == game_id:
            new_list_room_cards.append(list_room_cards[i])
    # *********************************************#

    # Eliminar las cartas que esten en el sobre
    # *********************************************#
    new_list_monster_cards_envelope = []
    new_list_victim_cards_envelope = []
    new_list_room_cards_envelope = []

    for i in range(0, len(new_list_monster_cards), 1):
        if new_list_monster_cards[i][3] == 0:
            new_list_monster_cards_envelope.append(new_list_monster_cards[i])
    for i in range(0, len(new_list_victim_cards), 1):
        if new_list_victim_cards[i][3] == 0:
            new_list_victim_cards_envelope.append(new_list_victim_cards[i])
    for i in range(0, len(new_list_room_cards), 1):
        if new_list_room_cards[i][3] == 0:
            new_list_room_cards_envelope.append(new_list_room_cards[i])
    # *********************************************#

    # Conseguir los jugadores que tienen las cartas de la sospecha
    # *********************************************#
    suspicion = []
    for i in range(0, len(new_list_monster_cards_envelope), 1):
        if new_list_monster_cards_envelope[i][0] == monster_id:
            suspicion.append(new_list_monster_cards_envelope[i])
    for i in range(0, len(new_list_victim_cards_envelope), 1):
        if new_list_victim_cards_envelope[i][0] == victim_id:
            suspicion.append(new_list_victim_cards_envelope[i])
    for i in range(0, len(new_list_room_cards_envelope), 1):
        if new_list_room_cards_envelope[i][0] == room_id:
            suspicion.append(new_list_room_cards_envelope[i])
    print(suspicion)
    # *********************************************#

    # Filtrar por orden del jugador mas cercano al que sospecha
    # *********************************************#
    min = float("inf")
    print("Player is", get_player_id(player_who_suspects))
    for i in range(0, len(suspicion), 1):
        print("Suspicion is", suspicion[i][5])
        if suspicion[i][5] < min and suspicion[i][5] > get_player_id(
            player_who_suspects
        ):
            min = suspicion[i][5]
    if min == float("inf"):
        for i in range(0, len(suspicion), 1):
            print(min)
            if suspicion[i][5] < min and suspicion[i][5] != get_player_id(
                player_who_suspects
            ):
                min = suspicion[i][5]
    new_suspicion = []
    for i in range(0, len(suspicion), 1):
        if suspicion[i][5] == min:
            new_suspicion.append(suspicion[i])
    return new_suspicion


# Accusation
@db_session
def accuse(player_who_accuse, monster_card, victim_card, room_card):
    game_id = get_player_game(player_who_accuse)
    my_player = Player.get(name=player_who_accuse)
    envelope_monster = get_monster_card_envelope(game_id)
    envelope_victim = get_victim_card_envelope(game_id)
    envelope_room = get_room_card_envelope(game_id)
    if (
        envelope_monster[1] == monster_card
        and envelope_victim[1] == victim_card
        and envelope_room[1] == room_card
    ):
        my_player.set(is_winner=True)
        print("Winner")
    else:
        my_player.set(is_loser=True)
        print("Loser")
    return envelope_monster, envelope_victim, envelope_room


# ----------------------------------------- BOARD -----------------------------------------


@db_session
def player_position_and_piece(game_name):
    players_Pieces = ["azul", "verde", "rojo", "celeste", "amarillo", "rosa"]
    players_Initial_Position = [(6, 0), (6, 19), (13, 0), (13, 19), (19, 13), (19, 6)]

    myPlayerList = get_all_players_from_game(game_name)
    for i in range(0, len(myPlayerList), 1):
        player_name = myPlayerList[i][1]
        player = Player.get(name=player_name)
        playerOrder = get_player_order(player_name)
        player.set(player_x=players_Initial_Position[playerOrder][0])
        player.set(player_y=players_Initial_Position[playerOrder][1])
        player.set(piece=players_Pieces[playerOrder])


@db_session
def is_available(
    coordenada_X, coordenada_Y
):  # ver que la casilla con las coordenadas sea accessible (osea un camino)
    available = [
        (0, 13),
        (1, 13),
        (2, 13),
        (3, 13),
        (4, 13),
        (5, 13),
        (6, 13),
        (7, 13),
        (8, 13),
        (9, 13),
        (10, 13),
        (11, 13),
        (12, 13),
        (13, 13),
        (14, 13),
        (15, 13),
        (16, 13),
        (17, 13),
        (18, 13),
        (19, 13),
        (0, 6),
        (1, 6),
        (2, 6),
        (3, 6),
        (4, 6),
        (5, 6),
        (6, 6),
        (7, 6),
        (8, 6),
        (9, 6),
        (10, 6),
        (11, 6),
        (12, 6),
        (13, 6),
        (14, 6),
        (15, 6),
        (16, 6),
        (17, 6),
        (18, 6),
        (19, 6),
        (6, 19),
        (6, 18),
        (6, 17),
        (6, 16),
        (6, 15),
        (6, 14),
        (6, 12),
        (6, 11),
        (6, 10),
        (6, 9),
        (6, 8),
        (6, 7),
        (6, 5),
        (6, 4),
        (6, 3),
        (6, 2),
        (6, 1),
        (6, 0),
        (13, 19),
        (13, 18),
        (13, 17),
        (13, 16),
        (13, 15),
        (13, 14),
        (13, 12),
        (13, 11),
        (13, 10),
        (13, 9),
        (13, 8),
        (13, 7),
        (13, 5),
        (13, 4),
        (13, 3),
        (13, 2),
        (13, 1),
        (13, 0),
        (5, 17),
        (4, 12),
        (5, 9),
        (3, 7),
        (5, 4),
        (10, 14),
        (10, 5),
        (14, 15),
        (15, 12),
        (14, 9),
        (16, 7),
        (14, 3),
    ]
    res = False
    i = 0
    while res == False and i < len(available):
        if available[i][0] == coordenada_X and available[i][1] == coordenada_Y:
            res = True
        else:
            i += 1
    return res


@db_session
def is_a_room(
    coordenada_X, coordenada_Y
):  # se fija si la casilla con las coordenadas es un recinto
    rooms = [
        (5, 17),
        (4, 12),
        (5, 9),
        (3, 7),
        (5, 4),
        (10, 14),
        (10, 5),
        (14, 15),
        (15, 12),
        (14, 9),
        (16, 7),
        (14, 3),
    ]
    res = False
    i = 0
    while res == False and i < len(rooms):
        if rooms[i][0] == coordenada_X and rooms[i][1] == coordenada_Y:
            res = True
        else:
            i += 1
    return res


@db_session
def get_coordinates_X(player_name, direction):
    myPlayer = Player.get(name=player_name)
    my_X = myPlayer.player_x
    my_Y = myPlayer.player_y
    if direction == "W" or direction == "w":
        if is_available(my_X, my_Y + 1):
            return my_X
    elif direction == "S" or direction == "s":
        if is_available(my_X, my_Y - 1):
            return my_X
    elif direction == "D" or direction == "d":
        if is_available(my_X + 1, my_Y):
            return my_X + 1
    elif direction == "A" or direction == "a":
        if is_available(my_X - 1, my_Y):
            return my_X - 1


@db_session
def get_coordinates_Y(player_name, direction):
    myPlayer = Player.get(name=player_name)
    my_X = myPlayer.player_x
    my_Y = myPlayer.player_y
    if direction == "W" or direction == "w":
        if is_available(my_X, my_Y + 1):
            return my_Y + 1
    elif direction == "S" or direction == "s":
        if is_available(my_X, my_Y - 1):
            return my_Y - 1
    elif direction == "D" or direction == "d":
        if is_available(my_X + 1, my_Y):
            return my_Y
    elif direction == "A" or direction == "a":
        if is_available(my_X - 1, my_Y):
            return my_Y


@db_session
def move_player(player_name, movement):
    myPlayer = Player.get(name=player_name)
    my_X = myPlayer.player_x
    my_Y = myPlayer.player_y
    dice = myPlayer.dice_number
    if movement == "W" or movement == "w":
        if is_available(my_X, my_Y + 1):
            if is_a_room(my_X, my_Y + 1):
                myPlayer.set(player_y=my_Y + 1)
                myPlayer.set(dice_number=0)
            else:
                myPlayer.set(player_y=my_Y + 1)
                myPlayer.set(dice_number=dice - 1)
        else:
            print("illegal move")
    elif movement == "S" or movement == "s":
        if is_available(my_X, my_Y - 1):
            if is_a_room(my_X, my_Y - 1):
                myPlayer.set(player_y=my_Y - 1)
                myPlayer.set(dice_number=0)
            else:
                myPlayer.set(player_y=my_Y - 1)
                myPlayer.set(dice_number=dice - 1)
        else:
            print("illegal move")
    elif movement == "D" or movement == "d":
        if is_available(my_X + 1, my_Y):
            if is_a_room(my_X + 1, my_Y):
                myPlayer.set(player_x=my_X + 1)
                myPlayer.set(dice_number=0)
            else:
                myPlayer.set(player_x=my_X + 1)
                myPlayer.set(dice_number=dice - 1)
        else:
            print("illegal move")
    elif movement == "A" or movement == "a":
        if is_available(my_X - 1, my_Y):
            if is_a_room(my_X - 1, my_Y):
                myPlayer.set(player_x=my_X - 1)
                myPlayer.set(dice_number=0)
            else:
                myPlayer.set(player_x=my_X - 1)
                myPlayer.set(dice_number=dice - 1)
        else:
            print("illegal move")
    else:
        print("wrong key, use AWSD")
