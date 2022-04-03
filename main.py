import discord
from json import load
from pathlib import Path
from discord.ext import commands
import youtube_dl
import os

with Path("config.json").open() as f:
    config = load(f)

TOKEN = config["token"]

client = commands.Bot(command_prefix="!")#TODO get this from config.json

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send('music is still playing')
        return
        
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
        
@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send('The bot is not connected to a voice channel')

@client.command()
async def pase(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send('No audio is playing')
        
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send('The audio isnt paused')
        
@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

client.run(TOKEN)