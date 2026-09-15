# backend/simple_server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Server is running!"}

@app.get("/system/load")
def system_load():
    return {"cpu": 10, "memory": 50, "disk": 30}

@app.get("/system/logs")
def system_logs(limit: int = 20):
    return {"logs": [f"Log {i}" for i in range(limit)]}

if __name__ == "__main__":
    print("✅ Server starting at http://127.0.0.1:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)