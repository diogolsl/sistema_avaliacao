from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from ... extensions import db
from . import generos_bp
from ...models import Genero

@generos_bp.route('/', methods=['POST'])
def criar_genero():
    data = request.get_json()

    if not data or not data.get('nome'):
        return jsonify({'erro': 'Nome é obrigatório'}), 400
    
    if Genero.query.filter_by(nome=data['nome']).first():
        return jsonify({'erro': 'Gênero já cadastrado'}), 409

    novo_genero = Genero(nome=data['nome'])
    db.session.add(novo_genero)

    try:
        db.session.commit()
        return jsonify({"Mensagem": "Gênero cadastrado com sucesso!", "id": novo_genero.id_genero}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'erro': 'Esse gênero já está cadastrado'}), 500
    

@generos_bp.route('/', methods=['GET'])
def listar_generos():
    generos = Genero.query.all()
    resultado = [
        {
            "id_genero": genero.id_genero,
            "nome": genero.nome
        }
        for genero in generos
    ]
    return jsonify(resultado), 200

@generos_bp.route('/<int:id_genero>', methods=['GET'])
def buscar_genero(id_genero):
    genero = Genero.query.get_or_404(id_genero)
    return jsonify({
        'id_genero': genero.id_genero,
        'nome': genero.nome
    }), 200


@generos_bp.route('/<int:id_genero>', methods=['PUT'])
def atualizar_genero(id_genero):
    genero = Genero.query.get_or_404(id_genero)
    data = request.get_json()

    if not data:
        return jsonify({'erro': 'Dados incompletos'}), 400

    if 'nome' in data:
        genero.nome = data['nome']
    
    try:
        db.session.commit()
        return jsonify({'mensagem': 'Gênero atualizado com sucesso'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'erro': 'Esse gênero já está cadastrado'}), 409
    

@generos_bp.route('/<int:id_genero>', methods=['DELETE'])
def deletar_genero(id_genero):
    genero = Genero.query.get_or_404(id_genero)
    
    db.session.delete(genero)
    db.session.commit()
    return jsonify({'mensagem': 'Gênero deletado com sucesso'}), 200