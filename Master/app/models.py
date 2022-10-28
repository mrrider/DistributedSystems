from pydantic import BaseModel
import datetime

class Secondary(BaseModel):
    id: int
    url: str 

class Item(BaseModel):
    message: str

class Response(BaseModel):
    __root__: list[Item] 

class Message(BaseModel):
    id: int
    message: str 
    createdDate: datetime.datetime