from flask import Blueprint

material = Blueprint("material",
                     __name__,
                     url_prefix="/api/v1/material"
                    )