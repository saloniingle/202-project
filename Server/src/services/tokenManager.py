import jwt
import os


def get_id_from_token(token):
    data = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
    id = data["user_id"]
    return id


def get_role_from_token(token):
    data = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
    id = data["role"]
    return id
