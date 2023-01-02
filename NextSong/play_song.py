import re
import vlc
import json
import requests
from PIL import Image
from bs4 import BeautifulSoup


class playsong:
    
    def play_song(self):
        url = requests.get("https://www.chosic.com/genre-chart/rhythm-and-blues/")
        art_text = BeautifulSoup(url.text, 'html.parser')
        span = art_text.find('div', {'class': 'track-list-item-right suggest-player'})(['data-previewurl'])
        # span
        p = vlc.MediaPlayer(span)
        p.play()
        # p.stop()
