from pony.orm import *

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


# Game Table
class Game(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    is_started = Required(bool)
    is_full = Required(bool)
    num_players = Required(int)
    Players = Set(Player)


db.generate_mapping(create_tables=True)


@db_session
def new_game(new_name):
    Game(name=new_name, is_started=False, is_full=False, num_players=0)


@db_session
def game_exist(un_name):
    if Game.get(name=un_name) is not None:
        return True


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
def is_started(started):
    return Game.get(is_started=started)


@db_session
def add_player(a_game):
    game = get_game(a_game)
    sum_players = get_number_player(a_game) + 1
    game.set(num_players=sum_players)


@db_session
def get_game(a_game):
    return Game.get(name=a_game)


@db_session
def insert_player(un_game, un_player):
    player = Player.get(name=un_player)
    game = get_game(un_game)
    game.Players.add(player)


@db_session
def new_player(name_player, name_game):
    Player(name=name_player, user=get_user(name_player), game=get_game(name_game))


@db_session
def player_delete(un_player):
    player = Player.get(name=un_player)
    curgame = player.game
    curgame.set(num_players=get_number_player(curgame.name)-1)
    Player.delete(player)


@db_session
def player_exist(un_player):
    if Player.get(name=un_player) is not None:
        return True
    
@db_session
def start_game(game):
    my_game = get_game(game)
    my_game.set(is_started = True)
