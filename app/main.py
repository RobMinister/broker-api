from fastapi import FastAPI, WebSocket
from app.market_data import market_data
from app.orders import order_book

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Broker API is running"}

@app.websocket("/ws/{ticker}")
async def websocket_endpoint(websocket: WebSocket, ticker: str):
    await market_data.subscribe(websocket, ticker)

@app.post("/order/{order_type}/{ticker}/{quantity}/{client_id}")
def place_order(order_type: str, ticker: str, quantity: int, client_id: str):
    order_result = order_book.place_order(order_type.upper(), ticker, quantity, client_id)
    return {
        "message": "Order placed",
        "matched": order_result["matched"],
        "confirmations": order_result["confirmations"]
    }
