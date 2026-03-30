from flask import Blueprint

generos_bp = Blueprint('generos', __name__, url_prefix='/generos')

from . import routes
