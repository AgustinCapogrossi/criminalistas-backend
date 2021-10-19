from pony.orm import *

db = pony.orm.Database()

db.bind("mysql", host="127.0.0.1", user="root", passwd="", db="mystery")
<<<<<<< HEAD
=======

# Games table and Functions


class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    nickname = Required(str)
    host = Required(bool)
    game = Required("Game")


class Game(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    is_started = Required(bool)
    is_full = Required(bool)
    num_players = Optional(int)
    players = Set(Player)


db.generate_mapping(create_tables=True)

@db_session
def new_game(new_name):
    Game(name=new_name, is_started=False, is_full=False)

@db_session
def game_exist(un_name):
    if Game.get(name=un_name) is not None:
        return True
>>>>>>> 95178e9dacc13aac37ddf9b97def952493eb160c
