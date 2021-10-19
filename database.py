from pony.orm import *

db = pony.orm.Database()

<<<<<<< HEAD
db.bind("mysql", host="127.0.0.1", user="root", passwd="", db="mystery")
<<<<<<< HEAD
=======
=======
db.bind(provider="sqlite", filename="db.mystery", create_db=True)
>>>>>>> 7418ecaaca89695d71bd6421de010eec8eefd89c

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


db.generate_mapping(create_tables=True)


@db_session
def new_game(new_name):
    Game(name=new_name, is_started=False, is_full=False)


@db_session
def game_exist(un_name):
    if Game.get(name=un_name) is not None:
        return True
<<<<<<< HEAD
>>>>>>> 95178e9dacc13aac37ddf9b97def952493eb160c
=======


@db_session
def new_user(new_name):
    User(nickname=new_name)


@db_session
def user_exist(name):
    if User.get(nickname=name) is not None:
        return True
>>>>>>> 7418ecaaca89695d71bd6421de010eec8eefd89c
