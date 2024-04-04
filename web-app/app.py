from flask import Flask, render_template, request, redirect, abort, url_for, make_response

app = Flask(__name__)

@app.route('/')
def home():
    """
    Route for the home page
    """
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)