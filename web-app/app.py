# import os
# from dotenv import load_dotenv
"""Module providing framework for the web app."""
from flask import Flask, render_template, request, redirect
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from flask_pymongo import PyMongo, MongoClient

# redirect, abort, url_for, make_response
# import pymongo

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PW = os.getenv("DB_PW")

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config["MONGO_URI"] = f"mongodb+srv://{DB_USER}:{DB_PW}@sweproject2.v6vtrh6.mongodb.net/sweproject4?retryWrites=true&w=majority&appName=SWEProject2"
mongo = PyMongo(app)
CORS(app)  # Enable CORS for all routes

# DB Set up
client = MongoClient("mongodb://localhost:27017/")
db = client["audio-transcriptions"]
collection = db["transcriptions"]

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.username = username
        self.password = password

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return self.id
    
@login_manager.user_loader
def load_user(username):
    print("load user username: ", username)
    user_info = mongo.db.users.find_one({"username": username})
    if user_info is not None:
        return User(username=user_info['username'], password=user_info['password'])
    return None

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_info = mongo.db.users.find_one({"username": request.form.get('username')})
        if user_info is not None:
            user = User(username=user_info['username'], password=user_info['password'])
            if user and user.check_password(request.form.get('password')):
                login_user(user, remember=True)
                return redirect('/')
        return 'Invalid credentials'
    else:
        if current_user.is_authenticated:
            return redirect('/')
        else:
            return render_template('login.html')
        

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect('/login')
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        existing_user = mongo.db.users.find_one({"username": username})
        if existing_user is None:
            hashed_password = generate_password_hash(password)
            mongo.db.users.insert_one({"username": username, "password": hashed_password})
            login_user(User(username=username, password=password), remember=True)
            return redirect('/')
        else:
            return 'Username already exists'
    else:
        if current_user.is_authenticated:
            return redirect('/')
        else:
            return render_template('signup.html')

@app.route("/")
def home():
    """
    Route for the home page
    """
    if current_user.is_authenticated:
        return render_template("index.html")
    else:
        return redirect("/login")

@app.route("/record", methods=["POST"])
def save_recording():
    """
    Route for save_recording POST request
    """
    print("received")
    print(request.data)
    return render_template("record.html")

@app.route("/record")
def record():
    return render_template("record.html")

@app.route("/view_transcription")
def view_transcription():
    return render_template("view_transcription.html")

@app.route("/view_all")
def view_all():

    # Get all transcriptions from the database
    transcriptions = collection.find()
    # print(transcriptions)
    
    return render_template("view_all.html", transcriptions=transcriptions)


if __name__ == "__main__":
    app.run(debug=True)
