import logging

def init():
    global secondariesList
    global messageList
    global urls
    global logger

    secondariesList = []
    messageList = []
    urls = { 
        'http://127.0.0.1:8000/addItem', 
        'http://127.0.0.1:8002/addItem', 
        #'http://127.0.0.1:8005/addItem', 
        # 'http://127.0.0.1:8007/addItem' 
        }
  
    logger = logging.getLogger("MasterApp")
