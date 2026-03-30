from flask import request, jsonify
from . import filmes_bp
from ...extensions import db
from ...models import Filme, Genero

@filmes_bp.route('/', methods=['POST'])
def criar_filme():
    data = request.get_json()
    if not data or not data.get('titulo'):
        return jsonify({'erro': 'Título é obrigatório'}), 400
    
    if Filme.query.filter_by(titulo=data['titulo']).first():
        return jsonify({'erro': 'Filme já cadastrado'}), 409
    
    id_genero = data.get('id_genero')
    if id_genero:
        genero_existe = Genero.query.get(id_genero)
        if not genero_existe:
            return jsonify({'erro': 'Gênero não encontrado'}), 404

    novo_filme = Filme(
        titulo=data['titulo'],
        sinopse=data.get('sinopse'),
        ano_lancamento=data.get('ano_lancamento'),
        genero_id=id_genero
    )

    db.session.add(novo_filme)
    db.session.commit()
    return jsonify({"Mensagem": "Filme cadastrado com sucesso!", "id": novo_filme.id_filme}), 201


@filmes_bp.route('/', methods=['GET'])
def listar_filmes():
    filmes = Filme.query.all()
    resultado = [
        {
            "id_filme": filme.id_filme,
            "titulo": filme.titulo,
            "ano_lancamento": filme.ano_lancamento,
            "sinopse": filme.sinopse,
            "id_genero": filme.id_genero
        }
        for filme in filmes
    ]
    return jsonify(resultado), 200

@filmes_bp.route('/<int:id_filme>', methods=['GET'])
def buscar_filme(id_filme):
    filme = Filme.query.get_or_404(id_filme)
    return jsonify({
        'id_filme': filme.id_filme,
        'titulo': filme.titulo,
        'sinopse': filme.sinopse,
        'ano_lancamento': filme.ano_lancamento,
        'id_genero': filme.id_genero
    }), 200


@filmes_bp.route('/<int:id_filme>', methods=['PUT'])
def atualizar_filme(id_filme):
    filme = Filme.query.get_or_404(id_filme)
    data = request.get_json()

    if not data:
        return jsonify({'erro': 'Dados incompletos'}), 400

    if 'titulo' in data:
        filme.titulo = data['titulo']
        
    if 'sinopse' in data:
        filme.sinopse = data['sinopse']
        
    if 'ano_lancamento' in data:
        filme.ano_lancamento = data['ano_lancamento']
        
    if 'id_genero' in data:
        id_genero = data['id_genero']
        genero_existe = Genero.query.get(id_genero)
        if not genero_existe:
            return jsonify({'erro': 'Gênero não encontrado'}), 404
        filme.id_genero = id_genero

    db.session.commit()
    return jsonify({"Mensagem": "Filme atualizado com sucesso!"}), 200


@filmes_bp.route('/<int:id_filme>', methods=['DELETE'])
def deletar_filme(id_filme):
    filme = Filme.query.get_or_404(id_filme)

    db.session.delete(filme)
    db.session.commit()
    return jsonify({"Mensagem": "Filme deletado com sucesso!"}), 200

