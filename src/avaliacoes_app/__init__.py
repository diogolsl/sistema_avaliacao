from flask import Flask, render_template
from .extensions import db, migrate
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import models
        
        from .blueprints.usuarios import usuarios_bp
        from .blueprints.filmes import filmes_bp
        from .blueprints.avaliacoes import avaliacoes_bp
        from .blueprints.generos import generos_bp

        app.register_blueprint(usuarios_bp)
        app.register_blueprint(filmes_bp)
        app.register_blueprint(avaliacoes_bp)
        app.register_blueprint(generos_bp)

    return app