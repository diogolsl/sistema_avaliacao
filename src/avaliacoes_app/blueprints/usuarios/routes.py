from flask import render_template, request, url_for, flash, redirect
from sqlalchemy.exc import IntegrityError
from . import usuarios_bp
from ...extensions import db
from ...models import Usuario

@usuarios_bp.route('/novo', methods=['POST'])
def criar_usuario():
    nome = request.form.get('nome')
    email = request.form.get('email')
    
    try:
        novo_usuario = Usuario(nome=nome, email=email)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Este e-mail já está sendo utilizado por outro usuário!', 'error')
        
    return redirect(url_for('usuarios_bp.listar_usuarios'))

@usuarios_bp.route('/', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()

    return render_template('usuarios.html', usuarios=usuarios)

@usuarios_bp.route('/editar/<int:id_usuario>', methods=['POST'])
def atualizar_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    
    nome = request.form.get('nome')
    email = request.form.get('email')
    
    if nome and email:
        try:
            usuario.nome = nome
            usuario.email = email
            db.session.commit()
            flash('Usuário atualizado com sucesso!', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Este e-mail já está em uso.', 'error')

    return redirect(url_for('usuarios_bp.listar_usuarios'))


@usuarios_bp.route('/deletar/<int:id_usuario>', methods=['POST'])
def deletar_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('usuarios_bp.listar_usuarios'))
