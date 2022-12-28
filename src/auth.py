from flask import (
    Blueprint,
    request,
    jsonify,
    render_template,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)
from .database import Users
from .database import db
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
)
from bleach import clean

# Create a Blueprint for the auth routes
auth = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/v1/auth",
)

@auth.post("/signup")
def signup():
    """
    Handle signup requests.
    """
    # List of required keys in the request
    required = ["firstName", "lastName", "username", "email", "password"]
    signup_info = request.get_json()

    # Check if the request is a valid JSON
    if not signup_info:
        return jsonify({"msg": "Not a JSON"}), 400

    # Check if all required keys are present in the request
    # If not, return an error message with a status code of 400 (bad request)
    for key in required:
        if key not in signup_info.keys():
            return jsonify({"msg": "Missing {}".format(key)}), 400

    first_name = signup_info["firstName"]
    last_name = signup_info["lastName"]
    username = signup_info["username"]
    email = signup_info["email"]
    password = signup_info["password"]

    # Check if the password is strong enough
    if len(password) < 6:
        return jsonify({"msg": "Password must be 8 or more characters"}), 400

    # Check if the email is unique
    if Users.query.filter_by(email=email).first() is not None:
        return jsonify({"msg": "Email is already in use"}), 409

    # Check if the username is unique
    if Users.query.filter_by(username=username).first() is not None:
        return jsonify({"msg": "Username is already taken"}), 409

    # Hash the password
    pwd_hash = generate_password_hash(password)
    user = Users(
        firstName=first_name,
        lastName=last_name,
        username=username,
        email=email,
        password=pwd_hash,
    )
    db.session.add(user)
    db.session.commit()

    return jsonify(
        {
            "msg": "User created successfully",
            "user": {
                "username": username,
                "email": email,
            },
        }
    ), 201



@auth.post("/login")
def login():
    """Take care of login queries."""
    # Required fields for post request
    required = ["email", "password"]
    login_info = request.get_json()
    if not login_info:
        return jsonify({"msg": "Not a JSON!"}), 400
    for key in required:
        if key not in login_info.keys():
            return jsonify({"msg": "Missing {}".format(key)}), 400
    email = login_info["email"]
    password = login_info["password"]

    # Check the login info with database
    user = Users.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.user_id)

            return jsonify(
                {
                    "user": {
                        "access": access_token,
                        "username": user.username,
                    }
                }
            ), 200
        else:
            return jsonify({"msg": "Wrong password"}), 401
    else:
        return jsonify({"msg": "No account with given email"}), 401
