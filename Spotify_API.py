Client_ID = "90dbbf2f8937401ab6dc16cd04b8eeab"
Client_secret = "0c8c1eb1ece2431a8317d858eb629cd7"


from dotenv import load_dotenv
import os
import base64
from requests import post,get
import json
from Artists_database import rock_artists,pop_artists,country_artists
import random
load_dotenv()

def get_token():
    auth_string = Client_ID + ":" + Client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"

    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url,headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("no artits with this name exists")
        return None
    
    return json_result[0] 

def get_songs_by_artist(token,artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_popularity_by_artist(token, artist):
    result = search_for_artist(token, artist)
    return result["popularity"]

def quiz_generator(token,genre,year_span,difficulty):
    Quiz_results = []
    
    artist_list = f"{genre}_artists"
    artist_list = globals()[artist_list]
    info = {}
    num = 1
    random.shuffle(artist_list)
    for artists in artist_list:
        result = search_for_artist(token, artists)
        artist_id = result["id"]
        info[num] = {}
        info[num]["artist"] = artists
        
        
        songs = get_songs_by_artist(token, artist_id)
        song_list = []
        for idx, song in enumerate(songs):
            
            song_list.append([f"{song["name"]}, {song['album']['release_date'][0:4]}"])
            
        
            
        info[num]["songs"] = song_list
        
        num += 1

    index = 1
    if difficulty == "Easy":
        while len(Quiz_results) < 10:
            
            top_three_songs = info[index]["songs"][:3]
            random.shuffle(top_three_songs)
            for i in top_three_songs:
                
                if int(i[0][-4:]) <= int(year_span[-4:]) and int(i[0][-4:]) >= int(year_span[:4]):
                    Quiz_results.append(f"{info[index]["artist"]}, {i}")
                    break

            index += 1
            continue
    if difficulty == "Medium":
        while len(Quiz_results) < 10:
            
            top_three_songs = info[index]["songs"][3:7]
            random.shuffle(top_three_songs)
            for i in top_three_songs:
                
                if int(i[0][-4:]) <= int(year_span[-4:]) and int(i[0][-4:]) >= int(year_span[:4]):
                    Quiz_results.append(f"{info[index]["artist"]}, {i}")
                    break

            index += 1
            continue
    if difficulty == "Hard":
        while len(Quiz_results) < 10:
            
            top_three_songs = info[index]["songs"][7:]
            random.shuffle(top_three_songs)
            for i in top_three_songs:
                
                if int(i[0][-4:]) <= int(year_span[-4:]) and int(i[0][-4:]) >= int(year_span[:4]):
                    Quiz_results.append(f"{info[index]["artist"]}, {i}")
                    break

            index += 1
            continue

    for idx, res in enumerate(Quiz_results):
        print(f"{idx+1} : {res}")
    



token = get_token()

#Write "rock,pop,country" to get a genre
#Write a year span of which era the music should come from
#Write the difficulty of the quiz. Choose from "Easy,Medium,Hard"
quiz_generator(token,"pop","2010-2020","Easy")
