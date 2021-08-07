import datetime
import json
from src.dto.meu_objeto_model import MeuObjetoModel
from src.db.banco_de_dados import DatabaseMongoDB


class ConsultDatabase:
    db = None

    def __init__(self):
        self.db = DatabaseMongoDB.connection()

    def insert_register(self, table, response) -> str:
        my_obj = {"Atual": {}, "Anterior": {}, "_id": response['id']}
        obj_find = self.exists_obj(table=table, id_obj=response['id'])

        item = MeuObjetoModel()
        item.latitude = self.calculo_latitude(response['latitude'])
        item.longitude = self.calculo_longitude(response['longitude'])
        item.data_inclusao = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')

        my_obj["Anterior"] = \
            obj_find["Atual"] if obj_find and obj_find["Atual"] else {}
        my_obj["Atual"] = json.loads(json.dumps(item.__dict__))

        if self.db is not None:
            self.db[table].insert_one(my_obj)

        return self.db[table].find_one()

    def exists_obj(self, table, id_obj):
        obj_find = {}

        for obj in self.db[table].find({'_id': id_obj}):
            obj_find = obj

        if obj_find:
            self.db[table].delete_many({'_id': id_obj})

        return obj_find

    @staticmethod
    def calculo_latitude(latitude):
        latitude = latitude / 60
        latitude = (latitude + 23.0) * -1
        return latitude

    @staticmethod
    def calculo_longitude(longitude):
        longitude = longitude / 60
        longitude = (longitude + 046.0) * -1
        return longitude

    def find_registers(self, table, id_obj):
        objects = self.db[table]
        lists_found = []

        for obj in objects.find({"_id": id_obj}):
            lists_found.append(obj)

        return lists_found
