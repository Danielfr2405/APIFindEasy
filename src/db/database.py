import certifi
from pymongo import MongoClient

ca = certifi.where()


class DatabaseMongoDB:

    @staticmethod
    def connection():
        client = MongoClient(
            "mongodb+srv://sa:findeasy@dbfindeasy.lxy04.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
            tlsCAFile=ca
            # ssl_cert_reqs=ssl.CERT_NONE
        )
        db = client.DBFindEasy

        return db
