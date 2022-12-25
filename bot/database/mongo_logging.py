from bot.database.conn.mongo import *
import datetime
class mongo_logging:
    def __init__(self, client):
        self.client = client.getConnection()
        self.db = self.client["imagine"]
        self.collection = self.db["logs"]


    """
    use_type:
    0: aiart
    1: upscale
    2: picture_analyze
    
    """
    def insert_log(self, user_id, use_type):
        query = {"user_id":user_id,
                 "type":use_type,
                 "time":datetime.datetime.now()
                }
        result = self.collection.insert_one(query)
        return result

    def get_log(self, user_id, use_type):
        query = {"user_id":user_id, "type":use_type}
        result = self.collection.find_one(query)
        print(result)
        if result == None:
            return False
        else:
            return result

    def get_logs(self, user_id, use_type):
        query = {"user_id":user_id, "type":use_type}
        """limit query to 10"""
        result = self.collection.find(query).limit(10)
        print(result)
        if result == None:
            return False
        else:
            return result