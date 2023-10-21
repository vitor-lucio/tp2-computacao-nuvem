from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv(override=True)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>" + str(os.getenv('TESTE'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=30501,debug=True)