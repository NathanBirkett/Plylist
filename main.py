import random
from tkinter.ttk import Combobox, Progressbar
from Song import Song
from Playlist import Playlist
import Catalog
from tkinter import *
from pygame import mixer
import pygame as pg
import pickle
import time

root = Tk()
root.title("Music Player")

def next_song(history):
    songLengths = dict(zip(playlist.songs, list(map(lambda x: x.length, playlist.songs))))
    total_time = dict(zip(playlist.songs, [history.count(song) * songLengths[song] for song in playlist]))
    random.shuffle(shuffled_total := list(total_time.items()))
    shortest = min(shuffled_total, key=lambda x: x[1])[0]
    return shortest
    
history: list[Playlist]
playlist: Playlist
volume: int
Catalog.restore()
try:
    with open("userdata/data.pickle", "rb") as infile:
        data = pickle.load(infile)
        history = data[0]
        playlist = data[1]
        volume = data[2]
except:
    history = []
    playlist = Catalog.playlists_map["all"]
    volume = 50

mixer.init()

last_time = 0
def play_music():
    if play_button["text"] == "Play":
        play_button["text"] = "Pause"
        history.append(next_song(history))
        mixer.music.load(history[len(history)-1].path)
        mixer.music.play()
        global last_time
        last_time = time.time()
    elif play_button["text"] == "Pause":
        play_button["text"] = "Resume"
        mixer.music.pause()
    elif play_button["text"] == "Resume":
        play_button["text"] = "Pause"
        mixer.music.unpause()
        
        
def skip():
    mixer.music.stop()
    
def reset():
    global playlist
    global history
    global elapsed
    mixer.music.pause()
    elapsed = 0
    progress["value"] = 0
    history = []
    play_button["text"] = "Play"
    song_list.delete(0, song_list.size())
    for song in playlist:
        song_list.insert(END, song.name)
        
def callback(*args):
    if selected.get() == "new playlist...":
        add_playlist_frame.tkraise()
    else:
        global playlist
        reset()
        playlist = Catalog.playlists_map[selected.get()]
        song_list.delete(0, song_list.size())
        for song in playlist:
            song_list.insert(END, song.name)

pg.init()
mixer.music.set_endevent(pg.USEREVENT+1)

def check_input(event):
    value = event.widget.get()
    lst = Catalog.playlists_map["all"].songs
    if value == '':
        add_song['values'] = lst
    else:
        data = []
        for item in lst:
            if value.lower() in item.name.lower():
                data.append(item)

        add_song['values'] = data
        
def put_song():
    if not add_song.get() in tentative_playlist.get(0, END):
        tentative_playlist.insert(0, add_song.get())

def remove_song():
    if add_song.get() in tentative_playlist.get(0, END):
        tentative_playlist.delete(tentative_playlist.get(0, END).index(add_song.get()))
        
def create_playlist(name, songs):
    base_frame.tkraise()
    Catalog.create_playlist(name, songs)
    dropdown["values"] = Catalog.playlists + ["new playlist..."]

add_playlist_frame = Frame(root, relief=RIDGE, borderwidth=1)
Label(add_playlist_frame, text="new playlist").grid(row=0, column=0, columnspan=2)
playlist_name = StringVar()
entry = Entry(add_playlist_frame, textvariable=playlist_name)
Label(add_playlist_frame, text="name: ").grid(row=1, column=0)
entry.grid(row=1, column=1)
Label(add_playlist_frame, text="song: ").grid(row=2, column=0)
add_song = Combobox(add_playlist_frame)
add_song["values"] = Catalog.playlists_map["all"].songs
add_song.bind("<KeyRelease>", check_input)
add_song.grid(row=2, column=1)
edit_list_frame = Frame(add_playlist_frame)
another = Button(edit_list_frame, text="add song", command=put_song)
another.grid(row=0, column=0)
remove_song_button = Button(edit_list_frame, text="remove song", command=remove_song)
remove_song_button.grid(row=1, column=0)
edit_list_frame.grid(row=4, column=0)
name_label = Label(add_playlist_frame, textvariable=playlist_name, relief=GROOVE, bg="white").grid(row=3, column=1)
tentative_playlist = Listbox(add_playlist_frame, height=4)
tentative_playlist.grid(row=4, column=1)
done = Button(edit_list_frame, text="done", command=lambda: create_playlist(entry.get(), tentative_playlist.get(0, END)))
done.grid(row=2, column=0)
add_playlist_frame.grid(row=0, column=0)

base_frame = Frame(root)
list_frame = Frame(base_frame)
buttons = Frame(base_frame)

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

selected = StringVar(value="select a playlist")
selected.trace_add("write", callback)
dropdown = Combobox(list_frame, textvariable = selected, state="readonly")
dropdown["values"] = Catalog.playlists + ["new playlist..."]
dropdown.pack(side=TOP)

song_list = Listbox(list_frame, yscrollcommand=scrollbar.set, width=0)
for song in playlist:
   song_list.insert(END, song.name)

song_list.pack(side=LEFT)
scrollbar.pack(side=RIGHT, fill=Y)
scrollbar.config(command=song_list.yview)
list_frame.grid(row=0, column=0)
buttons.grid(row=0, column=1)

progress = Progressbar(base_frame, mode="determinate")
root.grid_columnconfigure(0, weight=0)
progress.grid(row=1, column=0, columnspan=2, sticky=E+W)
base_frame.grid(row=0, column=0)

def on_closing():
    with open("userdata/data.pickle", "wb") as outfile:
        pickle.dump([history, playlist, slider.get()], outfile)
    Catalog.save()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

elapsed = 0
def check_event():
    global elapsed
    global last_time
    song_list.select_clear(0, song_list.size())
    if not history == []:
        song_list.select_set(playlist.songs.index(history[len(history)-1]))
        song_list.see(playlist.songs.index(history[len(history)-1]))
        if mixer.music.get_busy():
            elapsed += time.time() - last_time
            progress["value"] = elapsed / (history[len(history)-1].length / 1000) * 100
    last_time = time.time()
    for event in pg.event.get():
        if event.type == pg.USEREVENT+1:
            elapsed = 0
            history.append(next_song(history))
            mixer.music.load(history[len(history)-1].path)
            mixer.music.play()
            last_time = time.time()
    mixer.music.set_volume(slider.get() / 100)
    root.after(100, check_event)

check_event()
root.mainloop()
pg.quit()