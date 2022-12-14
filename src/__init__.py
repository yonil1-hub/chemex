from flask import Flask
from flask_cors import CORS
from os import environ
from flask_jwt_extended import JWTManager
from datetime import timedelta
from .auth import auth
from .reaction import reaction
from .thermodynamics import thermodynamics
from .biotech import biotech
from .chemistry import chemistry
from .fluid import fluid
from .material import material
from .database import db



def create_app(test_config=None):
    """
        configration for appilication
    """

    app = Flask(__name__,
                instance_relative_config=True
                )
    if test_config is None:
        app.config.from_mapping(
            dbUsername = "",
            dbPassword= "",
            dbname = "",
            SECRET_KEY=environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=environ.get("SQLALCHEMY_DATABASE_URI"),
            JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1),
            JWT_SECRET_KEY=environ.get('JWT_SECRET_KEY')
             
        )
    else:
        app.config.from_mapping(test_config)

    cors = CORS(app)
    db.app=app
    JWTManager(app)
    db.init_app(app)
    app.url_map.strict_slashes = False
    app.register_blueprint(auth)
    app.register_blueprint(reaction)
    app.register_blueprint(chemistry)
    app.register_blueprint(fluid)
    app.register_blueprint(thermodynamics)
    app.register_blueprint(material)
    app.register_blueprint(biotech)
    
    return app
