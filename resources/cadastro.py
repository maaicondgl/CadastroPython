from flask import request, jsonify
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
        
        customerList =  CustomerModel.all_customer();
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
            if customer.find_customer_by_username(dados['userName']):
                return {'message': 'Erro ao criar Customer: userName already exists'.format(dados['userName'])}, 500
            else:
                customer.create_customer()
                return customer.json(), 200
        except Exception as e:
            return {'message': f'Erro ao criar Customer: {str(e)}'}, 500

class CustomerSearch(Resource):
    def get(self, userId):
        customer = CustomerModel.find_customer(userId)
        if customer:
            return jsonify(customer.json()), 200 
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
            userRegistered.update_customer(**dados)
            userRegistered.save_customer()
            return userRegistered.json(), 200
        else: 
            return {'message': 'cadastro não encontrado'}, 404

class CustomerDelete(Resource):
    def delete(self, userId):
        customer =  CustomerModel.find_customer(userId);

        if customer is None or customer == '':
            return{'message': 'Customer não encontrado'}, 400;
        else:
            customer.delete_customer()
            return{'message': 'Cadastro deletado com sucesso'}, 200;

   
class search_partial(Resource):
    def get(self, name):
        customers = CustomerModel.search_by_partial_name(name)
        if customers:
            return [customer.json() for customer in customers], 200
        else:
            return {'message': 'Nenhum cadastro encontrado'}, 404

class UserLogin(Resource):
    def post(self):

        dados = request.get_json()

        if 'userName' not in dados or 'password' not in dados:
            return {'message': 'Usuário e senha são obrigatórios'}, 400

        username = dados['userName']
        password = dados['password']

        user_info = CustomerModel.find_customer_by_username(username)

        if user_info:
            userid = user_info['userId']

            user = CustomerModel.find_customer(userid)
            if user and user.password == password:

                access_token = create_access_token(identity=str(userid))
                
                return {'userId': str(userid), 'userName': user_info['userName'], 'access_token': access_token}, 200
            else:
                return {'message': 'Usuário ou senha incorretos'}, 401
        else:
            return {'message': 'Usuário não encontrado'}, 404