from typing import Dict
from fastapi import WebSocket
from database import *

class ConnectionManager:
    """
    Handler of socket connections
    """

    def __init__(self):
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, name_game: str, name_player: str):
        gameID = get_game_id(name_game)
        playerID = get_player_id(name_player)
        await websocket.accept()
        if gameID in self.active_connections:  # Exist game in active_connections
            self.active_connections[gameID].update({playerID: websocket})
        else:
            self.active_connections[gameID] = {playerID: websocket}

    async def disconnect(self, name_game: str, name_player: str):
        gameID = get_game_id(name_game)
        playerID = get_player_id(name_player)
        await self.active_connections[gameID].get(playerID).close()
        self.active_connections[gameID].pop(playerID)
        if self.active_connections[gameID] == {}:  # Empty game
            self.active_connections.pop(gameID)

    async def send_personal_json(self, message, websocket: WebSocket):
        await websocket.send_json(message)
        return

    async def broadcast_text(self, name_game: str, message: str):
        gameID = get_game_id(name_game)
        game = self.active_connections.get(gameID)
        if game != None:
            for connection in game.values():
                await connection.send_text(message)
        return

    async def broadcast_json(self, name_game: str, message):
        gameID = get_game_id(name_game)
        game = self.active_connections.get(gameID)
        if game != None:
            for connection in game.values():
                await connection.send_json(message)
        return

    def exist_socket_of_player(self, name_game: str, name_player: str) -> bool:
        gameID = get_game_id(name_game)
        playerID = get_player_id(name_player)
        game = self.active_connections.get(gameID)
        if game != None and get_player_game(name_game) != None:
            return True
        return False

    def get_all_connections(self):
        return self.active_connections

    def get_socket_player(self, name_game: str, name_player: str) -> WebSocket:
        gameID = get_game_id(name_game)
        playerID = get_player_id(name_player)
        game = self.active_connections.get(gameID)
        if game != None:
            player = get_player(name_player)
            return player
