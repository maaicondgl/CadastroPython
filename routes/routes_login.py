from flask import Blueprint, request, render_template, redirect, url_for, session, current_app
from flask_jwt_extended import create_access_token
from models.customer import CustomerModel
from resources.cadastro import UserLogin

login_bp = Blueprint('login',__name__)

@login_bp.route('/index')
def index():
    return render_template('index.html')


@login_bp.route('/profile/<string:userId>')
def profile(userId):

    customer = CustomerModel.find_customer(userId)    
    
    if customer:
        username = customer.name
        user_rg = customer.rg
        user_cpf =  customer.cpf

        return render_template('profile.html', name=username, rg=user_rg, cpf=user_cpf)
    else:
        return 'Usuário não encontrado'

@login_bp.route('/logout')
def logout():
    # Limpa todos os dados da sessão
    session.clear()
   
    return render_template('index.html')

@login_bp.route('/register')
def register():
   
    return render_template('register.html')

