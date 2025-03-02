from fastapi import APIRouter, Depends
from app.core import database
from app import crud, schemas


router = APIRouter(prefix="/users", tags=["users"])
