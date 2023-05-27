#hello_world.py
from flask import Flask
from application import app

if __name__ == '__main__':
    app.run(debug=False)

#app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"