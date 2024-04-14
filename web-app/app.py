"""Module providing framework for the web app."""
from flask import Flask, render_template
from flask_cors import CORS
from pymongo import MongoClient

# DB Set up
client = MongoClient("mongodb://localhost:27017/")
db = client["audio-transcriptions"]
collection = db["transcriptions"]


def create_app(test_config=None):
    """
    Create and configure the Flask application.

    Args:
        test_config (dict, optional): Configuration dictionary for testing purposes. Defaults to None.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)
    CORS(app) # Enable CORS for all routes
    if test_config is not None:
        app.config.update(test_config)

    @app.route("/")
    def home():
        """
        Route for the home page.
        """
        return render_template("index.html")

    @app.route("/record")
    def record():
        """
        Route for the record page.
        """
        return render_template("record.html")

@app.route("/view_all")
def view_all():
    # Get all transcriptions from the database
    print("collection: ", collection)
    transcriptions = collection.find()
    print("transcriptions: ", transcriptions)
    return render_template("view_all.html", transcriptions=transcriptions)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)