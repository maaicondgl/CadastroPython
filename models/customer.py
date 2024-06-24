import uuid
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from db.db import db


class CustomerModel(db.Model):
    __tablename__ = 'usuarios'
    userId = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(80))
    rg = db.Column(db.String(10), unique=True)
    cpf = db.Column(db.String(11), unique=True)
    userName = db.Column(db.String(30))
    password = db.Column(db.String(40))

    def __init__(self, name, rg, cpf, userName, password) -> None:
        self.userId = str(uuid.uuid4())
        self.name = name
        self.rg = rg
        self.cpf = cpf
        self.userName = userName
        self.password = password

    def json(self):
        return {
            'userId': self.userId,
            'name': self.name,
            'rg': self.rg,
            'cpf': self.cpf,
            'userName': self.userName,
            'password': self.password
        }

    @classmethod
    def findCustomerByUsername(cls, userName):
        return cls.query.filter_by(userName=userName).first()

    @classmethod
    def find_customer(cls, userId):
        return cls.query.filter_by(userId=userId).first()

    def createCustomer(self):
        if CustomerModel.query.filter_by(rg=self.rg).first():
            raise ValueError(f"RG '{self.rg}' já está em uso por outro usuário.")
        
        if CustomerModel.query.filter_by(cpf=self.cpf).first():
            raise ValueError(f"CPF '{self.cpf}' já está em uso por outro usuário.")
        
        db.session.add(self)
        db.session.commit()

        # Cria e salva o usuário associado
        new_user = User(
            userName=self.userName
        )
        new_user.set_password(self.password)

        db.session.add(new_user)
        db.session.commit()

    def updateCustomer(self, name, rg, cpf):
        if rg != self.rg and CustomerModel.query.filter_by(rg=rg).first():
            raise ValueError(f"RG '{rg}' já está em uso por outro usuário.")
        
        if cpf != self.cpf and CustomerModel.query.filter_by(cpf=cpf).first():
            raise ValueError(f"CPF '{cpf}' já está em uso por outro usuário.")

        self.name = name
        self.rg = rg
        self.cpf = cpf

    def saveCustomer(self):
        db.session.add(self)
        db.session.commit()

    def deleteCustomer(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def allCustomer(cls):
        return cls.query.all()

    @classmethod
    def search_by_partial_name(cls, partial_name):
        return cls.query.filter(cls.name.ilike(f"%{partial_name}%")).all()
    
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def __init__(self, userName):
        self.userName = userName

    def __repr__(self):
        return f"User(id={self.id}, userName='{self.userName}')"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(userName=username).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.get(user_id)
