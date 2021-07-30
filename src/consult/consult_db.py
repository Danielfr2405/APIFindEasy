import datetime
import json
from src.dto.meu_objeto_model import MeuObjetoModel


class ConsultDatabase:
    db = None

    def __init__(self, db):
        self.db = db

    def insert_register(self, table, response) -> str:
        obj_find = self.db[table].find_one()
        item = MeuObjetoModel()
        item.id = response['id']
        item.latitude = response['latitude']
        item.longitude = response['longitude']
        item.data_inclusao = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')

        if obj_find:
            self.db[table].delete_many({})

        if self.db is not None:
            item = [json.loads(json.dumps(item.__dict__))]
            self.db[table].insert_many(item)

        return self.db[table].find_one()
