import models
import data
from cmath import log
from re import L
import datetime
import aiohttp
import asyncio
import ast
import logging

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

async def post(secondary, session, message, errors):
    try:
        timeout = aiohttp.ClientTimeout(total=30)
        async with session.post(url=secondary.url, json=message, timeout=timeout) as response:
            data.logger.info("Request to host id={}, utl='{}' started....".format(secondary.id, secondary.url))
            resp = await response.json()
            data.logger.info("Request to host id={}, utl='{}' finised successfull".format(secondary.id, secondary.url))
    except Exception as e:
        data.logger.error("Request to host id={}, utl='{}' failed. Error: '{}'".format(secondary.id, secondary.url, e))
        errors.append("Request to host id={}, utl='{}' failed.".format(secondary.id, secondary.url))

async def main(urls, message, errors):
    jsonMsg = message.json()
    body = ast.literal_eval(jsonMsg)
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[post(secondary, session, body, errors) for secondary in urls])

def createSecondariesList():
    for url in data.urls:
        s = models.Secondary(id=len(data.secondariesList), url=url)
        data.secondariesList.append(s)

def initLogger():
    data.logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    data.logger.addHandler(ch)

def start():
    data.init()
    createSecondariesList()
    initLogger()
    data.logger.info("Master application started. Secondaries added with such details: {}".format(data.secondariesList))

def processMessage(item: models.Item):
    errors = []
    message = models.Message(id=len(data.messageList), message=item.message, createdDate=datetime.datetime.now())
    data.messageList.append(message)
    
    asyncio.run(main(data.secondariesList, message, errors))
    if errors: 
        errorResp = models.Response(__root__=[])
        for error in errors: 
            er =  models.Item(message="Message saved, but error occured: {}".format(error))
            errorResp.__root__.append(er)
        return errorResp

    response = models.Response(__root__=[])
    it =  models.Item(message="Message '{}' saved.".format(item.message))
    response.__root__.append(it)

    return response