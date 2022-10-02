# Rehash 🎶
![issues](https://img.shields.io/github/issues/vaaibhavsharma/rehash?style=flat-square)
[![GitHub forks](https://img.shields.io/github/forks/vaaibhavsharma/rehash)](https://github.com/vaaibhavsharma/rehash/network?style=flat-square)
[![GitHub stars](https://img.shields.io/github/stars/vaaibhavsharma/rehash)](https://github.com/vaaibhavsharma/rehash/stargazers?style=flat-square)
![Python](https://img.shields.io/badge/python-v3.8+-blue.svg?style=flat-square&logo=python)

We all know YouTube's recommendation system is miles ahead of Spotify or any other platform

This simple script will take your Spotify playlist and port it to YouTube's playlist, so you don't have to search for all your favourite songs again!

## Running Script

### Step 1
```shell
git clone https://github.com/vaaibhavsharma/rehash.git
cd rehash
pip install -r requirements.txt
```

### Step 2

1. Create account at [Spotify Developers](https://developer.spotify.com/)
2. Get Client ID and Client Secret 
3. Go to [Google API Console](https://console.cloud.google.com/) and GET
    1. API KEY
    2. OAuth 2.0 Client ID

### Step 3
```shell
cd rehash #Project Directory
mkdir "env" # Make folder named env
```
Make file named apiKeys.py with following data

```shell
api_key = #Youtube API KEY
client_id_spotify = #Spotify 
client_secret_spotify = #Spotify
```

### Step 4

Enjoy your songs!

```shell
python main.py
```

## Working


https://user-images.githubusercontent.com/38813335/193477011-b2a7d295-1298-450b-95bb-5e5d8c7edebf.mp4




