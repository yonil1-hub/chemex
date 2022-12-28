"""
Handles user actions on post
"""

from flask import Blueprint, request, jsonify
from .database import db,Users, Posts, Replies, Comments


userActions = Blueprint('useraction', __name__, url_prefix='/api/v1/handle')


@userActions.route('/likes/<int:postId>', methods=['POST'])
def handleLikes(postId):
    """Add or remove a like from a post.
    
    Parameters:
        postId (int): The ID of the post to be liked or disliked.
    
    Returns:
        JSON object with message indicating success or error.
    """
    try:
        # Get the JSON data from the request
        user_input = request.get_json()

        # Check if the request has valid JSON data
        if user_input is None:
            return jsonify({"error": "Not valid JSON"}), 400

        # Check if the request has empty data
        if len(user_input) == 0:
            return jsonify({"error": "No Data sent"}), 400

        # Check if the request has the required 'data' key
        if "data" not in user_input:
            return jsonify({"error": "data key not found"}), 400

        # Check if the value of the 'data' key is valid
        if user_input["data"] not in ["like", "dislike"]:
            return jsonify({"error": "Invalid data value"}), 400

        # Get the post with the specified post_id
        post = Posts.query.filter_by(postId=postId).first()
        # Return a 404 error if the post is not found
        if post is None:
            return jsonify({"error": "Post not found"}), 404

        # Increment or decrement the number of likes based on the value of 'data'
        if user_input["data"] == 'like':
            post.likes += 1
        elif user_input["data"] == 'dislike':
            post.likes -= 1
        else:
            return jsonify({"error": "unknown data"}), 400

        # Commit the changes to the database
        db.session.commit()

        # Return a success message with the updated number of likes
        return jsonify({"msg": f"{user_input['data']} successfully added"}), 200
    except Exception as e:
        # Rollback any changes made to the database
        db.session.rollback()
        # Return a 500 error if an exception occurs
        return jsonify({"error": str(e)}), 500


@userActions.route('/comment/<int:postId>', methods=["POST"])
def handleComment(postId: int) -> dict:
    """
    This function handles the creation of a new comment for a given post.
    
    Parameters:
        postId (int): The ID of the post to which the comment will be added.
    
    Returns:
        A dictionary containing a message indicating the result of the operation.
        If the comment was created successfully, the dictionary will contain a "msg" field with a value of "Comment created successfully".
        If an error occurred, the dictionary will contain an "error" field with a value indicating the error that occurred.
    """
    # Validate the postId parameter
    if not isinstance(postId, int):
        return {"error": "Invalid postId parameter"}, 400
    
    # Fetch the post from the database
    post = Posts.query.filter_by(postId=postId).first()
    
    # Return an error message if the post does not exist
    if post is None:
        return {"error": "Post not found"}, 404
    
    # Parse the request body as JSON
    user_input = request.get_json()
    
    # Return an error message if the request body is not a valid JSON object
    if not user_input:
        return {"error": "Invalid JSON in request body"}, 400
    
    # Check that the required fields are present in the request body
    required = ["body", "userId"]
    for r in required:
        if r not in user_input.keys():
            return {"error": "Missing {} field in request body".format(r)}, 400
    
    # Validate the userId field
    if not isinstance(user_input['userId'], int):
        return {"error": "Invalid userId in request body"}, 400
    
    # Check that the user with the given userId exists
    user = Users.query.filter_by(userId=user_input['userId']).first()
    if user is None:
        return {"error": "User with given userId does not exist"}, 400
    
    # Create a new Comment object
    comment = Comments(postId=postId, body=user_input['body'], userId=user_input['userId'])
    
    # Add the comment to the database and commit the changes
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Return an error message if the database operation fails
        return {"error": "Failed to create comment: {}".format(e)}, 500
    
    # Return a success message
    return {"msg": "Comment created successfully"}

@userActions.route('editcomment/<int:commentId>', methods=['POST'])
def editComment(commentId):
    """Edit user comment
    
    Parameters:
        commentId (int): The ID of the comment to be edited.
    
    Returns:
        JSON object with message indicating success or error.
    """
    user_info = request.get_json()

    if user_info is None or not user_info.keys():
        return jsonify({"msg":"Not a valid JSON"})

    required  = ["userId", "body"]

    for r in required:
        if r not in user_info.keys():
            return jsonify({"msg":"Missing {}".format(r)})
    
    # Validate input
    if not isinstance(commentId, int) or commentId < 0:
        return jsonify({"msg":"Comment ID must be a positive integer"})
    if not isinstance(user_info['userId'], int) or user_info['userId'] < 0:
        return jsonify({"msg":"User ID must be a positive integer"})

    author = Users.query.filter_by(userId=user_info['userId']).first() 
    if  author is None:
        return jsonify({"msg":"No user with given ID"})
    comment = Comments.query.filter_by(commentId=commentId).first()
    if comment.userId != author.userId:
        return jsonify({"msg":"You are not the author of the comment"})
    
    try:
        comment.body = user_info['body']
        db.session.commit()
        return jsonify({"msg":"Comment updated successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg":"Error updating comment"})
