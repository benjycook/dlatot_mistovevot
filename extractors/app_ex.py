# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
from time import sleep
from tqdm import tqdm
from tofes_class import Tofes


def get_csv_data(argv):
    action = argv[1]
    _year = argv[2]
    filename = os.path.dirname(os.getcwd())+'{}{}_{}.{}'.format('/data/scraped_data/', action, _year, 'csv')
    df = pd.read_csv(filename)
    return df

review_again = []

for year in range(2004, 2017):
    year = str(year)
    print ('\n{}'.format(year))
    for x, data in tqdm(enumerate(get_csv_data(['', 'appointment', year]).iterrows())):
        sleep(0.5)
        item = data[1]
        tofes_link = item.html_link
        item_info = {'year': year,
                     'action': item.action,
                     'company_name': item.company_name,
                     'maya_link': item.maya_link,
                     'tofes_link': tofes_link}
        if tofes_link == 'nan' or type(tofes_link) != str or len(tofes_link) < 10:
            review_again.append(item_info)
            continue

        tofes = Tofes(item_info)
        if not tofes.status:
            review_again.append(item_info)
            continue


        tofes.parse_html
