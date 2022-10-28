import logging

def init():
    global secondariesList
    global messageList
    global urls
    global logger

    secondariesList = []
    messageList = []
    urls = { 
        'http://172.17.0.2:81/addItem', 
        'http://172.17.0.3:82/addItem', 
        #'http://localhost:83/addItem'
        }
  
    logger = logging.getLogger("MasterApp")
