from typing import List
from pony.orm import *

db = pony.orm.Database()


db.bind(provider="sqlite", filename="db.mystery", create_db=True)

# Games table and Functions


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    nickname = Required(str)
    player = Optional("Player")


class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    host = Required(bool)
    user = Required(User)
    game = Required("Game")


class Game(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    is_started = Required(bool)
    is_full = Required(bool)
    num_players = Optional(int)
    players = Set(Player)

class List_of_Games(db.Entity):
    games = List[Game]


db.generate_mapping(create_tables=True)


@db_session
def new_game(new_name):
    Game(name=new_name, is_started=False, is_full=False)


@db_session
def game_exist(un_name):
    if Game.get(name=un_name) is not None:
        return True


@db_session
def new_user(new_name):
    User(nickname=new_name)


@db_session
def user_exist(name):
    if User.get(nickname=name) is not None:
        return True


@db_session
def game_exist(gname):
    if Game.get(name=gname) is not None:
        return True


@db_session
def join_game(new_name):
    Game(name=new_name, is_started=False, is_full=False)


@db_session
def get_number_player(num_user):
    return Game.get(num_players=num_user)


@db_session
def is_full(num_user):
    if get_number_player(num_user) == 6:
        return True


@db_session
def is_started(started):
    return Game.get(is_started=started)


@db_session
def add_player(num_user):
    return get_number_player(num_user) + 1


@db_session
def get_game(game):
    return Game.get(name=game)


@db_session
def insert_player(un_game, player):
    game = get_game(un_game)
    game.Player.add(player)


@db_session
def get_all_games(data):
    p = 0
    games : List_of_Games
    for p in len(data):
        games[p] = get_game(data)
    return games


@db_session
def game_is_available(game):
    if not game.is_full and not game.is_started:
        return True
