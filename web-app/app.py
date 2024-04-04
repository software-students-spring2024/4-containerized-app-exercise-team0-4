#import os
#from dotenv import load_dotenv
"""Module providing framework for the web app."""
from flask import Flask, render_template
#request, redirect, abort, url_for, make_response
#import pymongo

app = Flask(__name__)

# Need to setup database
'''
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
'''

@app.route('/')
def home():
    """
    Route for the home page
    """
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
