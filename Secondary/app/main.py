from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import datetime

messageList = []

class Message(BaseModel):
    id: int
    message: str 
    createdDate: datetime.datetime

app = FastAPI()

@app.get("/getItems/") 
def read_item():
    return messageList

@app.post("/addItem/")
def addItem(message: Message):
    messageList.append(message)
    return message

