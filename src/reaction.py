from flask import Blueprint

reaction = Blueprint("reaction",
                     __name__,
                     url_prefix="/api/v1/reaction"
                    )
@reaction.get("/all")
def all():
    return {
        "post_ui":1,
        "author":"Yaekob Demisse",
        "title":"Batch reaction",
        "body":"this is tutoril about batch reactor"
    }