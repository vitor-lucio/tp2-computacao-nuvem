from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from fpgrowth_py import fpgrowth
import csv

app = Flask(__name__)
load_dotenv(override=True)

itemSetList = [] #lista de listas de track_names (nome das musicas) de cada playlist, no formato necessario para rodar o fpgrowth e retornar as regras para recomendacao.
playlists = [] #lista de objetos representando as playlists, contendo playlist id (pid) e musicas (songs). Necessario para identificar e analisar cada playlist de acordo com as regras geradas para recomendacao

# atraves de arquivos csv, como os samples de playlist, vai ser criado a lista para geracao das regras de recomendacao e a lista com objetos identificando as playlists e suas musicas
previous_pid = 0
playlist_songs = []
with open('playlist-sample-ds1.csv','r', encoding="utf8") as data:
   for line in csv.reader(data):
        if line[0] != 'pid':
            current_pid = line[0]
            if current_pid == previous_pid:
                playlists[-1]['songs'].append(line[5])

                playlist_songs.append(line[5])
            else:
                if len(playlist_songs) != 0:
                    itemSetList.append(playlist_songs)
                
                playlists.append({'pid': line[0], 'songs': [line[5]]})

                playlist_songs = [line[5]]
                previous_pid = current_pid

previous_pid = 0
playlist_songs = []
with open('playlist-sample-ds2.csv','r', encoding="utf8") as data:
   for line in csv.reader(data):
        if line[0] != 'pid':
            current_pid = line[0]
            if current_pid == previous_pid:
                playlists[-1]['songs'].append(line[5])

                playlist_songs.append(line[5])
            else:
                if len(playlist_songs) != 0:
                    itemSetList.append(playlist_songs)
                
                playlists.append({'pid': line[0], 'songs': [line[5]]})

                playlist_songs = [line[5]]
                previous_pid = current_pid

                
# print("----------------------------------------------------- item set list -----------------------------------------------------")
# print(itemSetList)
# print("----------------------------------------------------- playlists ---------------------------------------------------------")
# print(playlists)

# rodamos o algoritmo de fpgrouwth e conseguimos um conjunto de regras
# itemSetList = [['eggs', 'bacon', 'soup'],
#             ['eggs', 'bacon', 'apple'],
#             ['soup', 'bacon', 'banana']]

freqItemSet, rules = fpgrowth(itemSetList, minSupRatio=0.015, minConf=0.6)
print("----------------------------------------------------- frequent item set -----------------------------------------------------")
print(freqItemSet)
print("----------------------------------------------------- rules -----------------------------------------------------------------")
print(rules)


@app.route("/api/recommend", methods=['POST'])
def hello_world():
    request_json_body = request.get_json(force=True)
    return "<p>Hello, World!</p> {} {}".format(os.getenv('TESTE'), request_json_body)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=30502,debug=True)