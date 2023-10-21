from flask import Flask, jsonify
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)
load_dotenv(override=True)

@app.route("/")
def hello_world():
    response = requests.post("http://{}:{}/api/recommend".format(os.getenv('SERVER_NAME'), os.getenv('SERVER_PORT')), json={'corpo': 'corpo da requisicao'})
    return "mensagem do cliente, com uma variavel de teste <{}> e a resposta do servidor  <{}>".format(os.getenv('TESTE'), response.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=30501,debug=True)