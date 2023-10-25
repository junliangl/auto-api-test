from flask import Blueprint

from .demo import demo_blueprint

common_query_blueprint = Blueprint("common_query", __name__)

common_query_blueprint.register_blueprint(demo_blueprint)
