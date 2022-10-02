import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from env.apiKeys import *
from tqdm import tqdm

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
    for i in tqdm(songs_id_youtube, desc= "Loading Your Songs!"):
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
    print(f'Your Playlist is ready: https://www.youtube.com/playlist?list={playlistID}')

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
    for y in list_songs['items']:
        song = y['track']['name']
        for i in y['track']['artists']:
            song += " " + i['name']
        songs_name.append(song)

def do_the_work_kiddo(id, name):
    print("Getting Songs From Spotify....")
    get_from_spotify(id)
    print(f'Total Number of Songs: {len(songs_name)}')
    print("Finding Songs on Youtube....")
    for i in songs_name:
        add_youtube(i)
    print("Making Brand new Playlist....")
    make_playlist(name)

def main():
    playlist_id = input("Enter Your Spotify PlaylistID: ")
    playlist_name = input("Name for Youtube Playlist?:  ")
    do_the_work_kiddo(playlist_id, playlist_name)

if __name__ == "__main__":
    main()