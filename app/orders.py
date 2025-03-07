from fastapi import HTTPException
from collections import deque

class OrderBook:
    def __init__(self):
        self.buy_orders = {}  # Stores buy orders as {ticker: deque[(quantity, client_id)]}
        self.sell_orders = {}  # Stores sell orders as {ticker: deque[(quantity, client_id)]}

    def place_order(self, order_type: str, ticker: str, quantity: int, client_id: str):
        if order_type == "BUY":
            return self.match_order(self.sell_orders, self.buy_orders, ticker, quantity, client_id, is_buy=True)
        elif order_type == "SELL":
            return self.match_order(self.buy_orders, self.sell_orders, ticker, quantity, client_id, is_buy=False)
        else:
            raise HTTPException(status_code=400, detail="Invalid order type")

    def match_order(self, counter_orders, current_orders, ticker, quantity, client_id, is_buy):
        if ticker not in counter_orders:
            counter_orders[ticker] = deque()
        if ticker not in current_orders:
            current_orders[ticker] = deque()

        matched = []
        confirmations = []  # Store confirmations for both buyer and seller

        while quantity > 0 and counter_orders[ticker]:
            existing_quantity, existing_client = counter_orders[ticker][0]
            match_quantity = min(quantity, existing_quantity)

            # Assign correct roles
            if is_buy:  # Current order is a BUY order
                buyer = client_id
                seller = existing_client
            else:  # Current order is a SELL order
                buyer = existing_client
                seller = client_id

            # Store confirmation details
            confirmations.append({
                "buyer": buyer,
                "seller": seller,
                "ticker": ticker,
                "quantity": match_quantity
            })

            matched.append((match_quantity, existing_client))
            quantity -= match_quantity

            if match_quantity == existing_quantity:
                counter_orders[ticker].popleft()
            else:
                counter_orders[ticker][0] = (existing_quantity - match_quantity, existing_client)

        # If any remaining quantity, store it in the order book
        if quantity > 0:
            current_orders[ticker].append((quantity, client_id))

        return {
            "matched": matched if matched else [],
            "confirmations": confirmations
        }

order_book = OrderBook()
