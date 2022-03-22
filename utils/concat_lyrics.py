import os
import re
from tqdm import tqdm
import gzip

def concat(folder, save_file):

    lyrics_files = []
    lyrics = []

    # Traversal to store all paths
    for root, dirs, files in tqdm(os.walk(folder)):
        for f in files:
            lyrics_files.append(os.path.join(root, f))
    
    # Store all lines
    for file in tqdm(lyrics_files):
        lines = open(file, 'r').readlines()

        # Remove strings containing japanese, english and korean
        for line in lines:
            if ":" not in line and "：" not in line \
                and "(" not in line and "（" not in line and "-" not in line and "-" not in line \
                and re.search(u'[\u4e00-\u9fff]', line) \
                and not re.search("[\uac00-\ud7a3]", line) \
                and not re.search("[\u3040-\u30ff]", line) \
                or re.search('[a-zA-Z]', line): # English

                lyrics.append(line)

    lyrics = "".join(lyrics)
    f_out = gzip.open(save_file, 'wb')
    f_out.write(lyrics.encode())

if __name__ == '__main__':

    folder = 'data/txt'
    save_file = 'lyrics.gz'

    concat(folder, save_file)

    f = gzip.open(save_file, 'rt', encoding='utf-8')
    file_content = f.read()
    print(len(file_content))