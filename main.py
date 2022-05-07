# importing packages
import random
import time
from pytube import YouTube
import os
import vlc


def new_playlist(name):
    os.mkdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "playlists", name))


def install_file(url, name, playlist):
    if os.path.exists(name + ".mp3"):
        os.remove(name + ".mp3")
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    destination = os.path.join("playlists", playlist)
    out_file = video.download(output_path=destination, filename=name)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    print(yt.title + " has been successfully downloaded.")


def play(playlist):
    song_list = os.listdir("playlists/" + playlist)
    songs = random.sample(song_list, len(song_list))
    create_list(songs, playlist)
    print(songs)
    play_song(playlist, songs, 0)
    play(playlist)


def create_list(songs, playlist):
    music_list = random.sample(songs, len(songs))
    for song in music_list:
        print(music_length(song, playlist))

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


def music_length(song, playlist):
    p = vlc.MediaPlayer("playlists/" + playlist + "/" + song)
    p.play()
    time.sleep(1.5)
    length = p.get_length()
    p.stop()
    return length


def play_song(playlist, songs, index):
    if index == len(songs):
        return
    p = vlc.MediaPlayer("playlists/" + playlist + "/" + songs[index])
    p.audio_set_volume(50)
    p.play()
    print("playing: " + songs[index])
    time.sleep(1.5)
    time.sleep(p.get_length() / 1000)
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
