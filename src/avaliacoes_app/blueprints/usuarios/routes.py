from flask import request, jsonify
from . import usuarios_bp
from ...extensions import db
from ...models import Usuario

@usuarios_bp.route('/', methods=['POST'])
def criar_usuario():
    data = request.get_json()
    if not data or not data.get('nome') or not data.get('email'):
        return jsonify({'erro': 'Dados incompletos'}), 400
    
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'erro': 'Email já cadastrado'}), 409
    
    novo_usuario = Usuario(
        nome=data['nome'],
        email=data['email']
    )

    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"Mensagem": "Usuário criado com sucesso!", "id": novo_usuario.id_usuario}), 201

@usuarios_bp.route('/<int:id_usuario>', methods=['GET'])
def buscar_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    return jsonify({
        'id_usuario': usuario.id_usuario,
        'nome': usuario.nome,
        'email': usuario.email
    }),200

@usuarios_bp.route('/<int:id_usuario>', methods=['PUT'])
def atualizar_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    data = request.get_json()

    if not data:
        return jsonify({'erro': 'Dados incompletos'}), 400

    if 'nome' in data:
        usuario.nome = data['nome']
        
    if 'email' in data:
        if Usuario.query.filter_by(email=data['email']).first():
            return jsonify({'erro': 'Email já cadastrado'}), 409
        usuario.email = data['email']

    db.session.commit()
    return jsonify({"Mensagem": "Usuário atualizado com sucesso!"}), 200

@usuarios_bp.route('/<int:id_usuario>', methods=['DELETE'])
def deletar_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"Mensagem": "Usuário deletado com sucesso!"}), 200
