from flask import request, render_template, url_for, flash, redirect
from sqlalchemy.exc import IntegrityError
from ...extensions import db
from . import avaliacoes_bp
from ...models import Avaliacao, Filme, Usuario

@avaliacoes_bp.route('/avaliar/<int:id_filme>', methods=['GET'])
def tela_avaliar(id_filme):
    filme = Filme.query.get_or_404(id_filme)
    usuarios = Usuario.query.all()
    
    return render_template('filmes/avaliar.html', filme=filme, usuarios=usuarios)

@avaliacoes_bp.route('/nova', methods=['POST'])
def criar_avaliacao():
    id_usuario = request.form.get('id_usuario')
    id_filme = request.form.get('id_filme')
    nota_str = request.form.get('nota')

    try:
        nota = int(nota_str)
        if nota < 1 or nota > 5:
            flash('A nota deve ser um valor entre 1 e 5.', 'error')
            return redirect(url_for('avaliacoes.listar_avaliacoes', id_filme=id_filme))
    except (ValueError, TypeError):
        flash('Nota inválida. Por favor, insira um número inteiro.', 'error')
        return redirect(url_for('avaliacoes.listar_avaliacoes', id_filme=id_filme))

    try: 
        nova_avaliacao = Avaliacao(
            id_usuario=id_usuario,
            id_filme=id_filme,
            nota=nota
        )
        db.session.add(nova_avaliacao)
        db.session.commit()
    
        flash('Avaliação registrada com sucesso!', 'success')
        return redirect(url_for('avaliacoes.listar_avaliacoes', id_filme=id_filme))
        
    except IntegrityError:
        db.session.rollback()
        flash('Você já avaliou este filme anteriormente!', 'error')
        return redirect(url_for('avaliacoes.listar_avaliacoes', id_filme=id_filme))
    
@avaliacoes_bp.route('/', methods=['GET'])
def listar_avaliacoes():
    avaliacoes = Avaliacao.query.all()
    return render_template('filmes/avaliar.html', avaliacoes=avaliacoes)

@avaliacoes_bp.route('/editar/<int:id_avaliacao>', methods=['POST'])
def atualizar_avaliacao(id_avaliacao):
    avaliacao = Avaliacao.query.get_or_404(id_avaliacao)
    id_filme = avaliacao.id_filme

    nota_str = request.form.get('nota')
    if nota_str:
        try:
            nota = int(nota_str)
            if nota < 1 or nota > 5:
                flash('A nota deve ser entre 1 e 5.', 'error')
                return redirect(url_for('avaliacoes.listar_avaliacoes', id_filme=id_filme))
            
            avaliacao.nota = nota
            db.session.commit()
            flash('Avaliação atualizada com sucesso!', 'success')
            
        except ValueError:
            flash('Nota inválida. Por favor, insira um número inteiro.', 'error')
            
    return redirect(url_for('avaliacoes.listar_avaliacoes', id_filme=id_filme))

@avaliacoes_bp.route('/deletar/<int:id_avaliacao>', methods=['POST'])
def deletar_avaliacao(id_avaliacao):
    avaliacao = Avaliacao.query.get_or_404(id_avaliacao)
    id_filme = avaliacao.id_filme

    db.session.delete(avaliacao)
    db.session.commit()

    flash('Avaliação deletada com sucesso!', 'success')
    return redirect(url_for('avaliacoes.listar_avaliacoes', id_filme=id_filme))