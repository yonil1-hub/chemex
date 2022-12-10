from flask import Blueprint

fluid = Blueprint("fluid",
                  __name__,
                  url_prefix="/api/v1/fluid"  
                 )