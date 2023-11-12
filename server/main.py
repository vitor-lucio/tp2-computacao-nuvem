from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from fpgrowth_py import fpgrowth
import csv
import pickle
from datetime import datetime

app = Flask(__name__)
load_dotenv(override=True)

playlists = [] # lista de playlists que serao consideradas para a recomendacao

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
                playlists.append({'pid': line[0], 'songs': [line[5]]})

                playlist_songs = [line[5]]
                previous_pid = current_pid

# atraves de arquivos csv, como os samples de playlist, vai ser criado a lista para geracao das regras de recomendacao e a lista com objetos identificando as playlists e suas musicas
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
                playlists.append({'pid': line[0], 'songs': [line[5]]})

                playlist_songs = [line[5]]
                previous_pid = current_pid

model_file_path = 'model.pickle'

with open(model_file_path, 'rb') as f:
    rules_model = pickle.load(f)

model_update_date_as_string = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

@app.route("/api/model", methods=['POST'])
def model_update():
    model = request.files['file']

    model.save(model_file_path)

    return {"message": "file sent sucessfully"}


@app.route("/api/recommend", methods=['POST'])
def recommend():
    global rules_model
    global model_update_date_as_string
    global model_file_change_time

    with open(model_file_path, 'rb') as f:
        new_rules_model = pickle.load(f)

    pairs = zip(rules_model, new_rules_model)
    if any(x != y for x, y in pairs):
        print("Updating model")
        model_update_date_as_string = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        rules_model = new_rules_model


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