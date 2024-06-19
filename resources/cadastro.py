from flask import request
from flask_restful import Resource, reqparse
from models.customer import CustomerModel
from flask_jwt_extended import create_access_token
from flask_login import login_user

from models.customer import User
atributos = reqparse.RequestParser();
atributos.add_argument('userName', type=str, required=True);
atributos.add_argument('password', type=str, required=True);

class CustomerList(Resource):
    def get(self):
        
        customerList =  CustomerModel.allCustomer();
        if not customerList:
            return {'message': 'Não existe cadastros'}, 500
        else:
            return {'cadastro': [customer.json() for customer in customerList]};

class CustomerCreate(Resource):
    argumentos = reqparse.RequestParser();
    argumentos.add_argument('name',type=str, required=True);
    argumentos.add_argument('rg', type=str, required=True);
    argumentos.add_argument('cpf', type=str, required=True);
    argumentos.add_argument('userName', type=str, required=True);
    argumentos.add_argument('password', type=str, required=True);

    def post(self):
        dados = CustomerCreate.argumentos.parse_args()
        customer = CustomerModel(**dados)
        try:
            if customer.findCustomerByUsername(dados['userName']):
                return {'message': 'Erro ao criar Customer: userName already exists'.format(dados['userName'])}, 500
            else:
                customer.createCustomer()
                return customer.json(), 200
        except Exception as e:
            return {'message': f'Erro ao criar Customer: {str(e)}'}, 500

class CustomerSearch(Resource):
    def get(self, userId):
        customer = CustomerModel.find_customer(userId)
        if customer:
            return customer.json();
        else:
            return {'message': 'cadastro não encontrado'}, 404;

class CustomerUpdate(Resource):
    def put(self, userId):
        argumentos = reqparse.RequestParser();
        argumentos.add_argument('name',type=str, required=True);
        argumentos.add_argument('rg', type=str, required=True);
        argumentos.add_argument('cpf', type=str, required=True);

        dados = argumentos.parse_args();
        userRegistered = CustomerModel.find_customer(userId);

        if userRegistered:
            userRegistered.updateCustomer(**dados)
            userRegistered.saveCustomer()
            return userRegistered.json(), 200
        else: 
            return {'message': 'cadastro não encontrado'}, 404

class CustomerDelete(Resource):
    def delete(self, userId):
        customer =  CustomerModel.find_customer(userId);

        if customer is None or customer == '':
            return{'message': 'Customer não encontrado'}, 400;
        else:
            customer.deleteCustomer()
            return{'message': 'Cadastro deletado com sucesso'}, 200;

class userLogin(Resource):
    @classmethod
    def post(cls):
        dados = request.get_json()
        username = dados.get('userName')
        password = dados.get('password')

        user = CustomerModel.findCustomerByUsername(username)

        if user and user.password == password:
            user_obj = User(username)
            login_user(user_obj)
            token_access = create_access_token(identity=user.userId)
            return {'access_token': token_access}, 200
        else:
            return {'message': 'Usuário ou senha incorretos'}, 401
