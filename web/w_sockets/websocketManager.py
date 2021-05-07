from websockets.exceptions import ConnectionClosedOK
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self,client_id, alvo, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append({"user": client_id,"alvo":alvo, "conn": websocket})

    def disconnect(self,client_id, websocket: WebSocket):
        for item in self.active_connections:
            self.active_connections.remove(item) if item["conn"] == websocket else ...


    async def send_personal_message(self,client_id: str, message: str, alvo: str):
        data = {
            "user":client_id,
            "msg": message
        }
        for item in self.active_connections:
            if item["user"] == alvo and item["alvo"] == client_id:
                websocket = item["conn"]
        try:
            await websocket.send_json(data)
        except Exception as error:
            print(error)
