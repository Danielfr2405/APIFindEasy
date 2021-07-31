import certifi
from pymongo import MongoClient

ca = certifi.where()


class DatabaseMongoDB:

    @staticmethod
    def connection():
        client = MongoClient(
            "",
            tlsCAFile=ca
            # ssl_cert_reqs=ssl.CERT_NONE
        )
        db = client.DBFindEasy

        return db
