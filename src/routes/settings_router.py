# Routes APIs and its endpoints

from fastapi import APIRouter
from src.endpoints.chat_control_endpoint import initiate, converse

chat_routes = APIRouter()

chat_routes.add_api_route("/initiate", initiate, methods=["POST"])
chat_routes.add_api_route("/converse", converse, methods=["POST"])
