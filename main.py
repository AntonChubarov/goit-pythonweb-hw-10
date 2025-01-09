import aioredis
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from api import contacts, auth, users
from clients.fast_api_mail_client import FastApiMailClient
from repositories.user_repository import UserRepository
from services.auth_service import AuthService

limiter = Limiter(
    key_func=lambda request: f"user-{getattr(request.state, 'user_id', get_remote_address(request))}",
    storage_uri="redis://redis:6379"
)

app = FastAPI()

app.state.limiter = limiter


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://redis:6379", encoding="utf-8", decode_responses=True)


user_repository = UserRepository()
email_client = FastApiMailClient()
auth_service = AuthService(user_repository=user_repository, email_sender=email_client)


@app.middleware("http")
async def set_user_id(request: Request, call_next):
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token[7:]
    else:
        token = None

    try:
        user = auth_service.get_current_user(token)
        request.state.user_id = user.id
    except Exception:
        request.state.user_id = None

    response = await call_next(request)
    return response


app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts.router)
app.include_router(auth.router)
app.include_router(users.router)
