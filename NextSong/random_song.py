import requests
from PIL import Image
from bs4 import BeautifulSoup
import random

import re
from NextSong.songs import Song

class randomsong:
    def getSong(self):
        random_song_url = requests.get("https://www.songlyrics.com/r-and-b-lyrics.php")

        # make it beautiful, remove the trash
        entire_table = BeautifulSoup(random_song_url.text, features="html.parser").find('tbody')
        # print(entire_table)
        items = []
        for el in entire_table.findAll('tr'):
            song_title = el.find('h3').text
            artist_name = el.find('span').text

            find_image = el.find('img', attrs={"class": "tiny-img"})
            imgfile = find_image.get("src")
            im = Image.open(requests.get(imgfile, stream=True).raw)
            items.append((song_title, artist_name, im))
            # print(song_title,artist_name)
        # print(len(items))
        rand_item = random.choice(items)
        song = Song()
        song.image = rand_item[2]
        song.artist = rand_item[1]
        song.title = rand_item[0]
        
         # get likes data
        rst = requests.get(f'https://www.songlyrics.com/{song.artist}/{song.title}/')
        art_te = BeautifulSoup(rst.text, 'html.parser')
        span = art_te.find('span', {'id': 'fbbox-total'})
        like = re.sub(r'(\n?|\t?)', '', span.text)
        song.likes = like
        
        # get views
        song_ti = re.sub(" ", "-",song.title)
        song_s = re.sub("'", "", song_ti)
        ar = re.sub(" ","-",song.artist)
        artist_name = re.sub("'"," ",ar)
      

        res = requests.get(f'https://genius.com/{artist_name}-{song_s}-lyrics')
        art_text = BeautifulSoup(res.text, 'html.parser')
        spans = art_text.find_all('span', {'class': 'LabelWithIcon__Label-sc-1ri57wg-1 kMItKF'})
        check = 0
        for span in spans:
            if(check == 1):
                song.view = span.text
                check = 0
            else:
                check = 1
        try:
            sp =  art_text.find('span',{'class': "LabelWithIcon__Label-sc-1ri57wg-1 gjSNHg"})
            song.contributers = sp.text
           
        except:
                song.contributers = None
                print('')
       
        print('title: ', song.title)
        print('artist:', song.artist)
        print('likes: ', song.likes)
        if song.view != None:
            print('Views :', song.view)
        if song.contributers != None:
            print('contributers on Ginius.com: ',song.contributers)
        print('album cover: ')
        song.image.show()