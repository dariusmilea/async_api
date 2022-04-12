from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends, HTTPException


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}