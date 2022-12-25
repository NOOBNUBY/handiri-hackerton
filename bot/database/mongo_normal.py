from bot.database.conn.mongo import *

class mongo_register:
    def __init__(self, client):
        self.client = client.getConnection()
        self.db = self.client["imagine"]
        self.collection = self.db["users"]

    def register(self, user_id):
        query = {"user_id":user_id}
        result = self.collection.insert_one(query)
        return result

    def register_check(self, user_id):
        query = {"user_id":user_id}
        result = self.collection.find_one(query)
        if result == None:
            return False
        else:
            return True