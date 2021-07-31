import json
import os
from flask import Flask, request
from db.banco_de_dados import DatabaseMongoDB
from consult.consult_db import ConsultDatabase

app = Flask(__name__)
# app.debug = True


@app.route("/")
def home():
    return 'Ops, tente novamente!'


@app.route('/insert', methods=['POST'])
def insert_cordenada():
    try:
        data = request.data
        data = data.decode('utf-8')
        db = DatabaseMongoDB.connection()
        if data:
            id_obj = ConsultDatabase(db=db).insert_register(
                table='cordenadas',
                response=json.loads(data)
            )

        if id_obj and id_obj.get('id') != '0':
            return str(id_obj)

        return 'Não foi possível processar a inclusão'
    except:
        return 'Não foi possível processar a inclusão'


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


if "__main__" == __name__:
    main()
