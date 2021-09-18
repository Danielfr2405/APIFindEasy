import base64
from src.db.banco_de_dados import DatabaseMongoDB


class AuthGuardians:
    db = None

    def __init__(self):
        self.db = DatabaseMongoDB.connection()

    def insert(self, table, response):
        message = 'Cadastro de usuário feito com sucesso!'
        status_code = 200
        data = {}

        user = {
            "_id": response['usuario'],
            "nome": response['nome'],
            "sobrenome": response['sobrenome'],
            "email": response['email'],
            "usuario": response['usuario'],
            "password": response['password'],
            "dispositivo": response['dispositivo']
        }

        if 'dt_nasc' in response:
            user['dt_nasc'] = response['dt_nasc']

        info_user = [response['usuario']]

        info_user = self.search_username(
            table=table,
            info_user=info_user
        )

        if info_user and 'usuario' in info_user:
            message = 'Já existe registro para o usuário preenchido.'
            data = False
            status_code = 400
            return message, data, status_code

        if self.db is not None:
            self.db[table].insert_one(user)

        return message, data, status_code

    def login(self, table, response):
        message = 'Autenticação feita com sucesso!'
        status_code = 200

        response = base64.b64decode(response)
        response = response.decode('utf-8')
        response = response.split(':auth:')

        info_user = self.search_username(
            table=table,
            info_user=response
        )

        if info_user and 'usuario' in info_user:
            if 'password' in info_user and \
                    info_user['password'] != response[1]:
                message = 'A senha preenchida está incorreta!'
                data = ''
                status_code = 400
            else:
                auth = f'{info_user["usuario"]}:auth:{info_user["password"]}'
                auth = base64.b64encode(bytes(auth, 'utf-8'))
                data = f'Basic {auth.decode("utf-8")}'
        else:
            message = 'O usuário ainda não foi cadastrado!'
            data = ''
            status_code = 400

        return message, data, status_code

    def search_username(self, table, info_user=[]):
        if len(info_user) > 0:
            filter_to_find = {'_id': info_user[0]}
            return self.find(table=table, filter_to_find=filter_to_find)

        return None

    def find(self, table, filter_to_find=None):
        objects = self.db[table]
        filter_db: object = filter_to_find if filter_to_find else {}

        for obj in objects.find(filter_db):
            return obj



