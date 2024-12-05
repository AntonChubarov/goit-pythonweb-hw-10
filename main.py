from fastapi import FastAPI

from api import contacts

app = FastAPI()

app.include_router(contacts.router)
