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
root.title("Play Music")

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

selected = StringVar(value="select a playlist")
selected.trace_add("write", callback)
dropdown = Combobox(list_frame, textvariable = selected, state="readonly")
dropdown["values"] = Catalog.playlists
dropdown.pack(side=TOP)

song_list = Listbox(list_frame, yscrollcommand=scrollbar.set, width=0)
for song in playlist:
   song_list.insert(END, song.name)

song_list.pack(side=LEFT)
scrollbar.pack(side=RIGHT, fill=Y)
scrollbar.config(command=song_list.yview)
list_frame.grid(row=0, column=0)
buttons.grid(row=0, column=1)

progress = Progressbar(root, mode="determinate")
root.grid_columnconfigure(0, weight=0)
progress.grid(row=1, column=0, columnspan=2, sticky=E+W)