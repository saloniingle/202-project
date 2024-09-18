from flask import Blueprint

bp1 = Blueprint("Hello World", __name__)


@bp1.route("/")
def hello_world():
    return {"message": "This is defualt route"}
