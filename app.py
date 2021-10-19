from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from database import *
from pydantic_models import *

MAX_LEN_NAME_GAME = 10
MIN_LEN_NAME_GAME = 3
MAX_LEN_NAME_NICK = 6
MIN_LEN_NAME_NICK = 3

app = FastAPI(title="mystery")

origins = ["http://localhost:3000" "localhost:3000"]

# creation game


@app.post("/creationgame")
async def game_creation(gametocreate: GameTemp):
    invalid_fields = HTTPException(status_code=404, detail="field size is invalid")
    if (
        len(gametocreate.game_name) > MAX_LEN_NAME_GAME
        or len(gametocreate.game_name) < MIN_LEN_NAME_GAME
    ):
        raise invalid_fields
    elif game_exist(gametocreate.game_name):
        raise HTTPException(status_code=404, detail="game exist")
    else:
        gametocreate.is_full = False
        gametocreate.is_started = False
        new_game(gametocreate.game_name)
        return {"game": gametocreate.game_name}


# creation user/nickname


@app.post("/creationuser")
async def user_creation(user_to_create: str):
    invalid_fields = HTTPException(status_code=404, detail="field size is invailde")
    if (
        len(user_to_create) > MAX_LEN_NAME_GAME
        or len(user_to_create) < MIN_LEN_NAME_GAME
    ):
        raise invalid_fields
    elif user_exist(user_to_create):
        raise HTTPException(status_code=404, detail="user exist")
    else:
        new_user(user_to_create)
        return {"user": user_to_create}
