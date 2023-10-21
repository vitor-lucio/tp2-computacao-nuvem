from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv(override=True)

@app.route("/api/recommend", methods=['POST'])
def hello_world():
    request_json_body = request.get_json(force=True)
    return "<p>Hello, World!</p> {} {}".format(os.getenv('TESTE'), request_json_body)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=30502,debug=True)