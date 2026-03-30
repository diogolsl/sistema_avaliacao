from flask import Blueprint

avaliacoes_bp = Blueprint('avaliacoes', __name__, url_prefix='/avaliacoes')

from . import routes