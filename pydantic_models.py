from pydantic import BaseModel
from typing import Optional

class GameTemp(BaseModel):
    game_name: str
    is_started: bool = False
    is_full: bool = False
