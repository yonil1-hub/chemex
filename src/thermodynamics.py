from flask import Blueprint

thermodynamics = Blueprint("reaction",
                           __name__,
                           url_prefix="/api/v1/thermo"
                            )