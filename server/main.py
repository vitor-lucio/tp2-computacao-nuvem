from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from fpgrowth_py import fpgrowth
import csv
import pickle
from datetime import datetime

app = Flask(__name__)
load_dotenv(override=True)

itemSetList = [] # lista de listas de track_names (nome das musicas) de cada playlist, no formato necessario para rodar o fpgrowth e retornar as regras para recomendacao.
playlists = [] # lista de objetos representando as playlists, contendo playlist id (pid) e musicas (songs). Necessario para identificar e analisar cada playlist de acordo com as regras geradas para recomendacao

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

# previous_pid = 0
# playlist_songs = []
# with open('playlist-sample-ds2.csv','r', encoding="utf8") as data:
#    for line in csv.reader(data):
#         if line[0] != 'pid':
#             current_pid = line[0]
#             if current_pid == previous_pid:
#                 playlists[-1]['songs'].append(line[5])

#                 playlist_songs.append(line[5])
#             else:
#                 if len(playlist_songs) != 0:
#                     itemSetList.append(playlist_songs)
                
#                 playlists.append({'pid': line[0], 'songs': [line[5]]})

#                 playlist_songs = [line[5]]
#                 previous_pid = current_pid

                
# print("----------------------------------------------------- item set list -----------------------------------------------------")
# print(itemSetList)
# print("----------------------------------------------------- playlists ---------------------------------------------------------")
# print(playlists)

# rodamos o algoritmo de fpgrouwth para obter um conjunto de rules
# itemSetList = [['eggs', 'bacon', 'soup'],
#             ['eggs', 'bacon', 'apple'],
#             ['soup', 'bacon', 'banana']]

freqItemSet, rules = fpgrowth(itemSetList, minSupRatio=0.015, minConf=0.6)
# print("----------------------------------------------------- frequent item set -----------------------------------------------------")
# print(freqItemSet)
# print("----------------------------------------------------- rules -----------------------------------------------------------------")
# print(rules)

#pickle_test = [[{'Someone'}, {'something'}, 0.63], [{'Let it'}, {'Roses'}, 0.87]]
with open('model.pickle', 'wb') as f:
    pickle.dump(rules, f)

model_update_date_as_string = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

with open('model.pickle', 'rb') as f:
    rules_model = pickle.load(f)
# print(rules_model)

@app.route("/api/recommend", methods=['POST'])
def recommend():
    request_json_body = request.get_json(force=True)

    # request_songs_set = set(["Have Yourself A Merry Little Christmas", "Sleigh Ride"])
    request_songs_set = set(request_json_body["songs"])

    # find rules that are matched by the request's songs. These will be the rules to be used in determining what playlists will be recommended.
    matched_rules = []
    for rule in rules_model:
        if rule[0].issubset(request_songs_set):
            matched_rules.append(rule)
    #print("-------------------------------------------------- matched rules -----------------------------------------------------------------")
    #print(matched_rules)

    # if even one song from the second item of a matched rule is a subset of the playlist songs, this playlist will be recommended.
    playlist_pids_to_recommend = []
    for playlist in playlists:
        for matched_rule in matched_rules:
             if matched_rule[1].issubset(set(playlist['songs'])):
                playlist_pids_to_recommend.append(playlist['pid'])
                break
    #print("-------------------------------------------------- playlist pids to recommend ----------------------------------------------------")
    #print(playlist_pids_to_recommend)

    return jsonify({"playlist_ids": playlist_pids_to_recommend, "model_date": model_update_date_as_string})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=32216,debug=True)