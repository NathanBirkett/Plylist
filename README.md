# Plylist

Ok so at first glance this is a really basic music player. It can download songs from YouTube and create playlists, and mix them, play and pause songs etc. But, the way this program randomizes the order is unique. It does it in such a way that once the playlist is listened to all the way through, the total amout of time each song was listened to will be about the same.

This was my first project in Python so it is extremely messy and probably breaks all of the Python norms, so definetly don't expect it to be bug free. It uses Pytube to download YouTube videos and vlc to play it, which probably wasn't the best choice concidering how annoying it is to install everything. Albeit simple, I created the algorithm to randomize the playlists on my own, and I like to think it's pretty efficient (I'm pretty sure it's O(n) but I'm not sure).

I learned a lot from this project including:
1. How to do basic Python
2. Multithreading
3. reading/writing to json files
4. creating algorithms
5. how to use github better

How to use: To create a playlist, type add playlist followed by the name. To add a song, type add song followed by the url to the YouTube video, the name, and what playlist you want to add it to. To play a playlist, type play followed by the playlist(s separated by a comma) you want to play. To rename a song, type rename followed by the playlist it's in, the current name, and the new one. While a song is playing type pause or resume to pause or resume playing, or type stop to stop. Then type quit to exit the program.
