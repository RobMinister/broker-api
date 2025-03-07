from fastapi import WebSocket
import asyncio
import random
import datetime

class MarketData:
    def __init__(self):
        self.subscribers = {}

    async def subscribe(self, websocket: WebSocket, ticker: str):
        await websocket.accept()
        if ticker not in self.subscribers:
            self.subscribers[ticker] = set()
        self.subscribers[ticker].add(websocket)

        try:
            while websocket in self.subscribers.get(ticker, set()):
                # Send market data
                tick_data = {
                    "timestamp": datetime.datetime.utcnow().isoformat(),
                    "symbol": ticker,
                    "price": round(random.uniform(100, 500), 2),
                    "quantity": random.randint(1, 100)
                }
                await asyncio.gather(*[ws.send_json(tick_data) for ws in self.subscribers[ticker]])
                
                # Check for unsubscribe message (without blocking)
                try:
                    message = await asyncio.wait_for(websocket.receive_text(), timeout=1)
                    if message.strip().upper() == f"UNSUBSCRIBE {ticker}":
                        await self.unsubscribe(websocket, ticker)
                        break  # Stop streaming
                except asyncio.TimeoutError:
                    pass  # Continue streaming if no message received
        except Exception:
            pass
        finally:
            await self.unsubscribe(websocket, ticker)

    async def unsubscribe(self, websocket: WebSocket, ticker: str):
        if ticker in self.subscribers and websocket in self.subscribers[ticker]:
            self.subscribers[ticker].remove(websocket)
            if not self.subscribers[ticker]:  # Remove ticker if no subscribers left
                del self.subscribers[ticker]
        await websocket.close()

market_data = MarketData()
