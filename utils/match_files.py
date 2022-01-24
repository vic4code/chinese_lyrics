from genericpath import exists
import json
import os
import requests
from opencc import OpenCC
from tqdm import tqdm

cc = OpenCC('s2t')
path = os.path.join('metadata', 'pages', '3.json')

f = open(path)
data = json.load(f)
id_list = []

for d in data:
    if d['artist'] == '周杰倫':
        id_list = d
        break

# print(id_list['songs'][0])
def name_to_id(name):

    for song in id_list['songs']:
        if name in song['song_name']:
            return song['song_id']

def save_lrc_file(song_id):

    lrc_url = 'https://www.kugeci.com/download/lrc'
    txt_url = 'https://www.kugeci.com/download/txt'

    lrc = requests.get(os.path.join(lrc_url, song_id), allow_redirects=True)
    txt = requests.get(os.path.join(txt_url, song_id), allow_redirects=True)

    lrc_dir = os.path.join('data/audio', 'lrc')
    txt_dir = os.path.join('data/audio', 'txt')
    
    if not os.path.exists(lrc_dir):
        os.makedirs(lrc_dir)

    with open(os.path.join(lrc_dir, song_id + '.lrc'), 'w') as f:
        f.write(cc.convert(lrc.text))

    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)

    with open(os.path.join(txt_dir, song_id + '.txt'), 'w') as f:
        f.write(cc.convert(txt.text))


if __name__ == "__main__":

    songs = []
    audio_path = os.path.join('data', 'audio')
    for root, dirs, files in os.walk(audio_path):
        for file in files:
            if file.endswith('.mp3'):
                match_file = file.split(' ')[0]
                song_id = name_to_id(match_file)
                if song_id:
                    songs.append(
                                    {
                                    'song_name':file,
                                    'song_id':song_id
                                    }
                                )
                
                    os.rename(os.path.join(root, file), os.path.join(root, song_id + ".mp3"))

    print('Matched songs: ',len(songs))

    for song in tqdm(songs):          
        print(song)
        song_id = song['song_id']
        # save_lrc_file(song_id)

