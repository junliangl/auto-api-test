from flask import Blueprint

demo_blueprint = Blueprint("demo", __name__)


@demo_blueprint.post("/demo")
def demo():
    return "OK"
