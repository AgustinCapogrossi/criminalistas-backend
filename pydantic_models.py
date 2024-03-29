from pydantic import BaseModel
from typing import Optional


class GameTemp(BaseModel):
    game_name: str
    num_players: int
    is_started: bool
    is_full: bool
