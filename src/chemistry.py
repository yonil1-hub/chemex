from flask import (
                    Blueprint,
                    jsonify,
                    request
)
from .database import (
                        db,
                        Posts
)
from flask_jwt_extended import (
                                 get_jwt_identity,
                                 jwt_required,
                        
)

chemistry = Blueprint("chem",
                      __name__,
                      url_prefix="/api/v1/chem"  
                     )



# create post
@chemistry.route(
                  "/post",
                  methods=["POST"]
)
@jwt_required()
def createPost():
    required = ["title", "description", "body", "category"]

    postData = request.get_json()
    if not postData:
        return jsonify({"msg": "Not a JSON"}), 400
    # check if required data has been sent
    for key in required:
        if key not in postData.keys():
            return jsonify({"msg": "Missing {}".format(key)}), 400

    if Posts.query.filter_by(title=postData.get('title')).first() is not None:
        return jsonify({"msg" :"The title is already taken"}), 400

    # check the content of the post
    if len(postData.get('title')) < 15:
        return jsonify({"msg":"the title is too short"}), 400
    if len(postData.get('description')) < 30:
        return jsonify({"msg": "The description is too short"}), 400
    if len(postData.get('body')) < 100:
        return jsonify({"msg": "The body is too Short"}), 400

    id = get_jwt_identity()
    postData["userId"] = id

    post = Posts(**postData)
    db.session.add(post)
    db.session.commit()
    print(postData)

    return jsonify({"msg": "Post created sucessfully"}), 201

@chemistry.route(
                 "/posts"
)
def get_recent_posts():
    """returns recent five posts from our database"""
    posts = Posts.query.all()
    return jsonify({"posts":posts})

    

    
    
