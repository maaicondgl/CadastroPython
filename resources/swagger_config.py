from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger, swag_from
from flask_jwt_extended import create_access_token
from flask_login import login_user

from models.customer import CustomerModel, User
app = Flask(__name__)
api = Api(app)

def configure_swagger(app):
    template = {
        "swagger": "2.0",
        "info": {
            "title": "Cadastro API",
            "description": "API para gerenciar cadastros de clientes",
            "version": "1.0.0",
            "contact": {
                "name": "MD",
                "email": "maaicondgl@outlook.com"
            }
        },
        "tags": [
            {"name": "Operações de Cadastros", "description": "Operações CRUD para cadastros de clientes"}
        ]
    }
    Swagger(app, template=template)


class CustomerList(Resource):

    @swag_from({
        'tags': ['Operações de Cadastros'],
        'summary': 'Lista todos os clientes cadastrados',
        'responses': {
            200: {
                'description': 'Lista de clientes',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'cadastro': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'name': {'type': 'string'},
                                    'rg': {'type': 'string'},
                                    'cpf': {'type': 'string'},
                                    'userName': {'type': 'string'}
                                }
                            }
                        }
                    }
                }
            },
            500: {
                'description': 'Erro interno no servidor',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def get(self):
        customerList = CustomerModel.all_customer()
        if not customerList:
            return {'message': 'Não existem cadastros'}, 500
        else:
            return {'cadastro': [customer.json() for customer in customerList]}

class CustomerCreate(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('name', type=str, required=True)
    argumentos.add_argument('rg', type=str, required=True)
    argumentos.add_argument('cpf', type=str, required=True)
    argumentos.add_argument('userName', type=str, required=True)
    argumentos.add_argument('password', type=str, required=True)

    @swag_from({
        'tags': ['Operações de Cadastros'],
        'summary': 'Cria um novo cliente',
        'parameters': [
            {
                'in': 'body',
                'name': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'rg': {'type': 'string'},
                        'cpf': {'type': 'string'},
                        'userName': {'type': 'string'},
                        'password': {'type': 'string'}
                    }
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Cliente criado com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'rg': {'type': 'string'},
                        'cpf': {'type': 'string'},
                        'userName': {'type': 'string'}
                    }
                }
            },
            500: {
                'description': 'Erro interno no servidor',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def post(self):
        dados = CustomerCreate.argumentos.parse_args()
        customer = CustomerModel(**dados)
        try:
            if customer.find_customer_by_username(dados['userName']):
                return {'message': f'Erro ao criar Customer: userName {dados["userName"]} já existe'}, 500
            else:
                customer.create_customer()
                return customer.json(), 200
        except Exception as e:
            return {'message': f'Erro ao criar Customer: {str(e)}'}, 500

class CustomerSearch(Resource):
    @swag_from({
        'tags': ['Operações de Cadastros'],
        'summary': 'Busca um cliente por ID',
        'parameters': [
            {
                'name': 'userId',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'ID do cliente a ser buscado'
            }
        ],
        'responses': {
            200: {
                'description': 'Cliente encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'rg': {'type': 'string'},
                        'cpf': {'type': 'string'},
                        'userName': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Cliente não encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def get(self, userId):
        customer = CustomerModel.find_customer(userId)
        if customer:
            return customer.json()
        else:
            return {'message': 'cadastro não encontrado'}, 404

class CustomerUpdate(Resource):
    @swag_from({
        'tags': ['Operações de Cadastros'],
        'summary': 'Atualiza um cliente por ID',
        'parameters': [
            {
                'name': 'userId',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'ID do cliente a ser atualizado'
            },
            {
                'in': 'body',
                'name': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'rg': {'type': 'string'},
                        'cpf': {'type': 'string'}
                    }
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Cliente atualizado com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'rg': {'type': 'string'},
                        'cpf': {'type': 'string'},
                        'userName': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Cliente não encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def put(self, userId):
        dados = request.get_json()
        userRegistered = CustomerModel.find_customer(userId)
        if userRegistered:
            name = dados.get('name')
            rg = dados.get('rg')
            cpf = dados.get('cpf')
            userRegistered.update_customer(name, rg, cpf)
            return userRegistered.json(), 200
        else:
            return {'message': 'cadastro não encontrado'}, 404

class CustomerDelete(Resource):
    @swag_from({
        'tags': ['Operações de Cadastros'],
        'summary': 'Deleta um cliente por ID',
        'parameters': [
            {
                'name': 'userId',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'ID do cliente a ser deletado'
            }
        ],
        'responses': {
            200: {
                'description': 'Cliente deletado com sucesso'
            },
            400: {
                'description': 'Cliente não encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def delete(self, userId):
        customer = CustomerModel.find_customer(userId)
        if customer:
            customer.delete_customer()
            return {'message': 'Cadastro deletado com sucesso'}, 200
        else:
            return {'message': 'Customer não encontrado'}, 400
        
class search_partial(Resource):
    @swag_from({
        'tags': ['Operações de Cadastros'],
        'summary': 'Busca clientes por nome parcial',
        'parameters': [
            {
                'name': 'name',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'Nome parcial do cliente'
            }
        ],
        'responses': {
            200: {
                'description': 'Lista de clientes encontrados',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'name': {'type': 'string'},
                            'rg': {'type': 'string'},
                            'cpf': {'type': 'string'}
                        }
                    }
                }
            },
            404: {
                'description': 'Nenhum cliente encontrado com o nome parcial fornecido',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def get(self, name):
        customers = CustomerModel.search_by_partial_name(name)
        if customers:
            return ([customer.json() for customer in customers]), 200
        else:
            return {'message': 'Nenhum cadastro encontrado'}, 404

class UserLogin(Resource):
    @swag_from({
        'tags': ['Operações de Cadastros'],
        'summary': 'Realiza o login do usuário',
        'parameters': [
            {
                'in': 'body',
                'name': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'userName': {'type': 'string'},
                        'password': {'type': 'string'}
                    }
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Login realizado com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'userId': {'type': 'string'},
                        'userName': {'type': 'string'},
                        'access_token': {'type': 'string'}
                    }
                }
            },
            401: {
                'description': 'Credenciais inválidas',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def post(cls):
        dados = request.get_json()
        username = dados.get('userName')
        password = dados.get('password')

        user_info = CustomerModel.find_customer_by_username(username)

        if user_info and user_info.get('userId'):
            user_obj = User(username)
            login_user(user_obj)

            access_token = create_access_token(identity=str(user_info['userId']))

            return {'userId': str(user_info['userId']), 'userName': user_info['userName'], 'access_token': access_token}, 200
        else:
            return {'message': 'Usuário ou senha incorretos'}, 401