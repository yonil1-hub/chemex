from flask import Flask
from os import environ
from src.auth import auth
from src.reaction import reaction
from src.thermodynamics import thermodynamics
from src.biotech import biotech
from src.chemistry import chemistry
from src.fluid import fluid
from src.material import material




def create_app(test_config=None):

    app = Flask(__name__,
                instance_relative_config=True
                )
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=environ.get("SECRET_KEY")
        )
    else:
        app.config.from_mapping(test_config)

    app.register_blueprint(auth)
    app.register_blueprint(reaction)
    app.register_blueprint(chemistry)
    app.register_blueprint(fluid)
    app.register_blueprint(thermodynamics)
    app.register_blueprint(material)
    app.register_blueprint(biotech)
    
    return app
