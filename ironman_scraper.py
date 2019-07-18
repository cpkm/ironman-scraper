#ironman-scraper
import csv
import requests
import os.path
from bs4 import BeautifulSoup

results_link = 'http://www.ironman.com/triathlon/events/emea/ironman-70.3/haugesund/results.aspx'
#'http://www.ironman.com/triathlon/events/americas/ironman-70.3/muskoka/results.aspx'
link = results_link
page_response = requests.get(link, timeout=5)
soup = BeautifulSoup(page_response.content, 'html.parser')

last_page = soup.find('div',{'id':'pagination'}).find_all('span')[-2].get_text()

print(last_page)