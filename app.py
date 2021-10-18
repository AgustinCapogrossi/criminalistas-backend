from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from database import *
from pydantic_models import *
MAX_LEN_NAME_GAME = 10
MIN_LEN_NAME_GAME = 3

app = FastAPI(title="mystery")

origins = ["http://localhost:3000" "localhost:3000"]

#creation game

@app.post("/creationgame")
async def game_creation(gametocreate: GameTemp):
    invalid_fields = HTTPException(
        status_code = 404,
        detail = "field size is invalid"
    )
    if len(gametocreate.game_name) > MAX_LEN_NAME_GAME or len(gametocreate.game_name) < MIN_LEN_NAME_GAME:
        raise invalid_fields
    elif game_exist(gametocreate.game_name):
        raise HTTPException(
            status_code =404,
            detail = "game exist"
        )
    else:
        gametocreate.is_full = False
        gametocreate.is_started = False
        new_game(gametocreate.game_name)
        return {"game": gametocreate.game_name}