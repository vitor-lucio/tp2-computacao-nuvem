import os
from fpgrowth_py import fpgrowth
import csv
import pickle
from flask import Flask
from dotenv import load_dotenv
import requests
import io

# variaveis de ambiente usadas (pode criar um .env com essas variaveis para rodar local)
# DATASET_NAME --> valor deve ser um dataset presente na URL https://homepages.dcc.ufmg.br/~cunha/hosted/cloudcomp-2023s2-datasets/, ele e passado no deployment.yaml

app = Flask(__name__)
load_dotenv(override=True)

playlist_dataset_response = requests.get("https://homepages.dcc.ufmg.br/~cunha/hosted/cloudcomp-2023s2-datasets/{}".format(os.getenv('DATASET_NAME')), verify=False)
playlist_dataset_csv = io.StringIO(playlist_dataset_response.text)

playlists = {}
for line in csv.reader(playlist_dataset_csv):
     if line[6] != 'pid':
         if line[6] in playlists: # line[6] e a coluna pid do dataset
             playlists[line[6]].append(line[7]) # line[7] e a coluna track_name do dataset
         else:
             playlists[line[6]] = [line[7]]

# print("----------------------------------------------------- playlists ---------------------------------------------------------")
# print(playlists)

itemSetList = [] # lista de listas de track_names (nome das musicas) de cada playlist, no formato necessario para rodar o fpgrowth e retornar as regras para recomendacao.
for key in playlists:
     itemSetList.append(playlists[key])
                
# print("----------------------------------------------------- item set list -----------------------------------------------------")
# print(itemSetList)

# rodamos o algoritmo de fpgrouwth para obter um conjunto de rules
freqItemSet, rules = fpgrowth(itemSetList, minSupRatio=0.1, minConf=0.82)
print("----------------------------------------------------- rules -----------------------------------------------------------------")
print(rules)

with open('../model/model.pickle', 'wb') as f:
    pickle.dump(rules, f)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=37000,debug=True)