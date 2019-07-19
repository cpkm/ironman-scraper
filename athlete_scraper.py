#athlete-scraper
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
        self.profession = None
        self.points = None
        self.overall_rank = None
        self.divison_rank = None
        self.gender_rank = None
        self.swim_time = None
        self.bike_tim  = None
        self.run_time = None
        self.total_time = None
        self.swim_racetime = None
        self.bike_racetime = None
        self.run_racetime = None
        self.t1_time = None
        self.t2_time = None

def time_split(t):
    try:
        (h, m, s) = t.split(':')
    except ValueError:
        return float('nan')
    return int(h) * 3600 + int(m) * 60 + int(s)

def set_int(string):
    try:
        num = int(string)
    except ValueError:
        return float('nan')
    return num

def scrape_athlete(link):
    '''link is a direct link to the athlete-specific results page'''
    page_response = requests.get(link, timeout=5)
    soup = BeautifulSoup(page_response.content, 'html.parser')

    result_window = soup.find('div', {'class':'moduleWrap eventResults resultsListing resultsListingDetails'})

    header = result_window.find('header')
    general_info = result_window.find('table', {'id': 'general-info'}).find_all('td')
    race_summary = result_window.find('table', {'id': 'athelete-details'}).find_all('td')
    race_details = result_window.find('div', {'class': 'athlete-table-details'}).find_all('td')

    a1 = Athlete()
    a1.name = header.h1.get_text()
    a1.overall_rank = set_int(header.find('div', {'id':'div-rank'}).get_text().split(': ',1)[-1])
    a1.divison_rank = set_int(header.find('div', {'id':'rank'}).get_text().split(': ',1)[-1])
    a1.gender_rank = set_int(header.find('div', {'id':'gen-rank'}).get_text().split(': ',1)[-1])
    a1.bib = set_int(general_info[2].get_text())
    a1.division = general_info[4].get_text()
    a1.age = set_int(general_info[6].get_text())
    a1.state = general_info[8].get_text()
    a1.country = general_info[10].get_text()
    a1.profession = general_info[12].get_text()
    a1.points = general_info[14].get_text()
    a1.swim_time = time_split(race_summary[2].get_text())
    a1.bike_time = time_split(race_summary[4].get_text())
    a1.run_time = time_split(race_summary[6].get_text())
    a1.total_time = time_split(race_summary[8].get_text())
    a1.swim_racetime = time_split(race_details[3].get_text())
    a1.bike_racetime = time_split(race_details[11].get_text())
    a1.run_racetime = time_split(race_details[19].get_text())
    a1.t1_time = time_split(race_details[25].get_text())
    a1.t2_time = time_split(race_details[27].get_text())

    return a1

def simple_scrape(soup):
    '''soup is a BeautifulSoup of the general results page (usually 20 athletes per page)'''
    athlete_table = soup.find('div',{'class':'results-athletes-table'})
    return

