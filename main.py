from fastapi import FastAPI
from starlette.routing import Mount

#only for debugging
# import debugpy
# debugpy.listen(("0.0.0.0", 5678))

from src.routes.settings_router import chat_routes

app = FastAPI()
app.mount("/chat", chat_routes)
