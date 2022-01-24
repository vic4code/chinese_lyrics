import requests
from tqdm import tqdm
from opencc import OpenCC
from bs4 import BeautifulSoup
import os
import json
import time
from datetime import datetime


def get_metadata(artist_url, song_url):
    cc = OpenCC('s2t')
    pages = [str(i) for i in range(1864)]
    # pages = '1'

    # Save as json
    metapath = os.path.join('metadata', 'pages')
    if not os.path.exists(metapath):
        os.makedirs(metapath)

    # Scrapping
    for page in tqdm(pages):
        if not os.path.exists(os.path.join(metapath, page + '.json')):
            artist_page = requests.get(artist_url + page, allow_redirects=True)
            artist_soup = BeautifulSoup(artist_page.text, 'html.parser')
            data = []

            # Find all artist under the search page
            for x in artist_soup.find(class_ ='table table-sm table-striped').find_all('a'):
                content = {
                        'artist_id':"",
                        'artist':"",
                        'songs':[],
                    }

                if x.get_text():

                    content['artist_id'] = x['href'].split('/')[-1]
                    content['artist'] = cc.convert((x.get_text()))
                
                    song_page = requests.get(os.path.join(song_url, content['artist_id']), allow_redirects=True)
                    song_soup = BeautifulSoup(song_page.text, 'html.parser')

                    # Find all songs under the artist
                    # tr = song_soup.find(class_ ='table table-sm table-striped').find_all('tr')[1:]
                    # print(tr[0].find_all('td')[1])
                    for tr in song_soup.find(class_ ='table table-sm table-striped').find_all('tr')[1:]:

                        td = tr.find_all('td')
                        content['songs'].append(
                                                {
                                                    'song_id':td[1].find('a')['href'].split("/")[-1].strip('\n'), 
                                                    'song_name':cc.convert((td[1].get_text())).strip(' '),
                                                    'lyricist':cc.convert((td[2].get_text())).strip('\n'),
                                                    'composer':cc.convert((td[3].get_text())).strip('\n'),
                                                }
                                            )
                            
                    data.append(content)
            
            # print(data)
        
            with open(os.path.join(metapath, page + '.json'), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            time.sleep(3)


def save_lyrics(song_id, artist_id):

    try:
        cc = OpenCC('s2t')

        lrc_dir = os.path.join('data', 'lrc', artist_id)
        txt_dir = os.path.join('data', 'txt', artist_id)
        
        # if not os.path.exists(lrc_dir):
        if not os.path.exists(lrc_dir):
            os.makedirs(lrc_dir)    

        lrc_url = 'https://www.kugeci.com/download/lrc'
        lrc = requests.get(os.path.join(lrc_url, song_id), allow_redirects=True)

        print(os.path.join(lrc_url, song_id))
        print(lrc)
        # print(os.path.join(lrc_url, song_id), cc.convert(lrc.text))

        res = cc.convert(lrc.text)[:20]
        print(res)

        if res == "":
            return False

        # Check if respond <404>
        if lrc.status_code == 404:
            print(os.path.join(lrc_url, song_id))
            return False

        with open(os.path.join(lrc_dir, song_id + '.lrc'), 'w') as f1:
            f1.write(cc.convert(lrc.text))

        if not os.path.exists(txt_dir):
            os.makedirs(txt_dir)

        txt_url = 'https://www.kugeci.com/download/txt'
        txt = requests.get(os.path.join(txt_url, song_id), allow_redirects=True)

        print(os.path.join(txt_url, song_id))
        print(txt)

        with open(os.path.join(txt_dir, song_id + '.txt'), 'w') as f2:
            f2.write(cc.convert(txt.text))
        
        print(cc.convert(txt.text)[:20])

        return True

    except:
        # datetime object containing current date and time
        now = datetime.now()
        print("now =", now)


def get_lyrics_data(meta_path):

    count = 0
    artist = 0

    for root, dirs, files in os.walk(meta_path):

        for i, file in tqdm(enumerate(files)):
            f = open(os.path.join(meta_path, file))
            data = json.load(f)

            for dic in data:
                artist += 1
                artist_id = dic['artist_id']

                print()
                print("file: ", file, "file number: ", i, "step: ", count)
                print("artist: ", dic['artist'])
                print("artist id: ", artist_id)
                print("number of songs to save: ", len(dic['songs']))

                for song in dic['songs']:
                    count += 1
                    res = save_lyrics(song['song_id'], artist_id)

                    if not res:
                        print("Wrong!@!")
                        break
                
                    time.sleep(1)

    print('Target artist: ', artist, 'Target number of files: ', count)


if __name__ == "__main__":

    artist_url = 'https://www.kugeci.com/singers?page='
    pages = [str(i) for i in range(1864)]
    # pages = '1'
    song_url = 'https://www.kugeci.com/singer'

    # Get metadata
    get_metadata(artist_url, song_url)

    # Get lyrics data
    meta_path = os.path.join('metadata', 'pages')
    get_lyrics_data(meta_path)

