import json
import os
import base64
from flask import Flask, request
from controler.monitoring import MonitoringObject as Monitoring

from controler.auth_guardians import AuthGuardians as Auth

app = Flask(__name__)
app.debug = True


@app.route('/Insert', methods=['POST'])
def insert_coordenada():
    try:
        data = request.data
        data = data.decode('utf-8')
        if data:
            id_obj = Monitoring().insert_register(
                table='coordenadas',
                response=json.loads(data)
            )

        print(id_obj)
        return gera_response('', len(id_obj) > 0, 200)
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
        finds_founds = Monitoring().find_registers(
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


@app.route('/DeleteAll', methods=['Post'])
def delete_all():
    try:
        finds_founds = Monitoring().delete_registers(
            table='coordenadas'
        )
        return gera_response(
            'Deleção realizada com sucesso!',
            len(finds_founds) == 0,
            200
        )
    except Exception as e:
        print(e)
        return gera_response(
            message='Não foi possível deletar as coordenadas!',
            data='',
            status_code=500
        )


@app.route('/Auth', methods=['Post'])
def auth_guardian():
    try:
        data = request.data
        data = data.decode('utf-8')
        if data:
            if 'usuario' in data:
                message, data, status_code = Auth().insert(
                    table='authGuardians', response=json.loads(data)
                )
            else:
                message, data, status_code = Auth().login(
                    table='authGuardians',
                    response=data
                )
            return gera_response(message, data, status_code)
    except Exception as e:
        print(e)
        return gera_response(
            message='Houve falha na autenticação do usuário!',
            data='',
            status_code=500
        )


@app.route('/FindUser/<user>', methods=['GET'])
def find_usuario(user):
    try:
        dados_usuario = Auth().search_username(
                table='authGuardians',
                info_user=[user]
            )

        dados_usuario.pop('password')

        return gera_response(
            'Consulta realizada com sucesso!',
            dados_usuario,
            200
        )
    except Exception as e:
        print(e)
        return gera_response(
            message=
            'Não foi possível consultar os dados do cadastro do usuário!',
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
