from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)
load_dotenv(override=True)

@app.route("/callserver", methods=['POST'])
def hello_world():
    request_json_body = request.get_json(force=True)
    print("-------------------------------------- request json body --------------------------------------")
    print(request_json_body)
    response = requests.post("http://{}:{}/api/recommender".format(os.getenv('SERVER_NAME'), os.getenv('SERVER_PORT')), json=request_json_body)
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)