# from flask
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin

# third party packages
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

# native packages
from datetime import timedelta, datetime, timezone

from functools import wraps
import dotenv



# create the app
app = Flask(__name__)

# configure CORS
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
# create the extension
# configure the SQLite database, relative to the app instance folder

# for sqlite database
if dotenv.get_key('.env', 'FLASK_DEBUG') == 'True':
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
else: 
    # for mysql database
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{dotenv.get_key('.env', 'MYSQL_USERNAME')}:{dotenv.get_key('.env', 'MYSQL_PASSWORD')}@{dotenv.get_key('.env', 'MYSQL_HOST')}/{dotenv.get_key('.env', 'MYSQL_DATABASE')}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = dotenv.get_key('.env', 'SECRET_KEY')

# initialize the app with the extension
db = SQLAlchemy(app)
migrate = Migrate(app, db)


## models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128),  nullable=False)
    is_student = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f'<User {self.username}>'





## decorators
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except Exception as e:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(*args, **kwargs)
    return decorated



## utilities
def validate_password(password):
    if len(password) < 8:
        return False
    else:
        return True


## routes
@app.route('/')
def index():
    return '500 Internal Server Error'


## user routes
@app.route('/api/create-user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        data = request.get_json()
        # get username and password from the request
        username = data.get('username')
        email = data.get('email')
        is_student = data.get('is_student')

        # check if email is valid
        if not email or '@' not in email:
            return jsonify({'message': 'Email is invalid'})
        
        # check if email already exists
        password = data.get('password')

        # check if username and password are not empty
        if username and password and email:
            # check if username already exists
            user = User.query.filter_by(email=email).first()
            if user:
                return jsonify({'message': 'Email already exists'})
            
            # check if password is valid
            if validate_password(password):
                hashed_password = generate_password_hash(password)
                new_user = User(username=username, email=email, is_student=is_student, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                return jsonify({'message': 'User created'})
            else:
                return jsonify({'message': 'Password is too short'})
        else:
            return jsonify({'message': 'Username, email or password is missing'})
    

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    # get username and password from the request
    email = data.get('email')
    password = data.get('password')

    # check if username and password are not empty
    if not email or not password:
        return jsonify({'message': 'Username or password is missing'})
    
    # check if username and password are correct
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            token = jwt.encode({'email': email, 'exp': datetime.now(timezone.utc) + timedelta(hours=7)}, app.config['SECRET_KEY'])
            return jsonify({'message': 'Logged in', 'token': token})
        else:
            return jsonify({'message': 'Wrong password'})
    else:
        return jsonify({'message': 'Wrong email or password'})
    

@app.route('/api/change-password', methods=['POST'])
@token_required
def change_password():
    data = request.get_json()
    # get username and password from the request
    email = data.get('email')
    password = data.get('password')
    new_password = data.get('new_password')

    # check if username and password are not empty
    if not email or not password or not new_password:
        return jsonify({'message': 'email, password or new_password is missing'})
    
    # check if username and password are correct
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            if not validate_password(new_password):
                return jsonify({'message': 'Password is too short'})
            hashed_password = generate_password_hash(new_password)
            user.password = hashed_password
            user.updated_at = datetime.now(datetime.timezone.utc)
            db.session.commit()
            return jsonify({'message': 'Password changed'})
        else:
            return jsonify({'message': 'Wrong usernamer or password'})
    else:
        return jsonify({'message': 'Wrong username or password'})
    


if __name__ == '__main__':
    if dotenv.get_key('.env', 'FLASK_DEBUG') == 'True':
        app.run(debug=True)
    else:
        app.run()