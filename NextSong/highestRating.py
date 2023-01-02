import re
import json
import requests
from PIL import Image
from bs4 import BeautifulSoup
from NextSong.songs import Song

class highestRSong:
    def get_rating(self):
        
        url = "https://spotify23.p.rapidapi.com/search/"
        search = "Big Energy"
        querystring = {"q":{search},"type":"R&B","offset":"0","limit":"1","numberOfTopResults":"1"}

        headers = {
            "X-RapidAPI-Host": "spotify23.p.rapidapi.com",
            "X-RapidAPI-Key": "f6f7ea39edmsh3b3072eed314667p141754jsn35fc580d2bab"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        jtxt = json.loads(response.text)
        
        for it in jtxt["tracks"]["items"]:
            song.title = it['data']['name']
            song.artist = it['data']['artists']["items"][0]['profile']['name']
            
        for it in jtxt["albums"]["items"]:
            alb_link = it['data']['coverArt']['sources'][0]['url']
            song.image = Image.open(requests.get(alb_link, stream=True).raw)
            
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
                
                
        print("Number one song of R&B genre in 2021")        
        print('title: ', song.title)
        print('artist:', song.artist)
        print('likes: ', song.likes)
        if song.view != None:
            print('Views :', song.view)
        if song.contributers != None:
            print('contributers on Ginius.com: ',song.contributers)
        print('album cover: ')
        song.image.show()