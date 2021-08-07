import certifi
from pymongo import MongoClient

ca = certifi.where()
url = ''


class DatabaseMongoDB:

    @staticmethod
    def connection():
        client = MongoClient(
            url,
            tlsCAFile=ca
        )
        db = client.DBFindEasy

        return db
