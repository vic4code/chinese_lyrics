# -*-coding=utf-8 -*-

import json
import os
from tqdm import tqdm
from youtubesearchpython import VideosSearch, ChannelsSearch
from utils.download import download_audio_from_youtube, retrieve_audio
import codecs
import sys
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def search_songs_by_artist(datadir, metadata_dir, artist):

    song_names = []

    for root, dirs, files in os.walk(metadata_dir):
        for file in files:
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                
                batches = json.load(f)
                for batch in batches:
                    if batch['artist'] == artist:
                        for song in batch['songs']:
                            song_names.append(song['song_name'])
                                   
                        return song_names


def search_lyrics_by_song(datadir, artist_id, song_id):

    filepath = os.path.join(datadir, 'txt', artist_id, song_id + '.txt')
    try:
        lines = open(filepath, 'r', encoding='utf-8').readlines()
        
    except FileNotFoundError:
        raise FileNotFoundError('File not found.')

    lyrics = []

    for line in lines:
        if ":" not in line and "：" not in line and "(" not in line and "（" not in line \
            and "-" not in line and "-" not in line: 
            lyrics.append(line)

    lyrics = "".join(lyrics)

    return lyrics


if __name__ == "__main__":


    datadir = 'data'
    metadata_dir = 'metadata'
    artist = '陳奕迅'
    
    song_names = search_songs_by_artist(datadir, metadata_dir, artist)
    # print(len(song_names), song_names)

    artist = '孫燕姿'
    song_names = search_songs_by_artist(datadir, metadata_dir, artist)
    # print(len(song_names), song_names)

    
    artist_id = 'pJEFcZhg'
    song_id = 'zHysF7vl'
    lyrics = search_lyrics_by_song(datadir, artist_id, song_id)
    # print(lyrics)


    ## Download audio from youtube
    retrieved = []
    failed = []
    save_dir = 'data/subset/audio'
    artist = '陳奕迅'
    song_names = search_songs_by_artist(datadir, metadata_dir, artist)

    for song_name in song_names:

        success = False

        # PARSE SONG ID INFO TO BE USED FOR SEARCHING ON YOUTUBE
        success = retrieve_audio(artist, song_name, save_dir, success)

        if success == True:
            retrieved.append(song_name)
            print('Retrieval of ' + song_name + ' - ' + artist + ' is successful.')

        if success == False:
            print('Could not retrieve the audio for ' + song_name +' due to search queries are not present in the video title!')
            failed.append([song_name, artist])
            #print('\n')
            
    # Print Length
    print(len(retrieved))
    
    # Print falied 
    print(failed)
    
    # Make up for the failed files
    for song_name, artist in failed:
        search_title = song_name + ' ' + artist
        videosSearch = VideosSearch(search_title, limit = 1)
        download_audio_from_youtube(song_name, artist, videosSearch.result()['result'][0]['link'], save_dir)
    
    # Print length after making up
    print(len(os.listdir(save_dir)))


