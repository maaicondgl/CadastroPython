from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db_user = 'postgres'
    db_password = 'postgres1234'
    db_host = 'localhost'
    db_port = '5432'
    db_name = 'api_python_cadastro'

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