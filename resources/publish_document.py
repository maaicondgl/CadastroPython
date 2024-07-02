from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from models.customer import NotepadModel

class CreateDocument(Resource):
    @jwt_required()  # Requer autenticação JWT para acessar este endpoint
    def post(self):
        dados = request.get_json()
        text = dados.get('text')

        # Obtém o userId do cliente autenticado através do token JWT
        customer_id = get_jwt_identity()

        # Cria uma instância de NotepadModel com os dados recebidos e o userId do cliente
        notepad = NotepadModel(text=text, customer_id=customer_id)
        
        # Salva o documento no banco de dados
        notepad.save_text()

        return notepad.json(), 200
