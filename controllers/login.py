import os
from datetime import timedelta
from flask import Flask, request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, create_access_token
from sqlalchemy.orm import sessionmaker
from passlib.hash import pbkdf2_sha256 as sha256

from connection import Base, engine
from models import User


class loginAPI(Resource):
    def get(self):
        session = sessionmaker(bind=engine)()
        data = request.json
        user = session.query(User).filter(
            User.user == data['user']).one_or_none()
        if user is not None:
            if sha256.verify(data['pass'], user.password):
                expires = timedelta(days=3)
                access_token = create_access_token(
                    identity=user.id, expires_delta=expires)
                return {'token': access_token}
            else:
                return {}
        else:
            return {}
