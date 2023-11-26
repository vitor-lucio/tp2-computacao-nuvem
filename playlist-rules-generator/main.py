import os
from fpgrowth_py import fpgrowth
import csv
import pickle
from flask import Flask
from dotenv import load_dotenv
import requests

app = Flask(__name__)
load_dotenv(override=True)

itemSetList = [] # lista de listas de track_names (nome das musicas) de cada playlist, no formato necessario para rodar o fpgrowth e retornar as regras para recomendacao.
playlists = [] # lista de objetos representando as playlists, contendo playlist id (pid) e musicas (songs). Necessario para identificar e analisar cada playlist de acordo com as regras geradas para recomendacao

# atraves de arquivos csv, como os samples de playlist, vai ser criado a lista para geracao das regras de recomendacao e a lista com objetos identificando as playlists e suas musicas
# previous_pid = 0
# playlist_songs = []
with open('2023_spotify_ds1.csv','r', encoding="utf8") as data: # mudar arquivo csv para '2023_spotify_ds2.csv' quando for testar a atualizacao do model
   for line in csv.reader(data):
        if line[6] != 'pid':
            new_playlist = True
            for playlist in playlists:
                if playlist['pid'] == line[6]: # line[6] e a coluna pid do dataset
                    playlist['songs'].append(line[7]) # line[7] e a coluna track_name do dataset
                    new_playlist = False
           
            if new_playlist: # Se a playlist da linha do dataset não estiver na lista de playlists, criar novo dicionario para esta playlist.
                playlists.append({'pid': line[6], 'songs': [line[7]]})
            new_playlist = True
           

# print("----------------------------------------------------- playlists ---------------------------------------------------------")
# print(playlists)

for playlist in playlists:
     itemSetList.append(playlist['songs'])
                
# print("----------------------------------------------------- item set list -----------------------------------------------------")
# print(itemSetList)

# rodamos o algoritmo de fpgrouwth para obter um conjunto de rules
freqItemSet, rules = fpgrowth(itemSetList, minSupRatio=0.1, minConf=0.82)
print("----------------------------------------------------- rules -----------------------------------------------------------------")
print(rules)

with open('model.pickle', 'wb') as f:
    pickle.dump(rules, f)

# req = requests.post("http://{}:{}/api/model".format(os.getenv('SERVER_NAME'), os.getenv('SERVER_PORT')), files={'file': open('model.pickle', 'rb')})

# print(req.content)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=37000,debug=True)