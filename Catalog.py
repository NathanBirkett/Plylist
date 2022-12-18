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
    playlists.sort(key=lambda x: x.name)
    playlists_map = dict(zip([playlist.name for playlist in playlists], playlists))

song_map = {}
playlists_map = {}
songs = []
playlists = []
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
    songs.sort(key=lambda x: x.name)
    playlists.sort(key=lambda x: x.name)
    song_map = dict(zip([song.name for song in songs], songs))
    playlists_map = dict(zip([playlist.name for playlist in playlists], playlists))
    
def add_song(name, path, length, url):
    global song_map
    global playlists_map
    playlists.remove(next((x for x in playlists if x.name == "all"), None))
    songs.append(Song(name, path, length, url))
    songs.sort(key=lambda x: x.name)
    playlists.append(Playlist("all", songs))
    playlists.sort(key=lambda x: x.name)
    song_map = dict(zip([song.name for song in songs], songs))
    playlists_map = dict(zip([playlist.name for playlist in playlists], playlists))
    
    