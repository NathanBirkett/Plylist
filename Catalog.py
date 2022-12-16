from Song import Song
import os
import json

def get_length(song, directory):
    with open(os.path.join("song_lengths", directory + ".json"), 'r+') as f:
        data = json.load(f)
        return data[song[0:len(song)-4]]

songs = []
playlists = list()
playlists = os.listdir("playlists")
playlists.remove(".gitignore")
for directory in playlists:
    entries = os.listdir("playlists/" + directory)
    for i in range(len(entries)):
        entries[i] = Song(entries[i][0:len(entries[i])-4], directory + "/" + entries[i], get_length(entries[i], directory))
    songs.extend(entries)