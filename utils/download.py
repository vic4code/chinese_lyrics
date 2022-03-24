import os, re
import pandas as pd
import DALI as dali_code
from youtubesearchpython import VideosSearch, ChannelsSearch
from youtube_dl import YoutubeDL
import unidecode
import codecs
import sys
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def download_audio_from_youtube(artist, song_name, link, output_dir):
    
    output_filename = artist + '-' + song_name

    try:
        audio_downloader = YoutubeDL({
                                'format': 'bestaudio/best',
                                'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                                                   }],
                                'outtmpl': os.path.join(output_dir, output_filename + '.mp3'),
                                'quiet': False,
                            })

        audio_downloader.extract_info(link)
        
    except:
        
        print('Download with python failed!')
        print('Trying with API on bash.')
        cmd = f"""youtube-dl -o "{output_dir}/{output_filename}.mp3" --extract-audio -x --audio-format mp3 {link}"""
        os.system(cmd.encode('utf-8'))
        

def normalize_text(text): 
    # Convert to lowercase to match with search results 
    # AND REMOVE SPECIAL ALL CHARACTERS LIKE " (,),!,..."
    # AND REMOVE ACCENTS (NORMALIZE TEXT)
    return unidecode.unidecode(re.sub(r"[^a-zA-Z0-9'(-)(/) ]", r'', text.lower())) 
    

def retrieve_audio(artist, song_name, save_dir, success):
    
    success = False
    
    #missing = []
    #vid_titles = []
    
    # PARSE SONG ID INFO TO BE USED FOR SEARCHING ON YOUTUBE
    search_title = song_name + ' ' + artist
        
    # FIRST LIST OF SEARCH QUERIES, TO CHECK IF ALL EXIST IN THE 
    # YOUTUBE VIDEO TITLE    
    search_queries_1 = [song_name, artist]         
    
    # SECOND LIST OF SEARCH QUERIES, TO CHECK IF ANY EXISTS IN THE 
    # YOUTUBE VIDEO TITLE. THESE ARE DETERMINED TO RETRIEVE THE VERSIONS
    # USED IN DALI_TestSet4ALT DATASET
    search_queries_2 = ['official', 'lyrics']
    
    # THIRD LIST OF SEARCH QUERIES, TO CHECK IF ANY DOES NOT EXIST IN THE 
    # YOUTUBE VIDEO TITLE. THESE ARE DETERMINED TO RETRIEVE THE VERSIONS
    # USED IN DALI_TestSet4ALT DATASET
    search_queries_3 = ['remix']
    
    #THE ABOVE DEFINED LIST OF QUERIES CAN BE EXTENDED DEPENDING ON THE GOAL OF THE USER
    videosSearch = VideosSearch(search_title, limit = 2)
    for vid in videosSearch.result()['result']:
        vid_lower = normalize_text(vid['title'])
        print(vid['title'])
        if success == False:
            if all(item in vid_lower for item in search_queries_1):
                if any(item in vid_lower for item in search_queries_2):
                    #vid_titles.append([vid['title'],vid['link']])
                    download_audio_from_youtube(artist, song_name, vid['link'], save_dir)
                    success=True
                    break
                elif all(item not in vid_lower for item in search_queries_3):   
                   # vid_titles.append([vid['title'],vid['link']])
                    download_audio_from_youtube(artist, song_name, vid['link'], save_dir)
                    success=True  
                    break
    
    return success
        
        
    
