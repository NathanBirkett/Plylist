import random
from tkinter.ttk import Progressbar
from Song import Song
import Catalog
from tkinter import *
from pygame import mixer
import pygame as pg
import pickle
import time

root = Tk()
root.title("Play Music")
# root.geometry("500x500")

def create_list(songs: list[Song]):
    mixed_list = random.sample(songs, len(songs))
    songLengths = dict(zip(songs, list(map(lambda x: x.length, songs))))
    longest = max(songLengths, key=songLengths.get)
    max_error = 1000000
    while max_error >= 1000000:
        longestLength = max(mixed_list.count(song) * songLengths[song] for song in songs)
        max_error = 0
        for song in songs:
            total_time = mixed_list.count(song) * songLengths[song]
            error = longestLength - total_time
            while error >= 60000:
                mixed_list.insert(random.randrange(len(mixed_list)+1), song)
                total_time = mixed_list.count(song) * songLengths[song]
                error = longestLength - total_time
        lengthArray = [(mixed_list.count(song) * songLengths[song]) for song in songs]
        max_error = max(lengthArray) - min(lengthArray)
    return mixed_list
    
playlist = create_list(Catalog.songs)
track = 0
volume = 0
with open("test.pickle", "rb") as infile:
    data = pickle.load(infile)
    playlist = data[0]
    track = data[1]
    volume = data[2]

mixer.init()

start_time = 0
def play_music():
    if play_button["text"] == "Play":
        play_button["text"] = "Pause"
        mixer.music.load(playlist[track].path)
        mixer.music.play()
        global start_time
        start_time = time.time()
    elif play_button["text"] == "Pause":
        play_button["text"] = "Resume"
        mixer.music.pause()
    elif play_button["text"] == "Resume":
        play_button["text"] = "Pause"
        mixer.music.unpause()
        
def skip():
    global track
    mixer.music.stop()
    
def reset():
    global track
    global playlist
    mixer.music.stop()
    playlist = create_list(Catalog.songs)
    track = -1
    play_button["text"] = "Play"
    for song in playlist:
        song_list.delete(0)
        song_list.insert(END, song.name)

pg.init()
mixer.music.set_endevent(pg.USEREVENT+1)

list_frame = Frame(root)
buttons = Frame(root)

play_button = Button(buttons, text="Play", command=play_music)
skip_button = Button(buttons, text="Skip", command=skip)
reset_button = Button(buttons, text="Reset", command=reset)
play_button.pack()
skip_button.pack()
reset_button.pack()

slider = Scale(buttons, from_=0, to=100, orient=HORIZONTAL)
slider.set(volume)
slider.pack()

scrollbar = Scrollbar(list_frame)

song_list = Listbox(list_frame, yscrollcommand=scrollbar.set, width=0)
for song in playlist:
   song_list.insert(END, song.name)

song_list.pack(side=LEFT)
scrollbar.pack(side=RIGHT)
scrollbar.config(command=song_list.yview)
list_frame.grid(row=0, column=0)
buttons.grid(row=0, column=1)

progress = Progressbar(root, mode="determinate")
root.grid_columnconfigure(0, weight=0)
progress.grid(row=1, column=0, columnspan=2, sticky=E+W)

def on_closing():
    with open("test.pickle", "wb") as outfile:
        pickle.dump([playlist, track, slider.get()], outfile)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

elapsed = 0
def check_event():
    global track
    global start_time
    global elapsed
    song_list.select_clear(0, len(playlist))
    song_list.select_set(track)
    if mixer.music.get_busy():
        elapsed = time.time() - start_time
    progress["value"] = elapsed / (playlist[track].length / 1000) * 100
        
    for event in pg.event.get():
        if event.type == pg.USEREVENT+1:
            print('music end event')
            track += 1
            mixer.music.load(playlist[track].path)
            mixer.music.play()
            start_time = time.time()
    mixer.music.set_volume(slider.get() / 100)
    root.after(100, check_event)

check_event()
root.mainloop()
pg.quit()