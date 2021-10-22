from pydantic import BaseModel
from typing import Optional

from database import List_of_Games


class GameTemp(BaseModel):
    game_name: str
    num_players: int
    is_started: bool 
    is_full: bool 

 
