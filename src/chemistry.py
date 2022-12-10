from flask import Blueprint

chemistry = Blueprint("chem",
                      __name__,
                      url_prefix="/api/v1/chem"  
                     )