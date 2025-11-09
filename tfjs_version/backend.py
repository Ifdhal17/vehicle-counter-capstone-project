from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import socketio
import os

# Create FastAPI instance
app = FastAPI()

# Setup CORS (optional, for development purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Socket.IO server
sio = socketio.AsyncServer(async_mode="asgi")

# Attach Socket.IO to FastAPI
socket_app = socketio.ASGIApp(sio, app)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Health check route
@app.get("/health", status_code=200)
def health_check():
    return {"status": "ok"}

# Serve index.html
@app.get("/", response_class=HTMLResponse)
async def get_index():
    file_path = "static/index.html"
    if os.path.exists(file_path):
        async with aiofiles.open(file_path, mode="r") as f:
            content = await f.read()
        return HTMLResponse(content=content)
    else:
        return HTMLResponse(content="<h1>index.html not found</h1>", status_code=404)

# Socket.IO event listener for "counter"
@sio.on("counter")
async def handle_counter(sid, data):
    print(f"Received counter message: {data}")

# To run the server, use the following command in the terminal:
# uvicorn main:socket_app --host 0.0.0.0 --port 8000
