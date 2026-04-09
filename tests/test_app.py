import pytest
from src.avaliacoes_app import create_app
from src.avaliacoes_app.extensions import db
from src.avaliacoes_app.models import Usuario, Genero, Filme, Avaliacao

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'chave-de-teste'

@pytest.fixture
def client():
    app = create_app(TestConfig)
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


def test_listar_usuarios(client):
    usuario = Usuario(nome="Maria da Silva", email="maria@email.com")
    db.session.add(usuario)
    db.session.commit()

    resposta = client.get('/usuarios/')
    assert resposta.status_code == 200
    
    assert b"Maria da Silva" in resposta.data
    assert b"maria@email.com" in resposta.data


def test_cadastrar_usuario_com_sucesso(client):
    resposta = client.post('/usuarios/novo', data={
        'nome': 'Carlos Silva',
        'email': 'carlos@email.com'
    }, follow_redirects=True)
    
    assert resposta.status_code == 200

    assert "Usuário cadastrado com sucesso!" in resposta.text
    
    usuario_no_banco = Usuario.query.filter_by(email='carlos@email.com').first()
    assert usuario_no_banco is not None
    assert usuario_no_banco.nome == 'Carlos Silva'


def test_cadastrar_usuario_email_duplicado(client):
    usuario = Usuario(nome="Ana", email="ana@email.com")
    db.session.add(usuario)
    db.session.commit()
    
    resposta = client.post('/usuarios/novo', data={
        'nome': 'Outra Ana',
        'email': 'ana@email.com'
    }, follow_redirects=True)
    
    assert resposta.status_code == 200
    assert "Este e-mail já está sendo utilizado por outro usuário!" in resposta.text

def test_criar_avaliacao_nota_acima_do_limite(client):
    user = Usuario(nome="Pedro", email="pedro@teste.com")
    gen = Genero(nome="Ação")
    db.session.add_all([user, gen])
    db.session.commit()
    
    filme = Filme(titulo="Duro de Matar", ano_lancamento=1988, id_genero=gen.id_genero)
    db.session.add(filme)
    db.session.commit()

    resposta = client.post('/avaliacoes/nova', data={
        'id_usuario': user.id_usuario,
        'id_filme': filme.id_filme,
        'nota': '6'
    }, follow_redirects=True)
    
    assert "A nota deve ser um valor entre 1 e 5." in resposta.text
    avaliacoes = Avaliacao.query.all()
    assert len(avaliacoes) == 0 

def test_remover_usuario(client):
    usuario = Usuario(nome="Deletar Mim", email="delete@email.com")
    db.session.add(usuario)
    db.session.commit()
    
    id_usuario = usuario.id_usuario
    
    client.post(f'/usuarios/deletar/{id_usuario}', follow_redirects=True)
    
    usuario_apos_delete = db.session.get(Usuario, id_usuario)
    assert usuario_apos_delete is None
