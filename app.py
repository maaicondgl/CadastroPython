from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from db.db import init_app
from resources.cadastro import CustomerList, CustomerCreate, CustomerSearch, CustomerDelete, CustomerUpdate, userLogin


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
api = Api(app)
jtw = JWTManager(app)

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Inicializa o SQLAlchemy e obtém o objeto db
db = init_app(app)

class User:
    def __init__(self, user_id):
        self.id = user_id

    def get_id(self):
        return str(self.id)

# Função para carregar usuário a partir do ID
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Adiciona os recursos da API
api.add_resource(CustomerList, '/cadastros')
api.add_resource(CustomerCreate, '/cadastros/create')
api.add_resource(CustomerSearch, '/cadastros/search/<string:userId>')
api.add_resource(CustomerDelete, '/cadastros/delete/<string:userId>')
api.add_resource(CustomerUpdate, '/cadastros/update/<string:userId>')
api.add_resource(userLogin, '/login')

if __name__ == '__main__':
    app.run(debug=True, port=3033)