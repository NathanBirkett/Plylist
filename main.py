# importing packages
import random
import time
import pytube
import os
import sys
import vlc
import json
import threading

def new_playlist(name):
    os.mkdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "playlists", name))
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "song_lengths", name + ".json")
    with open(path, 'w') as f:
        f.write("{\n\n}")
        f.close()
        print("file has been created")


def install_file(url, name, playlist):
    if os.path.exists(name + ".mp3"):
        os.remove(name + ".mp3")
    try:
        yt = pytube.YouTube(url)
    except:
        print("connection error")
    video = yt.streams.filter(only_audio=True).first()
    destination = os.path.join("playlists", playlist)
    out_file = video.download(output_path=destination, filename=name)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    print(yt.title + " has been successfully downloaded.")
    with open(os.path.join("song_lengths", playlist + ".json"), 'r+') as f:
        data = json.load(f)
        data[name] = music_length_vlc(name, playlist)
        f.seek(0)
        json.dump(data, f, indent = 4)


def play(playlist):
    playlists = list()
    song_list = list()
    if playlist == "all":
        playlists = os.listdir("playlists")
        playlists.remove(".gitignore")
    else:
        playlists = playlist.split(', ')
    for directory in playlists:
        entries = os.listdir("playlists/" + directory)
        for i in range(len(entries)):
            entries[i] = os.path.join(directory, entries[i])
        song_list = song_list + entries
    queue = create_list(song_list, playlist)
    p = vlc.MediaPlayer("playlists/" + queue[0])
    p.audio_set_volume(50)
    print("starting t2")
    t2 = threading.Thread(target=control, args=(p,))
    t2.start()
    play_song(p, playlist, queue, 0)


def create_list(songs, playlist):
    music_list = random.sample(songs, len(songs))
    song_length = {}
    for song in music_list:
        song_length[song] = get_length(song, playlist)
    longest = song_length[max(song_length, key=song_length.get)]
    for song in music_list:
        element_time = music_list.count(song) * song_length[song]
        error = longest - element_time
        if error >= 60000:
            music_list.insert(random.randrange(len(music_list)+1), song)
    printable = list()
    for song in music_list:
        printable.append(song.split('\\')[1][0:len(song.split('\\')[1])-4])
    print(printable)
    print(len(printable))
    return music_list


def music_length_vlc(song, playlist):
    p = vlc.MediaPlayer("playlists/" + playlist + "/" + song + ".mp3")
    p.play()
    time.sleep(1.5)
    length = p.get_length()
    p.stop()
    return length

def get_length(song, playlist):
    with open(os.path.join("song_lengths", song.split('\\')[0] + ".json"), 'r+') as f:
        data = json.load(f)
        return data[song.split('\\')[1][0:len(song.split('\\')[1])-4]]


def play_song(p, playlist, songs, index):
    if index == len(songs):
        return
    p.set_media(vlc.Media("playlists/" + songs[index]))
    p.play()
    print("playing: " + songs[index] + ", next: " + songs[index+1])
    timer = time.time() + get_length(songs[index], playlist)/1000
    while True:
        if time.time() >= timer and p.is_playing():
            break
    print("playing next song")
    p.stop()
    index += 1
    print(index)
    play_song(p, playlist, songs, index)
    
def rename(playlist, song, name):
    os.rename("playlists/"+playlist+"/"+song+".mp3", "playlists/"+playlist+"/"+name+".mp3")
    with open("song_lengths/"+playlist+".json", 'r+') as f:
        data = json.load(f)
        for pair in data.items():
            pair[name] = pair.pop(song)
            
def delete(playlist, song):
    with open("song_lengths/"+playlist+".json", 'r+') as f:
        data = json.load(f)
        for pair in data.items():
            pair.pop(song)
        print(data)
    os.remove("playlists/"+playlist+"/"+song+".mp3")
    
def control(p):
    while True:
        command = input("command: ")
        if command == "stop":
            p.stop()
            run()
            sys.exit("stopping thread")
            break
        elif command in ["pause", "resume"]:
            print("pausing")
            p.pause()
        continue

def run():
    command = input("command: ")
    if command == "add playlist":
        new_playlist(input("name: "))
        run()
    elif command == "add song":
        install_file(input("url: "), input("name: "), input("playlist: "))
        run()
    elif command == "play":
        play(input("playlist: "))
    elif command == "quit":
        os._exit(0)
    elif command == "rename":
        rename(input("playlist: "), input("song: "), input("name: "))
        run()
    elif command == "delete":
        delete(input("playlist: "), input("song: "))
    else:
        print("invalid command")
        run()
if __name__ == "__main__":
    run()