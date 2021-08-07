import json
import os
from flask import Flask, request
from consult.consult_db import ConsultDatabase

app = Flask(__name__)
# app.debug = True


@app.route('/Insert', methods=['POST'])
def insert_coordenada():
    try:
        data = request.data
        data = data.decode('utf-8')
        if data:
            id_obj = ConsultDatabase().insert_register(
                table='coordenadas',
                response=json.loads(data)
            )

        is_ok = id_obj and id_obj.get('id') != '0'
        return gera_response('', is_ok, 200)
    except Exception as e:
        print(e)
        return gera_response(
            message='Não foi possível processar a inclusão',
            data='',
            status_code=500
        )


@app.route('/FindById/<id_obj>', methods=['GET'])
def find_coordenada(id_obj):
    try:
        finds_founds = ConsultDatabase().find_registers(
            table='coordenadas',
            id_obj=id_obj
        )
        return gera_response(
            'Consulta realizada com sucesso!',
            finds_founds,
            200
        )
    except Exception as e:
        print(e)
        return gera_response(
            message='Não foi possível consultar as coordenadas!',
            data='',
            status_code=500
        )


def gera_response(message, data, status_code):
    body = {}

    if message:
        body['message'] = message

    body['data'] = data

    return body, status_code


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


if "__main__" == __name__:
    main()
