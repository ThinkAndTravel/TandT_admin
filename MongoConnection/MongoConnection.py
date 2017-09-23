from pymongo import MongoClient

class MongoConnector():
    def __init__(self, connection_string, database_name):
        client = MongoClient(connection_string)
        self.db = client[database_name]

    def get_collection(self, name):
        self.collection = self.db[name]