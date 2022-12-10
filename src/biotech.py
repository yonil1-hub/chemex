from flask import Blueprint

biotech = Blueprint("biotech",
                    __name__,
                    url_prefix="/api/v1/biotech"
                   )