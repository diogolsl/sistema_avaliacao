from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from ... extensions import db
from . import avaliacoes_bp
from ...models import Avaliacao, Filme, Usuario

@avaliacoes_bp.route('/', methods=['POST'])
def criar_avaliacao():
    data = request.get_json()

    if not data or not all(key in data for key in ('nota', 'filme_id', 'usuario_id')):
        return jsonify({'erro': 'Dados incompletos'}), 400
    
    try:
        nota = int(data['nota'])
        if nota < 1 or nota > 5:
            return jsonify({'erro': 'A nota deve ser entre 1 e 5'}), 400
    except ValueError:
        return jsonify({'erro': 'A nota deve ser um número inteiro'}), 400
    
    if not Usuario.query.get(data['usuario_id']):
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    if not Filme.query.get(data['filme_id']):
        return jsonify({'erro': 'Filme não encontrado'}), 404
    
    nova_avaliacao = Avaliacao(
        id_usuario=data['id_usuario'],
        id_filme=data['id_filme'],
        nota=nota
    )

    db.session.add(nova_avaliacao)

    try:
        db.session.commit()
        return jsonify({'mensagem': 'Avaliação criada com sucesso', 'id': nova_avaliacao.id_avaliacao}), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({'erro': 'Não é permitido criar uma avaliação duplicada'}), 409
    

@avaliacoes_bp.route('/<int:id_avaliacao>', methods=['GET'])
def listar_avaliacao(id_avaliacao):
    avaliacoes = Avaliacao.query.all()
    resultado = [
        {
            'id_avaliacao': avaliacao.id_avaliacao,
            'id_usuario': avaliacao.id_usuario,
            'id_filme': avaliacao.id_filme,
            'nota': avaliacao.nota
        }
        for avaliacao in avaliacoes
    ]
    return jsonify(resultado), 200


@avaliacoes_bp.route('/<int:id_avaliacao>', methods=['PUT'])
def atualizar_avaliacao(id_avaliacao):
    avaliacao = Avaliacao.query.get_or_404(id_avaliacao)
    data = request.get_json()

    if 'nota' in data:
        nota = int(data['nota'])
        if nota < 1 or nota > 5:
            return jsonify({'erro': 'A nota deve ser entre 1 e 5'}), 400
        avaliacao.nota = nota

    if 'comentario' in data:
        avaliacao.comentario = data['comentario']

    db.session.commit()
    return jsonify({'mensagem': 'Avaliação atualizada com sucesso'}), 200


@avaliacoes_bp.route('/<int:id_avaliacao>', methods=['DELETE'])
def deletar_avaliacao(id_avaliacao):
    avaliacao = Avaliacao.query.get_or_404(id_avaliacao)
    
    db.session.delete(avaliacao)
    db.session.commit()
    return jsonify({'mensagem': 'Avaliação deletada com sucesso'}), 200