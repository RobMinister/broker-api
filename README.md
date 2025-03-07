 # Broker API - Dockerized Setup

## Overview
This Broker API lets you:
- Subscribe to real-time market data via WebSockets.
- Unsubscribe from market data streaming.
- Place **BUY** and **SELL** orders.
- Automatically match buy and sell orders based on quantity.

This project is fully **Dockerized**, making it easy to set up and run anywhere.

---

## **Getting Started**
### **1. Install Prerequisites**
Make sure you have:
- **Docker Desktop** ([Download Here](https://www.docker.com/products/docker-desktop/))
- **Postman** ([Download Here](https://www.postman.com/downloads/)) - For WebSocket and API requests testing


---

## **2. Run the API in Docker**

### **Clone the Repository**
```bash
 git clone https://github.com/RobMinister/broker-api.git
 cd broker-api
```

### **Build the Docker Image**
```bash
 docker build -t broker-api .
```

### **Run the API in a Container**
```bash
 docker run -p 8000:8000 broker-api
```
✅ The API is now live at **http://127.0.0.1:8000/**

---

## **3. Testing the API**

### **Check If the API is Running**
Run:
```bash
 curl -X GET "http://127.0.0.1:8000/"
```
✅ Expected Output:
```json
{
    "message": "Broker API is running"
}
```

### **Subscribe to Market Data (WebSocket)**
#### **Using Postman**
1. Open **Postman**.
2. Click on **New**
2. Select **WebSocket**.
3. Connect to:
   ```
   ws://127.0.0.1:8000/ws/TSLA
   ```
4. ✅ You should start seeing real-time updates like:
   ```json
   {
       "timestamp": "2025-03-07T12:34:56.789Z",
       "symbol": "TSLA",
       "price": 312.45,
       "quantity": 50
   }
   ```

### **Unsubscribe from Market Data**
1. In **Postman**, in **Message** enter:
   ```
   UNSUBSCRIBE TSLA
   ```
and click on **Send**

✅ WebSocket connection closes, and data stops streaming.

---

## **4. Placing Orders**

1. In **Postman**, click on New.
2. Select **HTTP**.
3. Connect to:

### **Place a BUY Order**
```bash
 curl -X POST "http://127.0.0.1:8000/order/BUY/TSLA/10/clientA"
```
✅ Expected Output:
```json
{
    "message": "Order placed",
    "matched": [],
    "confirmations": []
}
```

### **Place a SELL Order (Partial Match)**
```bash
 curl -X POST "http://127.0.0.1:8000/order/SELL/TSLA/5/clientB"
```
✅ Expected Output:
```json
{
    "message": "Order placed",
    "matched": [[5, "clientA"]],
    "confirmations": [
        {
            "buyer": "clientA",
            "seller": "clientB",
            "ticker": "TSLA",
            "quantity": 5
        }
    ]
}
```

### **Complete the Trade with Another SELL Order**
```bash
 curl -X POST "http://127.0.0.1:8000/order/SELL/TSLA/5/clientC"
```
✅ Expected Output:
```json
{
    "message": "Order placed",
    "matched": [[5, "clientA"]],
    "confirmations": [
        {
            "buyer": "clientA",
            "seller": "clientC",
            "ticker": "TSLA",
            "quantity": 5
        }
    ]
}
```

---

## **5. Stopping the Docker Container**
To stop the running container:
```bash
CTRL + C
```
Or manually stop it:
```bash
docker ps  # List running containers
docker stop <CONTAINER_ID>
```

---

## **Final Notes**
- WebSocket **subscriptions and unsubscriptions** work smoothly.
- Orders **match correctly** and store unmatched ones for later.
- Everything runs **fully in Docker**, making setup easy.
