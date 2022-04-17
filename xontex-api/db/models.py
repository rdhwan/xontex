from pydantic import BaseModel, Field
from typing import Optional


class Soal(BaseModel):
    soal: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "soal": "PHA+IERpYmF3YWggaW5pIG1lcnVwYWthbiBjb250b2ggL3QgL24gPC9wPg==",
            }
        }


class SubmitJawaban(BaseModel):
    soal: str = Field(...)
    jawaban: Optional[str]
    username: str = Field(...)

    def __getitem__(self, item):
        return getattr(self, item)

    class Config:
        schema_extra = {
            "example": {
                "soal": "PHA+IERpYmF3YWggaW5pIG1lcnVwYWthbiBjb250b2ggL3QgL24gPC9wPg==",
                "jawaban": "PGxhYmVsPiAxMjAvNDAgPSAzIDwvbGFiZWw+",
                "username": "bunga",
            }
        }


def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message,
        "data": {"jawab": [{"username": "Belum ada jawaban", "jawaban": " "}]},
    }
