import pickle
from Song import Song
from Playlist import Playlist
import os
import json

def get_length(song, directory):
    with open(os.path.join("song_lengths", directory + ".json"), 'r+') as f:
        data = json.load(f)
        return data[song[0:len(song)-4]]

def create_playlist(name, songs):
    global playlists_map
    global playlists
    playlists.append(Playlist(name, [song_map[song] for song in songs]))
    playlists_map = dict(zip([playlist.name for playlist in playlists], playlists))

song_map = []
playlists_map = []
def save():
    with open("userdata/catalog.pickle", "wb") as outfile:
        pickle.dump([songs, playlists], outfile)
        
def restore():
    global songs
    global playlists
    global playlists_map
    global song_map
    try:
        with open("userdata/catalog.pickle", "rb") as infile:
            data = pickle.load(infile)
            songs = data[0]
            playlists = data[1]
    except:
        songs = []
        playlists = []
        playlists.append(Playlist("all", songs))
    song_map = dict(zip([song.name for song in songs], songs))
    playlists_map = dict(zip([playlist.name for playlist in playlists], playlists))