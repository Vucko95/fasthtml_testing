from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/receive")
async def receive_data(request: Request):
    data = await request.json()  # Get JSON payload
    print("Received Data:", data)  # Print to console
    return {"message": "Data received successfully", "data": data}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)  # Runs on port 8002
