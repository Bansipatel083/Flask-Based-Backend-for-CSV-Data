from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

def create_user(data):
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return {"msg": "Missing required fields", "status": 400}

    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return {"msg": "User already exists", "status": 400}

    hashed_password = generate_password_hash(password, method='scrypt')
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity={'username': username, 'email': email})
    return {"msg": "User created successfully", "access_token": access_token, "status": 201}

def authenticate_user(data):
    username_or_email = data.get('username_or_email')
    password = data.get('password')

    if not username_or_email or not password:
        return {"msg": "Missing username/email or password", "status": 400}

    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity={'username': user.username, 'email': user.email})
        return {"msg": "Login successful", "access_token": access_token, "status": 200}

    return {"msg": "Invalid username/email or password", "status": 401}

