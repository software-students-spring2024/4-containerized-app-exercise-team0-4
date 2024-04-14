# import os
# from dotenv import load_dotenv
"""Module providing framework for the web app."""
from flask import Flask, render_template, request, redirect
from flask_cors import CORS
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

# Need to setup database
"""
# Connect to the MongoDB server using environment variables 
load_dotenv()
connection = pymongo.MongoClient(os.getenv('MONGO_URI'))
db = connection[os.getenv('MONGO_DBNAME')]
try:
    # verify the connection works by pinging the database
    connection.admin.command("ping")  
    print(" *", "Connected to MongoDB!")  
except Exception as e:
    # the ping command failed, so the connection is not available.
    print(" * MongoDB connection error:", e)
"""

@app.route("/")
def home():
    """
    Route for the home page
    """
    return render_template("index.html")

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

@app.route("/view_all")
def view_all():

    # Get all transcriptions from the database
    transcriptions = collection.find()
    
    return render_template("view_all.html", transcriptions=transcriptions)


if __name__ == "__main__":
    app.run(debug=True)
