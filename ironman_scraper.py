# -*- coding: utf-8 -*-
#ironman-scraper
import pandas as pd
import csv
import time
import requests
import os.path
from bs4 import BeautifulSoup
from athlete_scraper import simple_scrape, get_event_links, scrape_athlete_links, full_scrape

results_link = 'https://www.ironman.com/triathlon/events/americas/ironman/canada/results.aspx'
#'http://www.ironman.com/triathlon/events/emea/ironman-70.3/haugesund/results.aspx'
#'http://www.ironman.com/triathlon/events/americas/ironman-70.3/muskoka/results.aspx'

#simple_scrape(results_link, outfile='data/data4')
#scrape_athlete_links(results_link, outfile='data/data2')

#ad = pd.read_csv('data/haugesund703/athlete_links.csv')

full_scrape(results_link, data_outfile='data/canada140/data', link_outfile='data/canada140/athlete_links')
