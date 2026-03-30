from .extensions import db

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    avaliacoes = db.relationship('Avaliacao', backref='autor', cascade='all, delete-orphan', lazy=True)

class Genero(db.Model):
    __tablename__ = 'genero'

    id_genero = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)

    filmes = db.relationship('Filme', backref='categoria', lazy=True)

class Filme(db.Model):
    __tablename__ = 'filme'

    id_filme = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    ano_lancamento = db.Column(db.Integer, nullable=False)
    sinopse = db.Column(db.Text, nullable=True)
    id_genero = db.Column(db.Integer, db.ForeignKey('genero.id_genero', ondelete='SET NULL'), nullable=True)

    avaliacoes = db.relationship('Avaliacao', backref='filme_avaliado', cascade='all, delete-orphan', lazy=True)

class Avaliacao(db.Model):
    __tablename__ = 'avaliacao'

    id_avaliacao = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario', ondelete='CASCADE'), nullable=False)
    id_filme = db.Column(db.Integer, db.ForeignKey('filme.id_filme', ondelete='CASCADE'), nullable=False)
    nota = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('id_usuario', 'id_filme', name='uk_usuario_filme'),
        db.CheckConstraint('nota >= 1 AND nota <= 5', name='check_nota_range')
    )
