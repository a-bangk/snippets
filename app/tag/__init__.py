from flask import Blueprint

tag_bp = Blueprint('tag_bp', __name__)

from app.tag import tag


