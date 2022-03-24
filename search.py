# -*-coding=utf-8 -*-

import shutil
import json
import os
from tqdm import tqdm
from youtubesearchpython import VideosSearch, ChannelsSearch
from utils.download import download_audio_from_youtube, retrieve_audio
import codecs
import sys

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def search_songs_by_artist(datadir, metadata_dir, artist):

    songs = []

    for root, dirs, files in os.walk(metadata_dir):
        for file in files:
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                
                batches = json.load(f)
                for batch in batches:
                    if batch['artist'] == artist:
                        for song in batch['songs']:
                            songs.append({  
                                            'artist_id': batch['artist_id'],
                                            'song_name': song['song_name'],
                                            'song_id': song['song_id']
                            })
                                   
                        return songs


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
            lyrics.append(line.strip() + '\n')

    lyrics = "".join(lyrics)

    return lyrics

def download_audio(save_dir, artist):

    ## Download audio from youtube
    retrieved = []
    failed = []
    
    songs = search_songs_by_artist(datadir, metadata_dir, artist)
    song_names = [song['song_name'] for song in songs]

    for song_name in song_names:

        success = False

        # PARSE SONG ID INFO TO BE USED FOR SEARCHING ON YOUTUBE
        success = retrieve_audio(artist, song_name, save_dir, success)

        if success == True:
            retrieved.append(song_name)
            print('Retrieval of ' + artist + ' - ' + song_name + ' is successful.')

        if success == False:
            print('Could not retrieve the audio for ' + song_name + ' due to search queries are not present in the video title!')
            failed.append([artist, song_name])
            #print('\n')
            
    # Print Length
    print(len(retrieved))
    
    # Print falied 
    print(failed)
    
    # Make up for the failed files
    for artist, song_name in failed:
        search_title = artist + ' ' + song_name
        videosSearch = VideosSearch(search_title, limit = 1)
        try:
            download_audio_from_youtube(artist, song_name, videosSearch.result()['result'][0]['link'], save_dir)

        except:
            print('Search failed!')
            
    # Print length after making up
    print(len(os.listdir(save_dir)))

def restore_lyrics(datadir, metadata_dir, transcription_save_dir, artist):

    songs = search_songs_by_artist(datadir, metadata_dir, artist)

    for song in tqdm(songs):

        artist_id, song_name, song_id = song['artist_id'], song['song_name'], song['song_id']
        lyrics = search_lyrics_by_song(datadir, artist_id, song_id)

        filename = (artist + "-" + song_name + ".txt").replace(":","").replace("/","")
        filepath = os.path.join(transcription_save_dir, filename)

        with codecs.open(filepath.replace(" ","").encode('utf-8'), 'w', encoding='utf-8') as f:
            f.writelines(lyrics)


if __name__ == "__main__":


    datadir = 'data'
    metadata_dir = 'metadata'
    transcription_save_dir = 'data/subset/transcription'
    artist = '王力宏'

    # Restore lyrics
    restore_lyrics(datadir, metadata_dir, transcription_save_dir, artist)

    # Download youtube audio
    save_dir = 'data/subset/audio'
    download_audio(save_dir, artist)

    


