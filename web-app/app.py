# import os
# from dotenv import load_dotenv
"""Module providing framework for the web app."""
from flask import Flask, render_template, request
from flask_cors import CORS
import os
from pymongo import MongoClient


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# DB Set up
client = MongoClient("mongodb://localhost:27017/")
# check if client is connected to the server
print("client: ", client)
db = client["audio-transcriptions"]
print("db: ", db)
collection = db["transcriptions"]
print("collection: ", collection)

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
    print("collection: ", collection)
    transcriptions = collection.find()
    print("transcriptions: ", transcriptions)
    return render_template("view_all.html", transcriptions=transcriptions)

if __name__ == "__main__":
    app.run(debug=True)
