# importing packages
import random
import time
from pytube import YouTube
import os
import vlc


def new_playlist(name):
    os.mkdir(os.path.join("C:/Users/Nathan/PycharmProjects/practice/playlists/", name))


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
    songs = os.listdir("playlists/" + playlist)
    song = songs[random.randrange(len(songs))]
    p = vlc.MediaPlayer("playlists/" + playlist + "/" + song)
    p.audio_set_volume(50)
    p.play()
    print("playing: " + song)
    time.sleep(1.5)
    time.sleep(p.get_length() / 1000)
    p.stop()
    play(playlist)


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
# new_playlist(str(input("name: ")))
# install_file(str(input("url: ")), str(input("name: ")))
# play_file(str(input("name: ")))
