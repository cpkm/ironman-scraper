# -*- coding: utf-8 -*-
#athlete-scraper
import pandas as pd
import csv
import time
import requests
import os
from bs4 import BeautifulSoup
from random import uniform

class Athlete:

    def __init__(self):
        self.link = None
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
        self.bike_time  = None
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

def soup_link(link, timeout=20, return_latency=False, retry=5):

    for _ in range(retry):
        try:
            page_response = requests.get(link, timeout=timeout)
        except:
            print('Error in accessing page; retrying...')
            continue
        if page_response:
            break
        wait = get_wait(page_response.elapsed.total_seconds())
        print('--- Waiting {:6.3f} seconds ---'.format(wait))
        time.sleep(wait)

    try:
        if page_response:
            pass
    except:
        raise Exception('ResponseError: No response from the server.')

    latency = page_response.elapsed.total_seconds()
    soup = BeautifulSoup(page_response.content, 'lxml')

    if return_latency:
        return soup, latency
    else:
        return soup
    
def get_wait(latency=None, ftime=None, frandom=True, **kwargs):

    if ftime is not None:
        if frandom:
            rt = 1
        else:
            rt = 0
        wait_time = ftime*(1 + rt*uniform(-0.1,0.1))

    elif latency is None:
        wait_time = 10 

    elif latency < 1:
        wait_time = 10*latency
    
    else:
        wait_time = 10

    return wait_time

def scrape_athlete(link, return_latency=False):
    '''link is a direct link to the athlete-specific results page'''
    soup, latency = soup_link(link, return_latency=True)

    result_window = soup.find('div', {'class':'moduleWrap eventResults resultsListing resultsListingDetails'})

    header = result_window.find('header')
    general_info = result_window.find('table', {'id': 'general-info'}).find_all('td')
    race_summary = result_window.find('table', {'id': 'athelete-details'}).find_all('td')
    race_details = result_window.find('div', {'class': 'athlete-table-details'}).find_all('td')

    a1 = Athlete()
    a1.link = link
    a1.name = header.h1.get_text().strip()
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

    if return_latency:
        return a1, latency

    return a1

def simple_scrape(link, outfile='athlete_data', v=True, **kwargs):
    ''' Scrape summary data from general results page. Does not require request to individual athletes pages.
    link is to the general results page (usually 20 athletes per page)'''

    links = get_event_links(link)

    with open(outfile+'.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)

        for i,l in enumerate(links):
            if v:
                print('Processing page {:d} of {:d}'.format(i+1,len(links)))

            soup, latency = soup_link(l,return_latency=True)
            athlete_rows = soup.find('div',{'class':'results-athletes-table'}).find_all('tr')[1:]

            for ar in athlete_rows:
                data = ar.find_all('td')
                a1 = Athlete()
                a1.link = l + data[0].find('a').get('href')
                a1.name = data[0].get_text().strip()
                a1.overall_rank = set_int(data[4].get_text())
                a1.divison_rank = set_int(data[2].get_text())
                a1.gender_rank = set_int(data[3].get_text())
                a1.country = data[1].get_text()
                a1.points = data[9].get_text()
                a1.swim_time = time_split(data[5].get_text())
                a1.bike_time = time_split(data[6].get_text())
                a1.run_time = time_split(data[7].get_text())
                a1.total_time = time_split(data[8].get_text())
                
                writer.writerow(a1.__dict__.values())
            
            wait = get_wait(latency,**kwargs)
            if v:
                print('--- Waiting {:.3f} seconds ---'.format(wait))
            time.sleep(wait)

    return

def full_scrape(link, data_outfile='data/full_athlete_data', link_outfile='data/athlete_links', linkdf=None, v=True, **kwargs):
    ''' Scrape summary data from general results page. Does not require request to individual athletes pages.
    link is to the general results page'''

    if linkdf is not None:
        ad = linkdf
    else:
        ad = scrape_athlete_links(link, outfile=link_outfile, return_links=True, v=True)

    al = list(ad['link'])

    filename = data_outfile+'.csv'
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(filename, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        a1 = Athlete()
        writer.writerow(a1.__dict__.keys())

        for i,l in enumerate(al):
            if v:
                print('Processing page {:d} of {:d}'.format(i+1,len(al)))
            a1, latency = scrape_athlete(l,return_latency=True)
            writer.writerow(a1.__dict__.values())
            wait = get_wait(latency,**kwargs)
            if v:
                print('--- Waiting {:.3f} seconds ---'.format(wait))
            time.sleep(wait)
    return

def get_event_links(link, v=True):
    '''link is event results main page'''
    soup = soup_link(link)

    page_table = soup.find('div',{'id':'pagination'})
    last_page = page_table.find_all('span')[-2].get_text()
    last_page_link = page_table.find_all('a')[-2].get('href')

    page_links = [last_page_link.replace('p='+last_page, 'p='+str(n+1)) for n in range(int(last_page))]

    if v:
        print('Retrieved {:d} page links!'.format(len(page_links)))

    return page_links

def scrape_athlete_links(link, outfile='athlete_links', v=True, return_links=False):
    '''link is event results page'''

    page_links = get_event_links(link)
    total_links = 0
    filename = outfile + '.csv'

    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(filename, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['lastname','firstname','link','complete'])

        for i,p in enumerate(page_links):
            soup, latency = soup_link(p, return_latency=True)
            athlete_table = soup.find_all('a',{'class':'athlete'})
            athlete_links = [link+a.get('href') for a in athlete_table]
            writer.writerows([s.strip() for s in at.get_text().split(',',1)]+[al]+[0] for at, al in zip(athlete_table,athlete_links))

            total_links += len(athlete_links)
            wait = get_wait(latency)
            if v:
                print('Page {:d} of {:d}: Recovered {:d} athlete links!'.format(i+1, len(page_links), len(athlete_links)))
                print('--- Waiting {:.3f} seconds ---'.format(wait))
            time.sleep(wait)

    if v:
        print('Retrieved a total of {:d} athlete links!'.format(total_links))

    if return_links:
        return pd.read_csv(filename)

    return
