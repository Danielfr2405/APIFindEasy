import datetime
import json
from src.dto.meu_objeto_model import MeuObjetoModel
from src.db.banco_de_dados import DatabaseMongoDB


class MonitoringObject:
    db = None

    def __init__(self):
        self.db = DatabaseMongoDB.connection()

    def insert_register(self, table, response) -> str:
        id_obj = str(response['id'])
        my_obj = {"Atual": {}, "Anterior": {}, "_id": id_obj}
        obj_find = self.exists_obj(table=table, id_obj=id_obj)

        item = MeuObjetoModel()
        item.latitude = self.calculo_coordenadas(response['latitude'])
        item.longitude = self.calculo_coordenadas(response['longitude'])
        item.data_inclusao = datetime.datetime.now().isoformat()

        my_obj["Anterior"] = \
            obj_find["Atual"] if obj_find and obj_find["Atual"] else {}
        my_obj["Atual"] = json.loads(json.dumps(item.__dict__))

        if self.db is not None:
            self.db[table].insert_one(my_obj)

        return self.find_registers(table=table, id_obj=id_obj)

    def exists_obj(self, table, id_obj):
        obj_find = {}

        for obj in self.find_registers(table=table, id_obj=id_obj):
            obj_find = obj

        if obj_find:
            self.delete_registers(table=table, id_obj=id_obj)

        return obj_find

    @staticmethod
    def calculo_coordenadas(latitude):
        split_latitude = latitude.split('.')
        valor_soma = split_latitude[0][:-2]
        aux1 = split_latitude[0][-2:len(split_latitude[0])]
        aux2 = split_latitude[1]

        valor = float(f"{ aux1 }.{ aux2 }")
        valor = valor / 60
        valor = (valor + float(valor_soma)) * -1
        return valor

    def find_registers(self, table, id_obj=None):
        objects = self.db[table]
        lists_found = []
        filter_db: object = {"_id": id_obj} if id_obj else {}

        for obj in objects.find(filter_db):
            lists_found.append(obj)

        return lists_found

    def delete_registers(self, table, id_obj=None):
        filter_db: object = {"_id": id_obj} if id_obj else {}
        self.db[table].delete_many(filter_db)

        return self.find_registers(table=table)
