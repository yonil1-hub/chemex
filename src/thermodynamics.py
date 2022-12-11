from flask import Blueprint, jsonify

thermodynamics = Blueprint("thermodynamics",
                           __name__,
                           url_prefix="/api/v1/thermo"
                            )

@thermodynamics.get("/all")
def all():
    """
        this will retrieve all posts from database
    """
    return jsonify({"title":"thermodynamics"})