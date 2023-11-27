from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from fpgrowth_py import fpgrowth
import csv
import pickle
from datetime import datetime
import time

time.sleep(20)

app = Flask(__name__)
load_dotenv(override=True)

playlists = {}

with open('2023_spotify_ds1.csv','r', encoding="utf8") as data:
   for line in csv.reader(data):
        if line[6] != 'pid':
            if line[6] in playlists: # line[6] e a coluna pid do dataset
                playlists[line[6]].append(line[7]) # line[7] e a coluna track_name do dataset
            else:
                playlists[line[6]] = [line[7]]

with open('2023_spotify_ds2.csv','r', encoding="utf8") as data:
   for line in csv.reader(data):
        if line[6] != 'pid':
            if line[6] in playlists: # line[6] e a coluna pid do dataset
                playlists[line[6]].append(line[7]) # line[7] e a coluna track_name do dataset
            else:
                playlists[line[6]] = [line[7]]

# print("----------------------------------------------------- playlists ---------------------------------------------------------")
# print(playlists)

model_file_path = '../model/model.pickle'

with open(model_file_path, 'rb') as f:
    rules_model = pickle.load(f)

print("----------------------------------------------------- rules model ---------------------------------------------------------")
print(rules_model)

model_update_date_as_string = datetime.today().strftime('%Y-%m-%d %H:%M:%S')


@app.route("/api/recommender", methods=['POST'])
def recommend():
    global rules_model
    global model_update_date_as_string
    global model_file_change_time

    with open(model_file_path, 'rb') as f:
        new_rules_model = pickle.load(f)

    # See if new_rules_model is different than rules_model, to check if we need to update the rules_model
    pairs = zip(rules_model, new_rules_model)
    if any(x != y for x, y in pairs):
        print("Updating model")
        model_update_date_as_string = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        rules_model = new_rules_model


    request_json_body = request.get_json(force=True)

    request_songs_set = set(request_json_body["songs"])

    # find rules that are matched by the request's songs. These will be the rules to be used in determining what playlists will be recommended.
    matched_rules = []
    for rule in rules_model:
        if rule[0].issubset(request_songs_set):
            matched_rules.append(rule)
    print("-------------------------------------------------- matched rules -----------------------------------------------------------------")
    print(matched_rules)

    # if even one song from the second item of a matched rule is a subset of the playlist songs, this playlist will be recommended.
    playlist_pids_to_recommend = []
    for key in playlists:
        for matched_rule in matched_rules:
            if matched_rule[1].issubset(set(playlists[key])):
               playlist_pids_to_recommend.append(key)
               break
    print("-------------------------------------------------- playlist pids to recommend ----------------------------------------------------")
    print(playlist_pids_to_recommend)

    return jsonify({"playlist_ids": playlist_pids_to_recommend, "model_date": model_update_date_as_string, "version": os.getenv('VERSION')})


@app.route("/api/ping", methods=['GET'])
def ping():
    return 'Pong!'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=32216,debug=True)