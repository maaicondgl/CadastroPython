from flask_sqlalchemy import SQLAlchemy
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
db = SQLAlchemy()

def init_app(app):
    db_user = DB_USER
    db_password = DB_PASSWORD
    db_host = DB_HOST
    db_port = DB_PORT
    db_name = DB_NAME

    # Configura a URI do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o SQLAlchemy com o app
    db.init_app(app)

    # Importa os modelos aqui para evitar ciclos de importação
    from models.customer import CustomerModel

    # Cria as tabelas no banco de dados
    with app.app_context():
        db.create_all()

    print('Tabelas criadas no banco de dados.')

    return db