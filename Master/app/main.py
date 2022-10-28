from fastapi import FastAPI
import models
import functions
import data

app = FastAPI()  
functions.start()    

@app.post("/addItem/")
def addItem(item: models.Item):
    data.logger.info("Add Item call started")
    resp = functions.processMessage(item)
    data.logger.info("Add Item call finished")
    return resp

@app.get("/getItems/") 
def read_item():
    data.logger.info("Get Items call started")
    return data.messageList