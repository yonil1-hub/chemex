from flask import (
                    Blueprint,
                    request,
                    jsonify
)
from werkzeug.security import (
                                generate_password_hash,
                                check_password_hash
)
from .database import Users
from .database import db


auth = Blueprint("auth",
                 __name__,
                 url_prefix="/api/v1/auth"
                 )

@auth.post('/signup')
def signup():
    required = ["firstName", "lastName", "username",
                "email", "password"
               ]
    signupInfo = request.get_json()

    #check if the form is valid JSON
    if not signupInfo:
        return jsonify({"error":"Not a JSON"}), 400
    
    # check if all required keys are passed to request
    # if not return error message with status code of 400(bad request)
    for key in required:
        if key not in signupInfo.keys():
            return jsonify({"error":"Missing {}".format(key)}), 400

    firstName = signupInfo['firstName']
    lastName = signupInfo['lastName']
    username = signupInfo['username']
    email = signupInfo['email']
    password = signupInfo['password']
    
    

    #check if the password is strong
    if len(password) < 8:
        return jsonify({"error":"Password must be 8 or more character"}), 400

    # email_validator here


    # check if the username is unique
    username = signupInfo['username']
    if Users.query.filter_by(username=username).first() is not None:
        return jsonify({"error":"Username is already taken"}), 409

    # check if the email is unique
    if Users.query.filter_by(email=email).first() is not None:
        return jsonify({"error":"Email is already in use"}), 409
    
    pwd_hash = generate_password_hash(password)
    user = Users(
                 firstName=firstName,
                 lastName=lastName,
                 username=username,
                 email=email,
                 password=pwd_hash
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg":"User created successfully",
                    "user":{
                        "username":username,
                        "email":email
                    }
    }), 201
@auth.get("/login")
def login():
    """"""
    return {"user":"me"}