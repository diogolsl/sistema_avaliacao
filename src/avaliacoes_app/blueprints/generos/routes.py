from flask import request, render_template, url_for, flash, redirect
from sqlalchemy.exc import IntegrityError
from ... extensions import db
from . import generos_bp
from ...models import Genero

@generos_bp.route('/novo', methods=['POST'])
def criar_genero():
    nome = request.form.get('nome')
    
    try:
        novo_genero = Genero(nome=nome)
        db.session.add(novo_genero)
        db.session.commit()
        flash('Gênero cadastrado com sucesso!', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Este gênero já está cadastrado!', 'error')
        
    return redirect(url_for('generos.listar_generos'))

@generos_bp.route('/', methods=['GET'])
def listar_generos():
    generos = Genero.query.all()
    return render_template('generos/generos.html', generos=generos)

@generos_bp.route('/editar/<int:id_genero>', methods=['POST'])
def atualizar_genero(id_genero):
    genero = Genero.query.get_or_404(id_genero)
    novo_nome = request.form.get('nome')
    
    if novo_nome:
        try:
            genero.nome = novo_nome
            db.session.commit()
            flash('Gênero atualizado com sucesso!', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Já existe um gênero com este nome.', 'error')
            
    return redirect(url_for('generos.listar_generos'))

@generos_bp.route('/deletar/<int:id_genero>', methods=['POST'])
def deletar_genero(id_genero):
    genero = Genero.query.get_or_404(id_genero)

    db.session.delete(genero)
    db.session.commit()
    flash('Gênero excluído com sucesso!', 'success')
    return redirect(url_for('generos.listar_generos'))