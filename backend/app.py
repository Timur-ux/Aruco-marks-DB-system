#!flask/bin/python
from flask import Flask

app = Flask(__name__);

@app.route("/")
def index():
    return "Hello vova"
@app.route('/api/login', methods=["GET"])
def auth():
    return "auth result"

@app.route('/api/marks', methods=["GET"])
def getMarksList():
    return "get marks list result"

@app.route('/api/marks/<int:mark_id>', methods=["GET", "POST", "PUT", "DELETE"])
def processMark(mark_id):
    return f"get data of mark with id: {mark_id}"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
