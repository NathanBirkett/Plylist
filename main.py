# importing packages
import random
import time
import pytube
import os
# os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')  
import vlc
import copy

print(vlc.__file__)
def new_playlist(name):
    os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "playlists", name))


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


def play(playlist):
    song_list = os.listdir("playlists/" + playlist)
    print(song_list)
    queue = create_list(song_list, playlist)
    for num in range(0,len(queue)):
        play_song(playlist, queue, num)

def total_time(len_dict, song, list):
    return len_dict[song] * list.count(song)


def create_list(music_list, playlist):
    song_length = {}
    balance = 0
    for song in music_list:
        song_length[song] = music_length(song, playlist)
    long_len = song_length[max(song_length, key=song_length.get)]
    new_list = copy.copy(music_list)
    while not balance == len(song_length):
        balance = 0
        for song in song_length:
            if long_len < total_time(song_length, song, new_list):
                long_len = total_time(song_length, song, new_list)
        for song in song_length:
            error = long_len - total_time(song_length, song, new_list)
            if error >= 60000:
                new_list.append(song)
            else:
                balance += 1
    random.shuffle(new_list)
    print(new_list)
    for song in song_length:
        print(song, new_list.count(song))
    return new_list
    

"""
ex: 3 songs: A: 1:30, B: 4:00, C: 1:00
sample random (A, C, B)
find longest element (B)

while all element sums < 60000:
    for each element in sample:         (A)     (B)     (C)
        sum total element time          (1:30)  (4:00)  (1:00)
        error = longest - el_time       (2:30)  (0)     (3:00)
        if error > 60000:               (no)    (yes)   (no)
            randomly insert duplicate of element    (A, A, C, C, A, B, C, C)
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

print(pytube.__version__)
run()
