# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
from time import sleep
from tqdm import tqdm
from templates2 import *
from templates import *


def classify_report_by_type(soup):
    # return MisparTofes
    try:
        res = soup.find_all('td', {"class": "clsTable"})[0].contents[1].contents[1].contents[0]
    except:
        res = ''
    # print(res)
    return res


def get_csv_data(argv):
    action = argv[1]
    _year = argv[2]
    filename = os.path.dirname(os.getcwd())+'{}{}_{}.{}'.format('/data/scraped_data/', action, _year, 'csv')
    df = pd.read_csv(filename)
    return df

forms = set()
for year in range(2004, 2017):
    year = str(year)
    print ('\n{}'.format(year))
    for x, data in tqdm(enumerate(get_csv_data(['', 'appointment', year]).iterrows())):
        if x > 10:
            break
        sleep(0.5)
        url = data[1].html_link
        company_name = data[1].company_name
        if url == 'nan':
            continue
        if type(url) != str:
            continue
        if len(url) < 10:
            continue
        res = requests.get(url)

        if res.status_code != 200:
            print(res.status_code)

        page_text = res.content
        soup = BeautifulSoup(page_text, 'html.parser')
        # soup = BeautifulSoup(res.content.decode('utf-8', 'ignore'), 'html.parser')

        functions = {
            # u'ת090': lambda x: template_090(x),
            # u'ת091': lambda x: template_091(x)
            # u'ת093': lambda x: template_093(x)
            #  u'ת304': lambda x: template_304(x) #,
            u'ת306': lambda x: template_306(x)
            # u'ת307': lambda x: tempalte_307(x)
        }

        report_type = classify_report_by_type(soup)
        if report_type not in functions.keys():
            # print(report_type)
            continue
        if not len(report_type): # or report_type != u'ת093':
            continue
        # data = functions[report_type]((soup, year))
        try:
            print(url)
            data = type1((soup, year))
            # flag = False
            break
        except:
            # data = type2((soup, year))
            print '00000'
            break

        # len_before  = forms.__len__()
        # forms.add(report_type)
        # if forms.__len__() != len_before:
        #     print(report_type)
        #     print(url)
        # # print(soup.find_all('textarea',{'class':'TextareaDeploy'})[0].contents)


print(set(forms))
