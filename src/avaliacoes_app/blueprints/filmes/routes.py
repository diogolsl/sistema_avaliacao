from flask import request, render_template, url_for, flash, redirect
from . import filmes_bp
from ...extensions import db
from ...models import Filme, Genero

@filmes_bp.route('/novo', methods=['POST'])
def criar_filme():
    titulo = request.form.get('titulo')
    ano_lancamento = request.form.get('ano_lancamento')
    sinopse = request.form.get('sinopse')
    id_genero = request.form.get('id_genero')
    
    try:
        novo_filme = Filme(
            titulo=titulo,
            ano_lancamento=int(ano_lancamento),
            sinopse=sinopse,
            id_genero=id_genero if id_genero else None
        )
        db.session.add(novo_filme)
        db.session.commit()
        flash('Filme cadastrado com sucesso!', 'success')
    except ValueError:
        flash('Ano de lançamento inválido.', 'error')
        
    return redirect(url_for('filmes.listar_filmes'))

@filmes_bp.route('/', methods=['GET'])
def listar_filmes():
    filmes = Filme.query.all()
    generos = Genero.query.all()
    return render_template('index.html', filmes=filmes, generos=generos)

@filmes_bp.route('/editar/<int:id_filme>', methods=['POST'])
def atualizar_filme(id_filme):
    filme = Filme.query.get_or_404(id_filme)
    
    filme.titulo = request.form.get('titulo')
    filme.sinopse = request.form.get('sinopse')
    ano_str = request.form.get('ano_lancamento')

    if ano_str:
        try:
            filme.ano_lancamento = int(ano_str)
        except ValueError:
            flash('Ano de lançamento inválido.', 'error')
            return redirect(url_for('filmes.listar_filmes'))
            
    id_genero = request.form.get('id_genero')
    if id_genero:
        filme.id_genero = id_genero

    db.session.commit()
    flash('Filme atualizado com sucesso!', 'success')
    return redirect(url_for('filmes.listar_filmes'))

@filmes_bp.route('/deletar/<int:id_filme>', methods=['POST'])
def deletar_filme(id_filme):
    filme = Filme.query.get_or_404(id_filme)

    db.session.delete(filme)
    db.session.commit()
    flash('Filme excluído com sucesso!', 'success')
    return redirect(url_for('filmes.listar_filmes'))