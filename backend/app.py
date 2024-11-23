#!flask/bin/python
import flask
from flask import jsonify
from flask_cors import CORS, cross_origin

app = flask.Flask(__name__);
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

@app.route("/")
@cross_origin()
def index():
    print(jsonify({"data": "Hello vova"}))
    response = jsonify({"data": "Hello vova"})
    return response

@app.route('/api/login', methods=["GET"])
@cross_origin()
def auth():
    response = jsonify({"data" :  "auth result"})
    return response

@app.route('/api/marks', methods=["GET"])
@cross_origin()
def getMarksList():
    response = jsonify({"data" :  "get marks list result"})
    return response

@app.route('/api/marks/<int:mark_id>', methods=["GET", "POST", "PUT", "DELETE"])
@cross_origin()
def processMark(mark_id):
    response = jsonify({"data" : f"get data of mark with id: {mark_id}"})
    return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
