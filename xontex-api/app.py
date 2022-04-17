import os
import secrets
from base64 import b64decode
from urllib.parse import unquote

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED

from api import database
from db import data
from db.models import *

load_dotenv()
app = FastAPI(openapi_url=None)

security = HTTPBasic()
# openapi_url = None
load_dotenv


def login(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(
        credentials.username, os.getenv("APP_USERNAME")
    )
    correct_password = secrets.compare_digest(
        credentials.password, os.getenv("APP_PASSWORD")
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True


# def login(credentials: HTTPBasicCredentials = Depends(security)):
#     if (
#         credentials.username != "paralympic"
#         or credentials.password != "paralympicjaya!"
#     ):
#         raise HTTPException(
#             status_code=HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     return True


@app.get("/api/v1")
async def root(login: bool = Depends(login)) -> None:
    return {"message": "xontex backend", "login": login}


@app.get("/api/v1/listmapel")
async def list_mapel(login: bool = Depends(login)):
    return {"mapel": data.listujian()}


# @app.get("/{mapel}")
# async def get_all_jawaban(mapel: str):
#     jawaban = await database.retrieve_all_jawaban(mapel)
#     if jawaban:
#         return ResponseModel(jawaban, "Jawaban data retrieved successfully.")
#     return ErrorResponseModel("An error occurred.", 404, "Belum ada jawaban")


@app.get("/api/v1/{mapel}")
async def get_jawaban(mapel: str, headers: Request, login: bool = Depends(login)):
    soal = headers.headers.get("X-SOAL")
    jawaban = await database.retrieve_jawaban(mapel, b64decode(soal).decode("utf-8"))
    if jawaban:
        return ResponseModel(jawaban, "Jawaban data retrieved successfully.")
    return ErrorResponseModel("An error occurred.", 404, "Belum ada jawaban")


@app.post("/api/v1/{mapel}/jawab")
async def submit_jawaban(
    mapel: str, jawaban: SubmitJawaban, login: bool = Depends(login)
):
    if jawaban["jawaban"]:
        submit = await database.add_jawaban(mapel, jawaban)
        return ResponseModel(submit, "Successfully added jawaban")
    return ErrorResponseModel("An error occurred.", 404, "Belum ada jawaban")
