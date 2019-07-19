#ironman-scraper
import csv
import time
import requests
import os.path
from bs4 import BeautifulSoup

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

    if page_response:
        pass
    else:
        raise Exception('ResponseError: No response from the server.')

    latency = page_response.elapsed.total_seconds()
    soup = BeautifulSoup(page_response.content, 'lxml')

    if return_latency:
        return soup, latency
    else:
        return soup
    
def get_wait(latency):
    if latency < 1:
        wait_time = 10*latency
    else:
        wait_time = 10

    return wait_time

results_link = 'http://www.ironman.com/triathlon/events/emea/ironman-70.3/haugesund/results.aspx'
#'http://www.ironman.com/triathlon/events/americas/ironman-70.3/muskoka/results.aspx'

soup, latency = soup_link(results_link,return_latency=True)

last_page = soup.find('div',{'id':'pagination'}).find_all('span')[-2].get_text()
last_page_link = soup.find('div',{'id':'pagination'}).find_all('a')[-2].get('href')

page_links = [last_page_link.replace('p='+last_page, 'p='+str(n+1)) for n in range(int(last_page))]

# print(page_links)

# for p in page_links:
#     soup, latency = soup_link(p, return_latency=True)
#     print('--- Request time: {:.3f}'.format(latency))
#     athlete_table = soup.find_all('a',{'class':'athlete'})
#     athlete_links = [results_link+a.get('href') for a in athlete_table]
    
#     wait = get_wait(latency)
#     print('--- Waiting {:.3f} seconds ---'.format(wait))
#     time.sleep(wait)
#     print('Recovered {:d} links!'.format(len(athlete_links)))
