from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .websocketManager import ConnectionManager


manager = ConnectionManager()
chat = APIRouter()

@chat.websocket("/{client_id}/{alvo}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, alvo: str):
    await manager.connect(client_id, alvo, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(client_id=client_id, alvo=alvo, message=data)

    except WebSocketDisconnect:

        manager.disconnect(client_id, websocket)
    
        await manager.send_personal_message(
            client_id=client_id, alvo=alvo, message=f"{client_id} saiu da conversa!"
        )