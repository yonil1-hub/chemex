from flask import Flask
from os import environ
from .auth import auth
from .reaction import reaction
from .thermodynamics import thermodynamics
from .biotech import biotech
from .chemistry import chemistry
from .fluid import fluid
from .material import material
from .database import db



def create_app(test_config=None):

    app = Flask(__name__,
                instance_relative_config=True
                )
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=environ.get("SQLALCHEMY_DB_URI")
             
        )
    else:
        app.config.from_mapping(test_config)


    db.app=app
    db.init_app(app   )
    app.register_blueprint(auth)
    app.register_blueprint(reaction)
    app.register_blueprint(chemistry)
    app.register_blueprint(fluid)
    app.register_blueprint(thermodynamics)
    app.register_blueprint(material)
    app.register_blueprint(biotech)
    
    return app
