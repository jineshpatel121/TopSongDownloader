import billboard
from youtubesearchpython import VideosSearch
import yt_dlp
import os
import certifi
import ssl
import urllib.request

# Configure SSL context to use certifi's certificates
ssl_context = ssl.create_default_context(cafile=certifi.where())
https_handler = urllib.request.HTTPSHandler(context=ssl_context)
opener = urllib.request.build_opener(https_handler)
urllib.request.install_opener(opener)

# Fetch Billboard Hot 100 chart
chart = billboard.ChartData("hot-100")

# Get the number of songs to download
numSongs = int(input("How many songs do you want to download: "))

def getTopSongs(numSongs):
    topSongs = []
    for x in range(numSongs):
        topSongs.append(chart[x])
    return topSongs

# List of top songs
storedSongs = getTopSongs(numSongs)

def displaySongs():
    for song in storedSongs:
        print(f"{song.rank}.{song.title} by {song.artist}")

def searchYT(storedSongs):
    urls = []
    for song in storedSongs:
        title = song.title
        artist = song.artist
        search = VideosSearch(f"{title} by {artist}", limit=1)
        results = search.result()
        vidURL = results["result"][0]["link"]
        urls.append(vidURL)
    return urls

def downloadSongs(urls, directory):
    if os.path.exists(directory):
        print(f"Directory already exists: {directory}")
    else:
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': os.path.join(directory, '%(title)s.%(ext)s'),
        'ffmpeg_location': '/usr/local/bin/ffmpeg'  # Ensure this path is correct
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

# Example usage
displaySongs()

# Set download directory to the user folder of choice
folder = os.path.expanduser('~/Desktop')
urls = searchYT(storedSongs)
downloadSongs(urls, folder)
