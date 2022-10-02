import time

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from env.apiKeys import *
from rich.console import Console
from rich.progress import track
from art import text2art
console = Console()
songs_id_youtube = []
songs_name = []
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def make_playlist(name):
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "env/client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    create_playlist = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": name,
                "description": "Ported From Spotify",
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "private"
            }
        }
    )
    res = create_playlist.execute()
    playlistID = res['id']
    # Tried Batch request but no luck, So simple, old-school way
    console.print("\n[green]+[/green] Making Playlist! \n", style="bold red")

    for i in track(songs_id_youtube, description="          "):
        try:
            req = youtube.playlistItems().insert(
                part="snippet",
                body={
                    "kind": "youtube#playlistItem",
                    "snippet": {
                        "playlistId": playlistID,
                        "resourceId": {
                            "videoId": i,
                            "kind": "youtube#video"
                        }
                    }
                })
            response = req.execute()
        except:
            print("Error In ", i)

    console.print(f'\n \n[green]+[/green] Your Playlist is ready: https://www.youtube.com/playlist?list={playlistID}', style="bold red")

def add_youtube(keyword):
    global songs_id_youtube
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=keyword
    )
    response = request.execute()

    # for r in response['items']:
    #     print(r)
    songs_id_youtube.append(response['items'][0]['id']['videoId'])

def get_from_spotify(id):
    global songs_name
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id_spotify,
                                                               client_secret=client_secret_spotify))

    list_songs = sp.playlist_items(id, market='IN')
    console.print("\n[green]+[/green] Getting Songs From Spotify: \n", style="bold red")

    for y in track(list_songs['items'], description="          "):
        song = y['track']['name']
        for i in y['track']['artists']:
            song += " " + i['name']
        songs_name.append(song)

def do_the_work_kiddo(id, name):

    get_from_spotify(id)

    console.print(f'\n[green]+[/green] Finding Songs on Youtube:  \n', style="bold red")

    for i in track(songs_name, description="          "):
        add_youtube(i)

    make_playlist(name)

def main():
    console.print("[green]+[/green] Enter Your Spotify's Playlist ID: ", style="bold red", end="")
    playlist_id = input()
    console.print("\n[green]+[/green] Enter Name for your playlist: ", style="bold red", end="")
    playlist_name = input()
    do_the_work_kiddo(playlist_id, playlist_name)

if __name__ == "__main__":
    ART = text2art("REHASH")
    print(ART)
    main()
