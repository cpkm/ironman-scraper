#ironman-scraper
import csv
import requests
import os.path
from bs4 import BeautifulSoup

class Athlete:
    def __init__(self):
        self.name = None
        self.bib = None
        self.division = None
        self.age = None
        self.state = None
        self.country = None
        self.points = None
        self.overall_rank = None
        self.divison_rank = None
        self.gender_rank = None

a1 = Athlete()

athlete_link = 'http://www.ironman.com/triathlon/events/americas/ironman-70.3/muskoka/results.aspx?rd=20190707&race=muskoka70.3&bidid=8&detail=1'

page_response = requests.get(athlete_link, timeout=5)
soup = BeautifulSoup(page_response.content, 'html.parser')

result_window = soup.find('div', {'class':'moduleWrap eventResults resultsListing resultsListingDetails'})

header = result_window.find('header')
a1.name = header.h1.get_text()
a1.overall_rank = int(header.find('div', {'id':'div-rank'}).get_text().split(': ',1)[-1])
a1.divison_rank = int(header.find('div', {'id':'rank'}).get_text().split(': ',1)[-1])
a1.gender_rank = int(header.find('div', {'id':'gen-rank'}).get_text().split(': ',1)[-1])

general_info = result_window.find('table', {'id': 'general-info'}).find_all('td')

a1.bib = int(general_info[2].get_text())
a1.division = general_info[4].get_text()
a1.age = int(general_info[6].get_text())
a1.state = general_info[8].get_text()
a1.country = general_info[10].get_text()
a1.profession = general_info[12].get_text()
a1.points = general_info[14].get_text()

