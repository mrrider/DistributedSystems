from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import datetime
import logging

messageList = []
logger = logging.getLogger("Secondary")

class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: yellow + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def initLogger():
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)

class Message(BaseModel):
    id: int
    message: str 
    createdDate: datetime.datetime

app = FastAPI()
initLogger()
logger.info("Application started.")

@app.get("/getItems/") 
def readItem():
    logger.info("Get items call started....")
    return messageList

@app.post("/addItem/")
def addItem(message: Message):
    logger.info("Post item call started...")
    messageList.append(message)
    logger.info("Message '{}' saved.".format(message.message))
    logger.info("Post item call finished")
    return message

