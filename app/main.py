# uvicorn app.main:app --reload
# Removing all the Note Comments from the Previous Tutorial.


from operator import index
from sqlite3 import Cursor
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from fastapi.params import Body
from grpc import StatusCode
from httpx import post
from pydantic import BaseModel
from typing import List, Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy.sql import text

from . import models, schemas, utils
from .database import engine, get_db
from .routers import posts, users, auth, votes
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"] # If you want to allow all the domains to access the request.
# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]

# I don't really know how to remove all the alembic shit that we did went through. Goddamn how do we remove it ?

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "My Name is Racheet Anand and I am the ruler of this world."}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(votes.router)

