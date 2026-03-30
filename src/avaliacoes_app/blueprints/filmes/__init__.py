from flask import Blueprint

filmes_bp = Blueprint('filmes', __name__, url_prefix='/filmes')

from . import routes