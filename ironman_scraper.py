# -*- coding: utf-8 -*-
#ironman-scraper
import csv
import time
import requests
import os.path
from bs4 import BeautifulSoup
from athlete_scraper import simple_scrape, soup_link



results_link = 'http://www.ironman.com/triathlon/events/emea/ironman-70.3/haugesund/results.aspx'
#'http://www.ironman.com/triathlon/events/americas/ironman-70.3/muskoka/results.aspx'

soup, latency = soup_link(results_link,return_latency=True)

last_page = soup.find('div',{'id':'pagination'}).find_all('span')[-2].get_text()
last_page_link = soup.find('div',{'id':'pagination'}).find_all('a')[-2].get('href')

page_links = [last_page_link.replace('p='+last_page, 'p='+str(n+1)) for n in range(int(last_page))]

ar = simple_scrape(page_links,outfile='data2')



# with open('athlete_links.csv', 'w', encoding='utf-8') as f:
#     writer = csv.writer(f)
#     writer.writerow(['lastname','firstname','link','complete'])
#     for i,p in enumerate(page_links):
#         soup, latency = soup_link(p, return_latency=True)
#         print('--- Request time: {:.3f}'.format(latency))
#         athlete_table = soup.find_all('a',{'class':'athlete'})
#         athlete_links = [results_link+a.get('href') for a in athlete_table]
#         writer.writerows([s.strip() for s in at.get_text().split(',',1)]+[al]+[0] for at, al in zip(athlete_table,athlete_links))
#         #print([at.get_text() for at in athlete_table])
#         wait = get_wait(latency)
#         print('--- Waiting {:.3f} seconds ---'.format(wait))
#         time.sleep(wait)
#         print('Recovered {:d} links! Page {:d} of {:d}.'.format(len(athlete_links), i+1, len(page_links)))
