from pymongo import MongoClient

class MongoConnection:
    def __init__(self):
        self.client = MongoClient("mongodb://172.30.1.26:27017")

    def getConnection(self):
        return self.client