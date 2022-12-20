from flask import (
                    Blueprint,
                    request,
                    jsonify,
                    render_template
)
from werkzeug.security import (
                                generate_password_hash,
                                check_password_hash
)
from .database import Users
from .database import db
from flask_jwt_extended import (
                                create_access_token,
                                create_refresh_token,
                                jwt_required
)
from bleach import clean


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
        return jsonify({"msg":"Not a JSON"}), 400
    
    # check if all required keys are passed to request
    # if not return error message with status code of 400(bad request)
    for key in required:
        if key not in signupInfo.keys():
            return jsonify({"msg":"Missing {}".format(key)}), 400

    firstName = signupInfo['firstName']
    lastName = signupInfo['lastName']
    username = signupInfo['username']
    email = signupInfo['email']
    password = signupInfo['password']
    
    

    #check if the password is strong
    if len(password) < 6:
        return jsonify({"msg":"Password must be 8 or more character"}), 400
    
    # check if the email is unique
    if Users.query.filter_by(email=email).first() is not None:
        return jsonify({"msg":"Email is already in use"}), 409
        
    # check if the username is unique
    username = signupInfo['username']
    if Users.query.filter_by(username=username).first() is not None:
        return jsonify({"msg":"Username is already taken"}), 409


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
@auth.post("/login")
def login():
    """
        take care of login queries 
    """
    # required feild for post request
    required = ["email", "password"]
    loginInfo = request.get_json()
    if not loginInfo:
        return jsonify({"msg":"Not a JSON!"}), 400 
    for key in required:
        if key not in loginInfo.keys():
            return jsonify({"msg": "Missing {}".format(key)}), 400
    email = loginInfo['email']
    password = loginInfo['password']

    # check the login info with database
    user = Users.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            accessToken = create_access_token(identity=user.userId)

            return jsonify({
                            "user": {
                                "access":accessToken,
                                "username":user.username
                            }
            }), 200
        else:
            return jsonify({"msg": "Wrong password"}), 401
    else:
        return jsonify({"msg": "No account with given email"}), 401

@auth.post("/test")
def test():
    data = request.get_json()
    print(data)