# importing packages
import random
import time
import pytube
import os
import vlc
import json


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
    if playlist == "all":
        playlists = os.listdir("playlists")
        song_list = list()
        for directory in playlists:
            if not directory == ".gitignore":
                entries = os.listdir("playlists/" + directory)
                for i in range(len(entries)):
                    entries[i] = os.path.join(directory, entries[i])
                print(entries)
                song_list = song_list + entries
    else:
        song_list = os.listdir("playlists/" + playlist)
    queue = create_list(song_list, playlist)
    play_song(playlist, queue, 0)


def create_list(songs, playlist):
    music_list = random.sample(songs, len(songs))
    song_length = {}
    for song in music_list:
        # song_length[song] = music_length(song, playlist)
        song_length[song] = get_length(song, playlist)
    longest = song_length[max(song_length, key=song_length.get)]
    for song in music_list:
        element_time = music_list.count(song) * song_length[song]
        print(song, element_time)
        error = longest - element_time
        print(error)
        if error >= 60000:
            print(song, "is to short")
            music_list.insert(random.randrange(len(music_list)+1), song)
    printable = list()
    for song in music_list:
        printable.append(song.split('\\')[1][0:len(song.split('\\'))-6])
    print(printable)
    return music_list
    

"""
ex: 3 songs: A: 1:30, B: 4:00, C: 1:00
sample random (A, C, B)
find longest element (B)

for each element in sample:         (A)     (B)     (C)
    sum total element time          (1:30)  (4:00)  (1:00)
    error = longest - el_time       (2:30)  (0)     (3:00)
    if error < 60000:               (no)    (yes)   (no)
        nothing
    else:
        randomly insert duplicate of element    (A, A, C, C, A, B, C, C)
repeat for loop
"""


def music_length_vlc(song, playlist):
    p = vlc.MediaPlayer("playlists/" + playlist + "/" + song + ".mp3")
    p.play()
    time.sleep(1.5)
    length = p.get_length()
    p.stop()
    return length

def get_length(song, playlist):
    if playlist == "all":
            with open(os.path.join("song_lengths", song.split('\\')[0] + ".json"), 'r+') as f:
                data = json.load(f)
                name_with_mp3 = song.split('\\')[1]
                return data[name_with_mp3[0:len(name_with_mp3)-4]]
    else:
        with open(os.path.join("song_lengths", playlist + ".json"), 'r+') as f:
            data = json.load(f)
            return data[song[0:len(song)-4]]


def play_song(playlist, songs, index):
    if index == len(songs):
        return
    if playlist == "all":
        p = vlc.MediaPlayer("playlists/" + songs[index])
    else:
        p = vlc.MediaPlayer("playlists/" + playlist + "/" + songs[index])
    p.audio_set_volume(50)
    p.play()
    print("playing: " + songs[index])
    time.sleep(get_length(songs[index], playlist)/1000)
    p.stop()
    index += 1
    play_song(playlist, songs, index)


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
    elif command == "stop":
        return
    elif command == "quit":
        return

run()
